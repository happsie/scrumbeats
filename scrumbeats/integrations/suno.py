import requests
import time
import os
import json

# This class is just to manage the function calls to SunoAPI since its quite expensive. The LLM shouldn't call more than once, but cant be guaranteed. 
class SongCreator:
    def __init__(self):
        self._has_triggered_creation = False
    
    def create_song(self, lyrics: str, music_style: str, title: str):
        """
        Create a song based on a lyrics and genre

        Args: 
            - lyrics: The lyrics to create a song with
            - music_style: The music style to create the song with 
            - title: The song title
        """
        if self._has_triggered_creation:
            print('SunoAPI already triggered. Skipping execution')
            return
        
        self._has_triggered_creation = True

        print("Generating the song!")
        print(f"""
Title: {title}

Lyrics: {lyrics}

Style: {music_style}
        """)

        url = "https://api.sunoapi.org/api/v1/generate"
        payload = {
            "prompt": lyrics,
            "style": music_style,
            "title": title,
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

        SUNOAPI_API_KEY = os.getenv("SUNOAPI_API_KEY")
        headers = {
            "Authorization": f"Bearer {SUNOAPI_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.json()["msg"] != "success":
            print("could not generate song.", response.json())
            return {"status", "error"}
        
        songUrlOrNone = None
        for num in range(10):
            print(f"checking song generation, attempt {num}")
            songUrlOrNone = self.poll(response.json()["data"]["taskId"])
            if songUrlOrNone != None:
                break
            time.sleep(30)
            
        print(f"Song successfully generated: {songUrlOrNone}")

    def poll(self, taskId: str) -> str | None: 
        SUNOAPI_API_KEY = os.getenv("SUNOAPI_API_KEY")
        url = f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={taskId}"
        headers = {"Authorization": f"Bearer {SUNOAPI_API_KEY}",}

        response = requests.get(url, headers=headers).json()
        print(f"status: {response["data"]["status"]}")
        if response["data"]["status"] != "SUCCESS":
            return None
        else:
            return response["data"]["response"]["sunoData"]["audioUrl"]