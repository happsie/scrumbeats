from agents import Agent, function_tool, output_guardrail, RunContextWrapper, GuardrailFunctionOutput
from scrumbeats.integrations.suno import SongCreator
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

class SongTitle(BaseModel):
    name: str
    """The title of the song"""

song_title_agent = Agent(
    name="Song Name Agent",
    instructions="""
        You are a song title agent for the product Scrumbeats. Your receive lyrics of the teams progress the last 24 hours and will give a good song title based on it. 
        Your goal is to generate a good song title.
    """,
    output_type=SongTitle,
    model="gpt-4o-mini"
)

class MusicStyle(BaseModel):
    style: str
    """The music style specified with text"""
    
@output_guardrail
async def character_length_guardrail(  
    ctx: RunContextWrapper, agent: Agent, output: MusicStyle
) -> GuardrailFunctionOutput:
    return GuardrailFunctionOutput(
        output_info=output,
        tripwire_triggered=len(output.style) > 200,
    )

music_style_agent = Agent(
    name="Song Name Agent",
    instructions="""
        You are a music style agent for the product Scrumbeats. Your receive lyrics of the teams progress the last 24 hours and will create a fitting music style using free text to describe it. 
        Your goal is to generate a good music style. The text can not be longer than 150 characters
    """,
    output_type=MusicStyle,
    model="gpt-4o-mini",
    output_guardrails=[character_length_guardrail]
)


song_creator = SongCreator()

song_director = Agent(
    name="Song Director",
    instructions="""
        You are a song director for the product Scrumbeats. Your receive a summary of the teams progress the last 24 hours and create a song. 
        Your goal is to use 'lyrics_manager' tool to come up with a good lyrics and the 'create_song' tool to generate a song with the lyrics. 

        Follow these steps carefully: 
        1. Gather lyrics: Use the 'lyrics_manager' tool. Pass the summary to the 'lyrics_manager', and only the received summary, nothing else. Do not proceed until lyrics has been provided.

        2. Generate a title: Pass lyrics to 'song_title_agent' to generate a good song name

        3. Generate a song style: Pass the lyrics to 'music_style_agent' to generate a fitting music style

        4. Use the song tool to create the song with lyrics. Pass the BEST lyrics, title and the generated style. ONLY CALL 'create_song' ONCE!

        Crucial Rules:
            - You DO NOT create lyrics by yourself
            - You pass the summary, and only the summary to the 'lyric_manager'
            - You may only call 'create_song' tool once per request. If you already called it, do not call it again. 
    """,
    tools=[
        lyrics_manager.as_tool(tool_name="lyrics_manager", tool_description="Generate the BEST lyric about the teams past 24 hours"),
        song_title_agent.as_tool(tool_name="song_title_agent", tool_description="Generate a song title based on lyrics"),
        music_style_agent.as_tool(tool_name="music_style_agent", tool_description="Generates a music style based on lyrics"),
        function_tool(song_creator.create_song)
    ],
    model="gpt-4o-mini",
    handoff_description="Convert a summary of a developer team to a song"
)