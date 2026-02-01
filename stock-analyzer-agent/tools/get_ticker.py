import yfinance as yf
from langchain_core.tools import tool

@tool
def search_ticker(query:str):
    """
    Search for ticker symbols based on a company name.
    Returns a list of potential matches with their symbols and exchanges.
    """
    print("trying to get the ticker for the stock!!!")
    search = yf.Search(query, max_results=5)
    if not search.quotes:
        return f"No ticker symbols found for '{query}'."
    arr = []
    for i in search.quotes:
        val = f"symbol: {i.get('symbol', 'N/A')} | quoteType: {i.get('quoteType', 'N/A')} | exchange: {i.get('exchange', 'N/A')} | shortname: {i.get('shortname', 'N/A')} | longname: {i.get('longname', 'N/A')}"
            
        
        arr.append(val)

    strData = "\n\n".join(arr)   
    return strData

