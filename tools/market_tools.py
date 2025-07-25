# tools/market_tools.py
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from config.settings import settings

@tool
def search_tool(query: str) -> str:
    """
    Performs a web search using Tavily for financial news and data.
    """
    print("🤖 [Tool Called] search_tool()")
    try:
        # Use the updated TavilySearch tool
        tavily_search = TavilySearch(max_results=5, tavily_api_key=settings.TAVILY_API_KEY)
        results = tavily_search.invoke(query)
        return results
    except Exception as e:
        return f"An error occurred during web search: {e}"

