from typing import List
from dataclasses import dataclass
from agents import function_tool
from datetime import datetime

@dataclass
class PullRequest:
    title: str
    description: str
    author: str
    time: datetime

@function_tool
def pull_requests() -> List[PullRequest]:
    """
    Get pull request informationfrom the past 24 hours

    Returns:
        List[dict]: A list of pull requests made the past 24 hours
            - title (str): The title of the pull request
            - description (str): The description of the PR
            - author (str): The author of the PR
    """
    return [
        PullRequest("Improve statistic for shots on goal", "Improves the hockey statistics for shots on goal made by a team", "Peter Griffin", datetime(2025, 9, 28, 15, 55)),
        PullRequest("Fix bug causing production outage", "", "Bart Simpson", datetime(2025, 9, 28, 11, 44)),
        PullRequest("Introduce new redis cache", "Introduces a new redis cache for the platform to faster load statistics", "Peter Griffin", datetime(2025, 9, 28, 9, 30))
    ]