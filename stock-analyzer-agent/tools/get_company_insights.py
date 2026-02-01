from langchain_community.tools import DuckDuckGoSearchRun
from ddgs import DDGS

search = DDGS()
def get_company_news(ticker: str):
    results1 = search.news(f"{ticker} stock price movement", max_results=3)
    results2 = search.news(f"{ticker} earnings report", max_results=3)
    results3 = search.news(f"{ticker} analyst ratings", max_results=3)
    nested = [results1, results2, results3]
    unique_news = {}
    for sublist in nested:
        for news in sublist:
            unique_news[news['url']] = news
    unique_news_list = list(unique_news.values())
    return unique_news_list


def safe_get_company_news(ticker:str):

    try:
        return get_company_news(ticker)
    except Exception:
        return []