from typing import List
from dataclasses import dataclass
from agents import function_tool

@dataclass
class Issue:
    title: str
    description: str
    status: str
    assignee: str

@function_tool
def issues() -> List[Issue]:
    """
    Get Jira data from the last 24 hours
    
    Returns:
        List[dict]: A list of issues worked on the past 24 hours
            - title (str): The title of the issue
            - description (str): The description of the issue
            - status (str): The status of the issue
            - assigne (str): The assignee of the issue

    """
    return [
        Issue("Improve statistics for shots on goal", "Based on our new algorithm, we can improve how we calculate shots on goal", "Ready for production", "Peter Griffin"),
        Issue("Add a new redis caching solution", "Introduce a redis cache to handle our scaling issues. We must be able to handle a bigger amount of users without slowing down the system", "Deployed", "Bart Simpson")
    ]