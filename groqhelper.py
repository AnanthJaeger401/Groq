from groq import Groq
import asyncio
import dotenv

def create_prompt(kanji):
   return f"""For each of the following kanji: {' '.join(kanji)}, return a concise explanation under a subtitle for each kanji.

Format each kanji like this (optimized for Telegram message bubbles):

1.[Kanji]
Onyomi: [ひらがな]  
Kunyomi: [ひらがな]  
Words Onyomi: [漢字(かな)] = [English], [漢字(かな)] = [English]  
Words Kunyomi: [漢字(かな)] = [English], [漢字(かな)] = [English]

- Show Onyomi and Kunyomi readings in hiragana.  
- Show vocab in kanji with hiragana readings in parentheses.  
- Keep each line under ~35–40 characters.  
- Only include 1–3 vocab per reading type.  
- No extra spacing or explanation outside the blocks.
- At the end, provide 2 paragraphs that use all the kanji in their different readings, with a focus on natural usage.
- Make sure the whole response is of maximum 4096 characters, including the kanji list and the paragraphs.
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