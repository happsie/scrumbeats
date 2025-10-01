from agents import Agent
from scrumbeats.integrations.suno import create_song

lyrics_agent1 = Agent(
    name="Lyric Agent 1",
    model="gpt-4o-mini",
    instructions="""
        You are a lyric creator for Scrumbeats - A place where songs are made about development team progress.
        You write fun lyrics about the teams last 24 hours based on a summary. Answer with just the lyrics, and only the lyrics and no formatting.
        Only generate 10 sentences of lyrics
    """
)

lyrics_agent2 = Agent(
    name="Lyric Agent 2",
    model="gpt-4o-mini",
    instructions="""
        You are a lyric creator for Scrumbeats - A place where songs are made about development team progress.
        You write roast lyrics about the teams last 24 hours based on a summary. Answer with just the lyrics, and only the lyrics and no formatting.
        Only generate 10 sentences of lyrics
    """
)

lyrics_agent3 = Agent(
    name="Lyric Agent 3",
    model="gpt-4o-mini",
    instructions="""
        You are a lyric creator for Scrumbeats - A place where songs are made about development team progress.
        You write neutral lyrics about the teams last 24 hours based on a summary. Answer with just the lyrics, and only the lyrics and no formatting.
        Only generate 10 sentences of lyrics
    """
)

tool_description = "Write a lyrics about the teams past 24 hours"

song_director = Agent(
    name="Song Director",
    instructions="""
        You are a song director for the product Scrumbeats. Your receive a summary of the teams progress the last 24 hours and create a song. 
        Your goal is to use lyrics agents to come up with a good lyric and the 'create_song' tool to generate a song with the lyrics. 

        Follow these steps carefully: 
        1. Gather lyrics: Use all lyrics tool to create lyrics. Pass the summary to all lyrics agents, and only the received summary, nothing else. Do not proceed until all lyric agents has provided a result.

        2. Evaluate lyrics: Take all three lyrics and evaluate them, pick the best one and only one.

        3. Use the song tool to create the song with lyric. Pass the BEST lyric and a style (Rock, Rap, House, Techno, Country). ONLY DO THIS ONCE FOR THE BEST LYRIC!

        Crucial Rules:
            - You DO NOT create lyrics by yourself
            - You pass the summary, and only the summary to the lyrics agents
            - ONLY call 'create_song' tool ONCE with the BEST lyric. 
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