from pydantic import Field
from anthropic import BaseModel
from langchain.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage, trim_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.llm import llm
from src.tools import tools
from src.prompts import get_system_prompt
import os
from src.tokencounter import count_tokens
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    completed: bool

class ReviewResult(BaseModel):
    feedback: str = Field(description="Feedback on the code or 'Great job' if done")
    is_done: bool = Field(description="True if the user request is fully satisfied, False otherwise")
   

graph = StateGraph(State)

def startNode(state: State):
    print("Starting the agent! 🤖")
    return state

def call_model(state: State):
    # 1. TRIMMING STRATEGY
    # We keep the last 15 messages to prevent context overloading.
    # We include_system=True so the agent never forgets who it is.
    sys_prompt = get_system_prompt()
    trimmed_messages = trim_messages(
        state["messages"],
        max_tokens=8000, # Adjust based on your model's limit
        strategy="last",
        token_counter=count_tokens,
        include_system=True,
    )
    messages_to_send = [SystemMessage(content=sys_prompt)] + trimmed_messages
    # 2. BIND TOOLS
    llm_with_tools = llm.bind_tools(tools)
    
    # 3. INVOKE
    # We wrap this in a try/except for API Fault Tolerance
    try:
        response = llm_with_tools.invoke(messages_to_send)
        return {"messages": [response]}
    except Exception as e:
        # FAULT TOLERANCE: Return the error to the graph so it can retry or notify user
        return {"messages": [SystemMessage(content=f"API Error occurred: {str(e)}. Please try again.")]}

# def understandQueryNode(state: State):
#     # this is to understand the query.

#     files_list = []
#     for root, dirs, files in os.walk("."):
#         if "node_modules" in dirs: dirs.remove("node_modules") # Skip node_modules
#         if ".git" in dirs: dirs.remove(".git")                 # Skip .git
#         if "reACT-agent" in dirs: dirs.remove("reACT-agent")   # Skip its own folder (optional)
        
#         for name in files:
#             files_list.append(os.path.join(root, name))
            
#     # Convert list to a string
#     project_structure = "\n".join(files_list[:50]) # Limit to top 50 files to save tokens
    
#     # Inject into System Prompt
#     system_prompt = f"""
#     You are a React AI Coder.
#     You are currently in the root directory of the project.
    
#     Current Project Structure:
#     {project_structure}
    
#     Understand the user query and decide if you need to use tools to read files or create code.
#     *You will always write either jsx/tsx for components.*
#     *You will always write either js/ts for functions.*
#     """
    

#     prompt = SystemMessage(content = system_prompt)
#     llm_with_tools = llm.bind_tools(tools)
#     res= llm_with_tools.invoke([prompt] + (state.get("messages")))
#     print("understanding query Node: 🤔💭", res)
#     return {"messages": res, "completed": state.get("completed")}


# def reviewResponseNode(state: State):
#     prompt = SystemMessage(content = "you are quality code reviewer, Match the original user request with the work done and tell if the query is completed or not.")
#     all_messages = [prompt] + state.get("messages")
#     structured_llm = llm.with_structured_output(ReviewResult)
#     res = structured_llm.invoke((all_messages))
#     print(f"📝 Review: {res.feedback} (Done: {res.is_done})")
#     return {"messages": res, "completed": res.is_done}

# def isCompletedFn(state: State):
#     if state.get("completed"):
#         return "endNode"
#     else:
#         return "understandQueryNode"
    

def endNode(state: State):
    print("Completed User Query! ✅✅")
    return state


graph.add_node("startNode", startNode)
graph.add_node("agent", call_model)
# graph.add_node("understandQueryNode", understandQueryNode)
# graph.add_node("reviewResponseNode", reviewResponseNode)
graph.add_node("endNode", endNode)
graph.add_node("toolCallFnNode", ToolNode(tools))


graph.add_edge(START, "startNode")
graph.add_edge("startNode", "agent")
graph.add_edge("endNode", END)
graph.add_edge("toolCallFnNode", "agent")
graph.add_conditional_edges("agent", tools_condition, {"tools": "toolCallFnNode", END: "endNode"})
# graph.add_conditional_edges("reviewResponseNode", isCompletedFn)

memory = MemorySaver() # in memory saver.

graph = graph.compile(checkpointer=memory)


