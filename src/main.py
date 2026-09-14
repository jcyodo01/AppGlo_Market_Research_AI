from search import search_web
from models import ask_model
import time
from search import research_company


def format_results(results):
    evidence = ""

    for i, result in enumerate(results, start=1):
        evidence += f"""
SOURCE {i}
Title: {result['title']}
URL: {result['url']}
Content:
{result['content']}

"""

    return evidence


def main():
    company = input("Company to research: ")

    print(f"\nResearching {company}...\n")

    research = research_company(company)

    print("\n--- RESEARCH RESULTS ---")

    for category, results in research.items():
        print(f"\n=== {category.upper()} ===")

        for i, result in enumerate(results, start=1):
            print(f"\n[{i}] {result['title']}")
            print(result["content"])
            print(result["url"])


if __name__ == "__main__":
    main()