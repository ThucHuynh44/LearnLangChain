from langchain_tavily import TavilySearch

# version khi muốn lấy output là text phù hợp với các câu trả lời nhanh
# def get_profile_url_tavily(name: str):
#     """Searches for Linkedin or twitter Profile Page."""
#     search = TavilySearch()
#     res = search.run(f"{name}")
#     return res

from langchain_community.tools.tavily_search import TavilySearchResults


# version khi muốn lấy output là JSON structured results
def get_profile_url_tavily(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return [r["url"] for r in res]
