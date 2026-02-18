import requests
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://ddc.chrisdonahue.com/choreograph"
class Levels:
    beginner = "Beginner"
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"
    challenge = "Challenge"

def get_sm(song, artist, diff_coarse):
    data = {
        "song_artist": artist,
        "song_title": song,
        "diff_coarse": diff_coarse,
    }
    files = {"audio_file": ("file.ogg", open("work/file.ogg", "rb"), "audio/ogg")}
    
    print(f"Start DDC downloading: {diff_coarse}")
    with requests.post(BASE_URL, data=data, files=files, stream=True) as response:
        response.raise_for_status()
        name = f"work/{diff_coarse}.zip"
        with open(name, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"End DDC download: {diff_coarse}")


def ddc(song, artist):
    with ThreadPoolExecutor() as executor:
        futures = []
        for level in (
        Levels.beginner,
        Levels.easy,
        Levels.medium,
        Levels.hard,
        Levels.challenge,
    ):
            futures.append(
                executor.submit(
                get_sm,
                song,
                artist, 
                level
                )
            )

        [future.result() for future in futures]
            
    








  