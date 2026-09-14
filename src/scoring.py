import json

from models import ask_model


MAX_CONTENT_CHARS = 700


def build_evidence(research):
    """
    Convert Tavily research into a compact evidence package.
    """

    sections = []

    for category, results in research.items():

        # Digital clutter will be inferred from the other evidence.
        if category == "digital_clutter":
            continue

        sections.append(f"\n=== {category.upper()} ===")

        if not results:
            sections.append("No relevant evidence found.")
            continue

        for i, result in enumerate(results, start=1):
            content = result["content"][:MAX_CONTENT_CHARS]

            sections.append(
                f"""
Source {i}
Title: {result['title']}
Evidence: {content}
URL: {result['url']}
"""
            )

    return "\n".join(sections)


def score_company(company, research):

    evidence = build_evidence(research)

    prompt = f"""
You are evaluating a company as a potential customer for a
B2B digital-system cleanup service.

Company: {company}

Use ONLY the evidence provided below.
Do not use prior knowledge.

Score the company using this rubric:

1. jira_usage: 0-25
   Evidence that the company internally uses Jira or Atlassian products.
   Product integrations alone are weak evidence of internal usage.

2. complexity: 0-20
   Organizational size, number of teams, departments, locations,
   technical workforce, and operational complexity.

3. clutter_risk: 0-20
   Likelihood that the organization experiences digital-system clutter.
   Infer this from observable evidence such as organizational complexity,
   distributed teams, Jira usage, acquisitions, growth, and changing systems.
   Do NOT claim that clutter itself was directly observed unless evidence says so.

4. ai_relevance: 0-15
   Evidence of internal AI adoption, agentic systems, automation,
   or organizational reliance on AI.

5. growth_change: 0-10
   Evidence of hiring, acquisitions, restructuring, expansion,
   rapid growth, or other organizational change.

6. buyer_identifiability: 0-10
   Evidence that relevant technology, IT, operations, program-management,
   or digital-transformation leaders can be identified.

IMPORTANT:

- Missing evidence means uncertainty, not proof that something is false.
- Do not invent facts.
- Base every score on the supplied evidence.
- Total score must equal the six category scores.
- Return ONLY valid JSON.
- Do not include markdown.
- Do not provide chain-of-thought.

EVIDENCE:

{evidence}

Return exactly this JSON structure:

{{
    "company": "{company}",
    "scores": {{
        "jira_usage": 0,
        "complexity": 0,
        "clutter_risk": 0,
        "ai_relevance": 0,
        "growth_change": 0,
        "buyer_identifiability": 0
    }},
    "total_score": 0,
    "confidence": "low",
    "summary": "Brief evidence-based explanation of the score."
}}
"""

    print(
        f"\nScoring prompt: {len(prompt):,} characters "
        f"(~{len(prompt) // 4:,} tokens)"
    )

    response = ask_model(prompt)

    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError(
            "The model did not return valid JSON.\n\n"
            f"Model response:\n{response}"
        )

    return result
