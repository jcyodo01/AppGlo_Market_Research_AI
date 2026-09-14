import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()

def filter_results(company, results):
    filtered = []

    company_lower = company.lower()

    for result in results:
        title = result["title"].lower()
        content = result["content"].lower()

        if company_lower in title or company_lower in content:
            filtered.append(result)

    return filtered

def search_web(query, max_results=3):
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


def research_company(company):
    queries = {
        "jira_usage":
            f'"{company}" Jira Atlassian',

        "complexity":
            f'"{company}" employees offices company size',

        "digital_clutter":
            f'"{company}" digital transformation workflow data management',

        "ai_relevance":
            f'"{company}" artificial intelligence AI adoption',

        "growth_change":
            f'"{company}" growth acquisition restructuring expansion',

        "sales_accessibility":
            f'"{company}" IT leadership technology operations',
    }

    research = {}

    for category, query in queries.items():
        print(f"  Searching: {category}...")

        results = search_web(
            query,
            max_results=5
        )

        research[category] = filter_results(
            company,
            results
        )[:3]

    return research