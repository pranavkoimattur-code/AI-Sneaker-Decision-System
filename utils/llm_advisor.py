import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_business_advisor(
    business_data: dict,
    question: str,
) -> str:
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    prompt = f"""
You are a business advisor helping a small company that produces
smart sneaker display cases.

Use only the business data provided below.

Business data:
{json.dumps(business_data, indent=2)}

Question:
{question}

Instructions:
- Answer the question directly.
- Use the supplied numbers.
- Explain the reasoning in simple language.
- Identify assumptions.
- Give one or two practical recommendations.
- Do not invent missing information.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    return response.output_text
