from langgraph.graph import StateGraph, MessagesState, START, END
from typing import TypedDict, Optional
from typing_extensions import NotRequired
from langchain.messages import SystemMessage, HumanMessage
from main_agent import llm_with_tools
from langgraph.prebuilt import ToolNode, tools_condition
from tools.tools_export import available_tools

class MessageState(MessagesState):
    tickers: NotRequired[list[str]] # current convo stock symbols
    stock_data: NotRequired[dict[str, dict]] # for same conversation, cached data of a stock.
    sentiment_scores: NotRequired[dict[str, float]] # sentiment around the stock.


def setup_node(state:MessageState):
    print("Starting the agent!!")
    return state

def start_node(state: MessageState):
    print("Agent working!!")
    SYSTEM_PROMPT =  (
        "You are a helpful Financial Analyst. "
        "Use your tools to provide accurate, data-driven insights. "
        "Always use the calculate tool for any math. "
        "If a ticker is provided, get its data and sentiment before answering."
        "Try to use calculator tool and avoid any expensive calculation on your own, as you can hallucinate and provide wrong results"
    )
    messages = [SystemMessage(content = SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}

tool_node = ToolNode(available_tools)

workflow = StateGraph(MessageState)

workflow.add_node("setup_node", setup_node)
workflow.add_node("start_node", start_node)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "setup_node")
workflow.add_edge("setup_node", "start_node")
workflow.add_conditional_edges("start_node", tools_condition)
workflow.add_edge("tools", "start_node")


agent = workflow.compile()

result = agent.invoke({"messages":[HumanMessage(content="Compare Apple and Microsoft's sentiment")]})


print(result["messages"][-1].content)