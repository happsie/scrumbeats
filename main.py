import asyncio
import os

from dotenv import load_dotenv
from scrumbeats.agents import scrumbeats_director, song_director
from agents import trace, Runner

def load_env():
    load_dotenv(override=True)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise Exception("OpenAI API Key not specified")
    SUNOAPI_API_KEY = os.getenv("SUNOAPI_API_KEY")
    if not SUNOAPI_API_KEY:
        raise Exception("SunoAPI API Key not specified")


async def main():
    print("ScrumBeats is tuning up!")
    load_env()
    with trace("Scrumbeats Song Creator"): 
        prompt = """
            Create a song about the team progress the last 24 hours. 
        """
        await Runner.run(scrumbeats_director, prompt)
        print("ScrumBeats tuning down!")

asyncio.run(main())
