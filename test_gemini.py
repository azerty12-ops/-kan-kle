import asyncio
import google.generativeai as genai

async def main():
    print(dir(genai.GenerativeModel))

asyncio.run(main())
