import requests
import time
import os

# This class is just to manage the function calls to SunoAPI since its quite expensive. The LLM shouldn't call more than once, but cant be guaranteed. 
class SongCreator:
    def __init__(self):
        self._has_triggered_creation = False
    
    def create_song(self, lyrics: str, genre: str, title: str):
        """
        Create a song based on a lyrics and genre

        Args: 
            - lyrics: The lyrics to create a song with
            - Genre: The genre to create the song with 
            - title: The song title
        """
        if self._has_triggered_creation:
            return
        
        self._has_triggered_creation = True

        print("Creating a song!")
        print(lyrics, genre, title)

        url = "https://api.sunoapi.org/api/v1/generate"
        payload = {
            "prompt": lyrics,
            "style": genre,
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
        
        self.poll(response.json()["data"]["taskId"], 0)
        return {"status": "success"}

    def poll(self, taskId: str, attempts: int): 
        if attempts >= 8:
            return
        SUNOAPI_API_KEY = os.getenv("SUNOAPI_API_KEY")
        url = f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={taskId}"
        headers = {"Authorization": f"Bearer {SUNOAPI_API_KEY}",}

        response = requests.get(url, headers=headers)
        print(response, response.json()["data"]["status"])
        if response.json()["data"]["status"] != "SUCCESS":
            time.sleep(15)
            self.poll(taskId=taskId, attempts=attempts+1)