from agents import Agent
from pydantic import BaseModel

lyrics_agent1 = Agent(
    name="Lyric Agent 1",
    model="gpt-4o-mini",
    instructions="""
        You are a lyric creator for Scrumbeats - A place where songs are made about development team progress.
        You write fun lyrics about the teams last 24 hours based on a summary. Answer with just the lyrics, and only the lyrics and no formatting.
        Only generate 15 sentences of lyrics
    """
)

lyrics_agent2 = Agent(
    name="Lyric Agent 2",
    model="gpt-4o-mini",
    instructions="""
        You are a lyric creator for Scrumbeats - A place where songs are made about development team progress.
        You write roast lyrics about the teams last 24 hours based on a summary. Answer with just the lyrics, and only the lyrics and no formatting.
        Only generate 15 sentences of lyrics
    """
)

lyrics_agent3 = Agent(
    name="Lyric Agent 3",
    model="gpt-4o-mini",
    instructions="""
        You are a lyric creator for Scrumbeats - A place where songs are made about development team progress.
        You write neutral lyrics about the teams last 24 hours based on a summary. Answer with just the lyrics, and only the lyrics and no formatting.
        Only generate 15 sentences of lyrics
    """
)

class Lyrics(BaseModel):
    lyrics: str
    """The BEST lyrics for the song"""

tool_description = "Write a lyrics about the teams past 24 hours"

lyrics_manager = Agent(
    name="Lyrics Manager",
    instructions="""
        You are a lyrics manager for the product Scrumbeats. Your receive a summary of the teams progress the last 24 hours and create the best lyrics for a song. 
        Your goal is to use lyrics agents tools to come up with good lyrics. You should run ALL lyrics tools and pick the BEST lyrics, and only ONE.

        Follow these steps carefully:

        1. Gather lyrics: Use all lyrics tool to create lyrics. Pass the summary to all lyrics agents, and only the received summary, nothing else. Do not proceed until all lyrics agents has provided a result.

        2. Evaluate: Take all lyrics and evaluate them. Pick the BEST one that is most aligned with the summary

        3. Return the BEST lyrics

        Crucial Rules:
            - You pass the summary, and only the summary to the lyrics agents
            - You evaluate all lyrics agents output before proceeding with a result
            - ONLY respond with the lyrics and nothing else. 
            - Do not use any formatting in the output
    """,
    tools=[
        lyrics_agent1.as_tool(tool_name="lyrics_agent1", tool_description=tool_description),
        lyrics_agent2.as_tool(tool_name="lyrics_agent2", tool_description=tool_description),
        lyrics_agent3.as_tool(tool_name="lyrics_agent3", tool_description=tool_description),
    ],
    output_type=Lyrics
)