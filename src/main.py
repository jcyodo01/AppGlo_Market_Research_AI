from search import search_web
from models import ask_model
import time


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

    print(f"\nSearching for Jira/Atlassian evidence about {company}...\n")

    results = search_web(
        f'"{company}" Jira Atlassian',
        max_results=3
    )

    evidence = format_results(results)

    print("Search complete.")
    print("Sending evidence to Qwen...\n")

    prompt = f"""
You are evaluating a company for B2B market research.

COMPANY:
{company}

Your task is to determine whether the provided evidence
shows that the company itself uses Jira or Atlassian products.

IMPORTANT RULES:

1. Use ONLY the evidence provided below.
2. Do not use prior knowledge.
3. Do not assume that a product integration means the company
   internally uses Jira.
4. Distinguish between:
   - Direct evidence
   - Indirect evidence
   - Insufficient evidence
5. If the evidence does not prove something, say so.
6. Cite the source numbers that support your conclusion.

EVIDENCE:

{evidence}

AAnswer using EXACTLY this format:

Conclusion: Yes / No / Unclear
Evidence strength: High / Medium / Low
Reasoning: No more than 2 sentences.
Best sources: List source numbers only.

Keep the entire response under 120 words.
Do not provide hidden reasoning or step-by-step analysis.
"""
    print(f"Prompt length: {len(prompt):,} characters")
    print(f"Approximate tokens: {len(prompt) // 4:,}")

    start_time = time.time()

    response = ask_model(prompt)

    elapsed = time.time() - start_time

    print(f"\nModel response time: {elapsed:.1f} seconds")

    print("--- AI Evaluation ---")
    print(response)


if __name__ == "__main__":
    main()