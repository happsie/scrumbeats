from agents import function_tool
import requests
import time
import os

@function_tool
def create_song(lyric: str, genre: str):
    """
    Create a song based on a lyrics and genre

    Args: 
        - lyric: The lyric to create a song with
        - Genre: The genre to create the song with 
    """
    SUNOAPI_API_KEY = os.getenv("SUNOAPI_API_KEY")
    print("Creating a song!")

    url = "https://api.sunoapi.org/api/v1/generate"

    payload = {
        "prompt": lyric,
        "style": genre,
        "title": "Song Director - Past 24!",
        "customMode": True,
        "instrumental": False,
        "model": "V3_5",
        "negativeTags": "",
        "vocalGender": "m",
        "styleWeight": 0.65,
        "weirdnessConstraint": 0.65,
        "audioWeight": 0.65,
        "callBackUrl": "https://api.example.com/callback"
    }
    headers = {
        "Authorization": f"Bearer {SUNOAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.json()["msg"] != "success":
        print("could not generate song.", response.json())
        return {"status", "error"}
    
    poll(0)
    return {"status": "success"}

def poll(attempts: int): 
    if attempts >= 8:
        return
    SUNOAPI_API_KEY = os.getenv("SUNOAPI_API_KEY")
    url = "https://api.sunoapi.org/api/v1/generate/record-info"
    headers = {"Authorization": f"Bearer {SUNOAPI_API_KEY}",}

    response = requests.get(url, headers=headers)
    if response.json()["data"]["status"] != "SUCCESS":
        time.sleep(15)
        poll(attempts=attempts+1)