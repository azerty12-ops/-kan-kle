import asyncio
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

async def test():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "votre_cle_gemini_ici":
        print("No real key, but syntax is ok")
        return
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = await model.generate_content_async("Hello")
    print(response.text)

asyncio.run(test())
