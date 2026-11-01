from django.conf import settings
from google import genai

client = genai.Client(api_key=settings.GEMINI_API_KEY)

PROMPT = """You are a friendly programming teacher for complete beginners.
Explain the following {language} code in simple natural language.

Rules:
1. Start with a one-line summary of what the code does.
2. Then explain it step by step in plain English.
3. Avoid jargon; define any technical term you must use.
4. If useful, end with a small example of input and output.
5. Use plain text only. Do not use markdown symbols such as **, #, or backticks. Number the steps like "1." and "2.".

Code:
{code}
"""

def explain_code(code: str, language: str = "python") -> str:
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=PROMPT.format(language=language, code=code),
    )
    return response.text