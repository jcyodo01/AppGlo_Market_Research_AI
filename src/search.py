import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()


def search_web(query, max_results=5):
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise RuntimeError("TAVILY_API_KEY was not found.")

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=max_results,
        include_answer=False,
    )

    results = []

    for result in response.get("results", []):
        results.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
        })

    return results
