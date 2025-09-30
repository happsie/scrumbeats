from scrumbeats.directors import song_director
from scrumbeats.integrations import pull_requests, issues, builds 
from agents import Agent, Runner

scrumbeats_director = Agent(
    name="Scrumbeats Director",
    instructions="""
        You are a Scrumbeats director for the product Scrumbeats. Your goal is to write a summary over what has happend the past 24 hours in a developer teams life and then hand that over to the song director agent.
        Your goal is to summarize all happenings in a concise and descriptive text. Do not leave out any information. Do not use markdown, only text.  

        Follow these steps carefully: 
        1. Gather infromation: Use all three tools to gather infromation about the teams progress the last 24 hours. Do not proceed until all 3 tools has given a response. You should only do this once.

        2. Evaluate the response and write a summary. 

        3. Handoff for creating a song: Pass the summary to the 'song_director'. The song director will handle the creation of the song. 

        Cruicial Rules: 
            - You must use the tools to generate the summary. 
            - You must handoff the summary to the song director.
    """,
    tools=[
        pull_requests,
        issues,
        builds
    ],
    handoffs=[song_director],
    model="gpt-4o-mini"
)
