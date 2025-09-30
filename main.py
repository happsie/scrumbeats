import asyncio
import os
import time

from dotenv import load_dotenv
from scrumbeats.directors import scrumbeats_director
from agents import trace, Runner

def load_env():
    load_dotenv(override=True)
    global OPENAI_API_KEY
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise Exception("OpenAI API Key not specified")


def main():
    print("ScrumBeats is tuning up!")
    load_env()
    with trace("Scrumbeats Song Creator"): 
        prompt = """
            Create a song about the team progress the last 24 hours. 
        """
        result = asyncio.run(Runner.run(scrumbeats_director, prompt))
        print(result)

if __name__ == "__main__":
    main()
