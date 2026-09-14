from models import ask_model


def main():
    company = input("Company to research: ")

    prompt = f"""
You are helping evaluate companies for B2B product-market fit.

Company: {company}

For now, do NOT research the company.

Simply confirm that you understand that {company}
is the company being evaluated.
"""

    response = ask_model(prompt)

    print("\n--- AI Response ---")
    print(response)


if __name__ == "__main__":
    main()
