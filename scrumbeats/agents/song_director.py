from agents import Agent, function_tool, output_guardrail, RunContextWrapper, GuardrailFunctionOutput
from scrumbeats.integrations.suno import SongCreator
from .lyrics_agents import lyrics_manager
from pydantic import BaseModel

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