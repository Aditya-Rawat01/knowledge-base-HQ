from pydantic import Field
from anthropic import BaseModel
from langchain.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from src.llm import llm
from src.tools import tools
import os
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

def understandQueryNode(state: State):
    # this is to understand the query.

    files_list = []
    for root, dirs, files in os.walk("."):
        if "node_modules" in dirs: dirs.remove("node_modules") # Skip node_modules
        if ".git" in dirs: dirs.remove(".git")                 # Skip .git
        if "reACT-agent" in dirs: dirs.remove("reACT-agent")   # Skip its own folder (optional)
        
        for name in files:
            files_list.append(os.path.join(root, name))
            
    # Convert list to a string
    project_structure = "\n".join(files_list[:50]) # Limit to top 50 files to save tokens
    
    # Inject into System Prompt
    system_prompt = f"""
    You are a React AI Coder.
    You are currently in the root directory of the project.
    
    Current Project Structure:
    {project_structure}
    
    Understand the user query and decide if you need to use tools to read files or create code.
    *You will always write either jsx/tsx for components.*
    *You will always write either js/ts for functions.*
    """
    

    prompt = SystemMessage(content = system_prompt)
    llm_with_tools = llm.bind_tools(tools)
    res= llm_with_tools.invoke([prompt] + (state.get("messages")))
    print("understanding query Node: 🤔💭", res)
    return {"messages": res, "completed": state.get("completed")}


def reviewResponseNode(state: State):
    prompt = SystemMessage(content = "you are quality code reviewer, Match the original user request with the work done and tell if the query is completed or not.")
    all_messages = [prompt] + state.get("messages")
    structured_llm = llm.with_structured_output(ReviewResult)
    res = structured_llm.invoke((all_messages))
    print(f"📝 Review: {res.feedback} (Done: {res.is_done})")
    return {"messages": res, "completed": res.is_done}

def isCompletedFn(state: State):
    if state.get("completed"):
        return "endNode"
    else:
        return "understandQueryNode"
    

def endNode(state: State):
    print("Completed User Query! ✅✅")
    return state


graph.add_node("startNode", startNode)
graph.add_node("understandQueryNode", understandQueryNode)
graph.add_node("reviewResponseNode", reviewResponseNode)
graph.add_node("endNode", endNode)
graph.add_node("toolCallFnNode", ToolNode(tools))
graph.add_edge(START, "startNode")
graph.add_edge("startNode", "understandQueryNode")
graph.add_edge("endNode", END)
graph.add_edge("toolCallFnNode", "understandQueryNode")
graph.add_conditional_edges("understandQueryNode", tools_condition, {"tools": "toolCallFnNode", END: "reviewResponseNode"})
graph.add_conditional_edges("reviewResponseNode", isCompletedFn)


agent = graph.compile()

userQuery = input("Enter your query 👉:")
print(userQuery)
agent.invoke({"messages": [HumanMessage(content=userQuery)]})





# v1



# cannot find the files and folders , throws error.
# not intelligent enough to understand the commands.
# will need shit ton on improvement.