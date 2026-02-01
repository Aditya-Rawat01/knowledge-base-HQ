import yfinance as yf
from langchain_core.tools import tool


@tool
def get_stock_data(ticker:str)->dict|str:
    """
    Retrieves financial metrics for a ticker.
    US STOCKS: Use the plain ticker (e.g., 'AAPL', 'TSLA').
    INDIAN STOCKS: Append '.NS' or '.BO' (e.g., 'RELIANCE.NS').
    If unsure of the exchange, call search_ticker first."
    """
    print("Agent collecting stock data!!!")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or "currentPrice" not in info or "currency" not in info:
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