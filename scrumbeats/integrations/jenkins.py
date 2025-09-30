from typing import List
from dataclasses import dataclass
from agents import function_tool
from datetime import datetime

@dataclass
class Build:
    project: str
    name: str
    success: bool
    time: datetime

@function_tool
def builds() -> List[Build]:
    """
    Get CI/CD build data from the past 24 hours
    
    Returns:
        List[dict]: A list of CI/CD builds made the past 24 hours
            - project (str): The name of the project
            - name (str): The name of the build
            - success (bool): If the build was successful
    """
    return [
        Build("hockey-platform", "Build #119", True, datetime(2025, 9, 28, 16, 11)),
        Build("hockey-stats", "Build #46", True, datetime(2025, 9, 28, 11, 56)),
        Build("hockey-stats", "Build #45", False, datetime(2025, 9, 28, 11, 54)),
        Build("hockey-stats", "Build #44", True, datetime(2025, 9, 28, 9, 45))
    ]