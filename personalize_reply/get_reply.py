from google import genai
import os
from dotenv import load_dotenv
GOOGLE_API_KEY = os.getenv("GOOGLE_API")

client = genai.Client(api_key=GOOGLE_API_KEY)


def get_reply_text(parent_text,mention_text):
    print(f"{parent_text} and {mention_text}")

    response = client.models.generate_content(
     model="gemini-2.0-flash",
     contents=(
          "Someone mentioned me on this X post.\n\n"
          "Original Post: \"{parent_text}\"\n"
          "Mention Text: \"{mention_text}\"\n\n"
          "Write a concise, friendly, and natural-sounding reply (1–2 sentences). "
          "The reply should feel personalized and context-aware, not generic. "
          "Avoid repeating the same phrases across replies. No hashtags or emojis. "
          "Return only the reply text—no intro, explanation, or formatting."
     )
    )
    reply_text = response.text.strip()
    print(response)
    return reply_text
