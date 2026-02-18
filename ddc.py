import requests

BASE_URL = "https://ddc.chrisdonahue.com/choreograph"

class Levels:
    beginner = "Beginner"
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"
    challenge = "Challenge"

def send(diff_coarse):
    data = {
        "song_artist": "Sia",
        "song_title": "Cheap Thrills",
        "diff_coarse": diff_coarse,
    }
    files = {"audio_file": ("file.ogg", open("work/file.ogg", "rb"), "audio/ogg")}
    
    with requests.post(BASE_URL, data=data, files=files, stream=True) as response:
        print("Status:", response.status_code)

        response.raise_for_status()

        with open(f"work/{diff_coarse}.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("ZIP salvo como resultado.zip 🎉")


def ddc():
    for level in (
        Levels.beginner,
        Levels.easy,
        Levels.medium,
        Levels.hard,
        Levels.challenge,
    ):
        send(level)
