from groq import Groq
import asyncio
import dotenv

def create_prompt(kanji):
   return f"""For each of the following kanji: {' '.join(kanji)}, provide a concise explanation formatted for Telegram message bubbles.

Use the following format for each kanji:

1. [Kanji]  
Onyomi: ひらがな  
Kunyomi: ひらがな  
▶ Onyomi Words:  
[漢字(かな)] = [English],  
[漢字(かな)] = [English],  
[漢字(かな)] = [English]  
▶ Kunyomi Words:  
[漢字(かな)] = [English],  
[漢字(かな)] = [English],  
[漢字(かな)] = [English]

- Break vocabulary into new lines to keep each under ~35–40 characters to prevent message wrap in Telegram.  
- Show Onyomi and Kunyomi in **hiragana** only.  
- Vocab must include **kanji + kana in parentheses** + brief English meaning.  
- Include **3 examples per reading** (no more than 4).  
- No extra spacing or explanations between kanji blocks.

At the end, include **2 short natural Japanese paragraphs** (with English translation), that demonstrate real-life usage of as many kanji from the list as possible.  
- Limit paragraph lines to ~35 characters for Telegram.  
- The full response must not exceed **4096 characters**.
"""


async def get_kanji_info(kanji_20):
    client = Groq(api_key=dotenv.get_key(".env", "GROQ_API_KEY"))
    prompt = create_prompt(kanji_20)
    # Await the create method
    completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{"role": "user", "content": prompt}],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stop=None,
    )

    # Access the response content
    full_response = completion.choices[0].message.content
    return full_response