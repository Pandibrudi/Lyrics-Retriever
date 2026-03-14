import sys
from get_lyrics import get_songs

def main():
    artist_argument = sys.argv[1]
    if artist_argument != None:
        get_songs(artist_argument)

if __name__ == "__main__":
    main()