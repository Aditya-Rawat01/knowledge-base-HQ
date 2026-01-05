from typing import TypedDict, Optional
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
load_dotenv()
llm = init_chat_model(
    model="qwen/qwen3-32b",
    model_provider="groq",
)

class State(TypedDict):
    user_query: str
    isOk: bool
    llmOutput: Optional[str]

def initialize(state: State):
    response = llm.invoke(state.get("user_query"))
    state["llmOutput"] = response.content
    
    return state 

def routerFn(state: State):
    if (state.get("isOk")):
        return "endnode"
    else:
        return "corrector"


def corrector(state: State):
    print("is the state here?")
    response = llm.invoke(state.get("user_query"))
    state["llmOutput"] = response.content
    return state

def endnode(state: State):
    return state



graph = StateGraph(State)

graph.add_node("initialize", initialize)
# graph.add_node("routerFn", routerFn) this is a router function, not a node
graph.add_node("corrector", corrector)
graph.add_node("endnode", endnode)


graph.add_edge(START, "initialize")
graph.add_conditional_edges("initialize", routerFn) # this is conditional
graph.add_edge("endnode", END)

graph.compile().invoke(State(user_query="hello how are you", isOk=True, llmOutput=None))