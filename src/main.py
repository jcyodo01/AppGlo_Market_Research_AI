from search import research_company
from scoring import score_company


def main():
    company = input("Company to research: ")

    print(f"\nResearching {company}...\n")

    research = research_company(company)

    print("\nResearch complete.")
    print("Evaluating company...\n")

    result = score_company(company, research)

    scores = result["scores"]

    print("\n" + "=" * 45)
    print(f" COMPANY EVALUATION: {result['company']}")
    print("=" * 45)

    print(f"Jira / Atlassian:       {scores['jira_usage']:>2}/25")
    print(f"Complexity:              {scores['complexity']:>2}/20")
    print(f"Digital clutter risk:    {scores['clutter_risk']:>2}/20")
    print(f"AI relevance:            {scores['ai_relevance']:>2}/15")
    print(f"Growth / change:         {scores['growth_change']:>2}/10")
    print(f"Buyer identifiability:   {scores['buyer_identifiability']:>2}/10")

    print("-" * 45)
    print(f"TOTAL SCORE:             {result['total_score']:>2}/100")
    print(f"CONFIDENCE:              {result['confidence'].upper()}")

    print("\nSummary:")
    print(result["summary"])


if __name__ == "__main__":
    main()