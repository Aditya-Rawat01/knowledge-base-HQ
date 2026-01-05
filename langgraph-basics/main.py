from langchain_classic.schema.runnable import RunnableConfig
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver
load_dotenv()
llm = init_chat_model(
    model="qwen/qwen3-32b",
    model_provider="groq",
)
DB_URI = "mongodb://admin:admin@localhost:27017"
class State(TypedDict):
    # This is the manual equivalent of MessagesState
    messages: Annotated[list[BaseMessage], add_messages]

graph = StateGraph(State)


def firstNode(state: State):
    res = llm.invoke(state.get("messages"))
    return {"messages": res}


graph.add_node("firstNode", firstNode)

graph.add_edge(START, "firstNode")
graph.add_edge("firstNode", END)


with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:

    g1 = graph.compile(checkpointer = checkpointer)
    # reason for giving config is to know which conversation to load from the db.
    # thread_id = conversation id
    # giving thread_id = unique username, can simplify things as well.
    config: RunnableConfig = {
        "configurable" : {
            "thread_id" : "1"
        }
    }
    for chunk in g1.stream(input = {"messages":["hello, nice to meet you"]}, config=config, stream_mode="values"):
        chunk["messages"][-1].pretty_print()