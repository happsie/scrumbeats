from typing import List
from agents import function_tool, Agent, Runner
from datetime import datetime
from pydantic import BaseModel

class Release(BaseModel):
    project: str
    """The project name"""
    description: str
    """The description of what was released"""
    released: bool
    """If it has been release"""
    time: datetime
    """The time it was released"""

@function_tool
async def release() -> List[Release]:
    """
    Get CI/CD build data from the past 24 hours
    
    Returns:
        List[dict]: A list of CI/CD builds made the past 24 hours
            - project (str): The name of the project
            - name (str): The name of the build
            - success (bool): If the build was successful
    """
    agent = Agent(
        name="Release Mocker", 
        instructions="Generate 4 different releases related to building a technical hockey platform for teams.", 
        output_type=List[Release],
        model="gpt-4o-mini"
    )
    result = await Runner.run(agent, "Generate releases")
    return result.final_output