import lyricsgenius
import requests
from decouple import config

# A Genius access token can be generated after signing up at https://genius.com
ACCESS_TOKEN = config("CLIENT_ACCESS_TOKEN")
BASE_URL = "https://api.genius.com/"

genius = lyricsgenius.Genius(ACCESS_TOKEN, timeout=20, retries=3, sleep_time=1)

# retrieves the base info of simple search call to the API returning data about songs and artist
def get_artist_info(artist_name):
    base_url = BASE_URL
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
    search_url = base_url + 'search'
    data = {'q': artist_name}
    response = requests.get(search_url, params=data, headers=headers)    

    return response

# checking the base info for Genius artist id
def get_artist_id(artist_name):
    info = get_artist_info(artist_name)
    
    info = info.json()

    artist_id = info["response"]["hits"][0]["result"]["primary_artist"]["id"]

    return artist_id

# trying to retrieve all albums of one artist using the id
def get_all_albums(artist_name):
    artist_id = get_artist_id(artist_name)

    all_albums = []

    page = 1

    albums = genius.artist_albums(artist_id, per_page=50, page=None)

    for a in albums["albums"]:
        all_albums.append((a["release_date_components"]["year"], a["name"]))

    # doing the same until there are no pages left
    while albums["next_page"] != None:
        try:
            page += 1
            albums = genius.artist_albums(artist_id, per_page=50, page=page)
            for a in albums["albums"]:
                all_albums.append((a["release_date_components"]["year"], a["name"]))
        # some faulty data seems to have no release date
        except TypeError:
            print("Skipped album without release date.")
    # Returns also special editions which could considered duplicates but the idea is to catch even every bonus track
    sorted_by_date = sorted(all_albums)

    return sorted_by_date

# SAMPLE CALL
# print(get_all_albums("Lana del Rey"))
