from google import genai

client = genai.Client(api_key="AIzaSyByT_VZnfQL-675MOtvatDKn2WXs8STOQQ")


def get_reply_text(parent_text,mention_text):
    print(f"{parent_text} and {mention_text}")

    response = client.models.generate_content(
     model="gemini-2.0-flash",
     contents=(
         "Someone mentioned me on this X post: \"{parent_text}\" "
         "with the line: \"{mention_text}\". "
         "Generate a short reply (only 2 to 3 lines) to this mention. "
         "Only return the reply—no explanations, suggestions, or extra text."
     )
    )
    reply_text = response.text.strip()
    print(response)
    return reply_text
