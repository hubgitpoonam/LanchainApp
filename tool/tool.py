# to get the name from linkedin url
#from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch


def get_profile_url_tavily(name: str):
    """Searches for LinkedIn or twitter profile page."""
    search = TavilySearch(max_results=1)
    res = search.run(f"{name}")
    return res