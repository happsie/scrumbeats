from typing import List
from agents import function_tool, Agent, Runner
from pydantic import BaseModel

class Issue(BaseModel):
    title: str
    """The title of the issue"""
    description: str
    """The description of the feature/issue"""
    status: str
    """The status of the issue"""
    assignee: str
    """The assignee of the issue"""

@function_tool
async def issues() -> List[Issue]:
    """
    Get Jira data from the last 24 hours
    
    Returns:
        List[dict]: A list of issues worked on the past 24 hours
            - title (str): The title of the issue
            - description (str): The description of the issue
            - status (str): The status of the issue
            - assigne (str): The assignee of the issue

    """
    agent = Agent(
        name="Issue Tracker Mocker", 
        instructions="Generate 10 different development issues related to building a technical hockey platform for teams.", 
        output_type=List[Issue],
        model="gpt-4o-mini"
    )
    result = await Runner.run(agent, "Generate issues, only use the following assignee names: 'Jesper', 'Milo', 'Victor'")
    return result.final_output