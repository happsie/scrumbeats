from typing import List
from agents import function_tool, Agent, Runner
from datetime import datetime
from pydantic import BaseModel

class PullRequest(BaseModel):
    title: str
    """The title of the pull request"""
    description: str
    """The description of the change"""
    author: str
    """The author of the pull request"""
    time: datetime
    """The time the pull request was created"""
    status: str
    """The status of the pull request"""

@function_tool
async def pull_requests() -> List[PullRequest]:
    """
    Get pull request informationfrom the past 24 hours

    Returns:
        List[dict]: A list of pull requests made the past 24 hours
            - title (str): The title of the pull request
            - description (str): The description of the PR
            - author (str): The author of the PR
    """
    agent = Agent(
        name="Pull Request Mocker", 
        instructions="Generate 7 different pull requests related to building a technical hockey platform for teams.", 
        output_type=List[PullRequest],
        model="gpt-4o-mini"
    )
    result = await Runner.run(agent, "Generate pull requests, only use the following author names: 'Jesper', 'Milo', 'Victor'")
    return result.final_output