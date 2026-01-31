from tools.get_company_insights import safe_get_company_news
from tools.subagent import structuredllm
from langchain_core.tools import tool


def formatted_news_str(news_list: list[dict])->str:
    if not news_list:
        return "No recent news found for this ticker"
    
    formatted_items = []

    for i, news in enumerate(news_list, 1):
        title = news.get("title", "No title")
        snippet = news.get("body", "No body")
        date = news.get("date", "Unknown date")

        formatted_items.append(f"-----Article {i}----- \n Date: {date}\n Title: {title}\n Snippet: {snippet}")

    return "\n\n".join(formatted_items)



@tool
def get_sentiment(ticker: str):
    """
    Fetches recent news and returns a structured sentiment score (-1 to 1), 
    a label (Bullish/Bearish), and a summary. 
    Use this when the user asks 'how is the stock doing' or 'what is the news'.
    """
    print("Sub agent call!!!")
    news = safe_get_company_news(ticker)
    company_context = formatted_news_str(news)
    messages = [
    (
        "system",
        f"You are a financial analyst. Analyze the following news for {ticker} stock and provide a sentiment score.",
    ),
    ("human",
    company_context
    )
    ]
    msg = structuredllm.invoke(messages)
    return msg
