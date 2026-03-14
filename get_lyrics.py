import lyricsgenius
import time
import re
from decouple import config
from get_albums import get_all_albums

# A Genius access token can be generated after signing up at https://genius.com
ACCESS_TOKEN = config("CLIENT_ACCESS_TOKEN")
BASE_URL = "https://api.genius.com/"

genius = lyricsgenius.Genius(ACCESS_TOKEN, timeout=20, retries=3, sleep_time=1)

def safe_filename(name):
    # Replace invalid characters with underscore
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def get_songs(artist_name):
    all_albums = get_all_albums(artist_name)

    for a in all_albums:
        print(a)
        time.sleep(5) # to avoid time out errors
        album = genius.search_album(a[1], artist_name)
        album = album.to_dict()
        for track in album["tracks"]:
            title = track["song"]["title"]
            year = str(a[0])
            album_name = a[1]
            filename = f"{artist_name}_{year}_{album_name}_{title}"
            filename = safe_filename(filename) + ".txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(track["song"]["lyrics"])

    return all_albums

(print(get_songs("Taylor Swift")))