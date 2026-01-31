import yfinance as yf
from langchain_core.tools import tool


@tool
def get_stock_data(ticker:str)->dict|str:
    """
    Retrieves key financial metrics for a stock ticker including price, 
    market cap, P/E ratio, and 52-week highs/lows.
    """
    print("Agent collecting stock data!!!")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or "currentPrice" not in info:
            return f"Error: Could not find data for the ticker: {ticker}. It might be delisted or invalid."

        return {
            "price": info.get("currentPrice"),
            "currency": info.get("currency"),
            "pe_ratio": info.get("trailingPE"),
            "high_52wk": info.get("fiftyTwoWeekHigh"),
            "low_52wk": info.get("fiftyTwoWeekLow"),
            "sector": info.get("sector"),
            "market_cap": info.get("marketCap"),
            "volume": info.get("volume"),
            "change_percent": info.get("regularMarketChangePercent")
        }
    except Exception as e:
        return f"Error fetching data for {ticker}: {str(e)}"