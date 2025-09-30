from agents import Agent
from scrumbeats.integrations.elevenlabs import create_song

lyrics_agent1 = Agent(
    name="Lyric Agent 1",
    model="gpt-4o-mini",
    instructions="""
        You are a lyric creator for Scrumbeats - A place where songs are made about development team progress.
        You write fun lyrics about the teams last 24 hours. 
    """
)

lyrics_agent2 = Agent(
    name="Lyric Agent 2",
    model="gpt-4o-mini",
    instructions="""
        You are a lyric creator for Scrumbeats - A place where songs are made about development team progress.
        You write roast lyrics about the teams last 24 hours. 
    """
)

lyrics_agent3 = Agent(
    name="Lyric Agent 3",
    model="gpt-4o-mini",
    instructions="""
        You are a lyric creator for Scrumbeats - A place where songs are made about development team progress.
        You write neutral lyrics about the teams last 24 hours. 
    """
)

tool_description = "Write a lyrics about the teams past 24 hours"

# TODO: Composition
song_director = Agent(
    name="Song Director",
    instructions="""
        You are a song director for the product Scrumbeats. Your goal is to take a summary of the teams progress the last 24 hours and create a song. 
        Your goal is to come up with a good lyric and song. 

        Follow these steps carefully: 
        1. Gather lyrics: Use all lyrics tool to create lyrics. Do not proceed until all lyric agents has provided a result.

        2. Evaluate lyrics: Take all three lyrics and evaluate them, pick the best one and only one.

        3. Use the song tool to create the song with lyric. Pass the best lyric and a style (Rock, Rap, House, Techno, Country)
    """,
    tools=[
        lyrics_agent1.as_tool(tool_name="lyrics_agent1", tool_description=tool_description),
        lyrics_agent2.as_tool(tool_name="lyrics_agent2", tool_description=tool_description),
        lyrics_agent3.as_tool(tool_name="lyrics_agent3", tool_description=tool_description),
        create_song
    ],
    model="gpt-4o-mini",
    handoff_description="Convert a summary of a developer team to a song"
)