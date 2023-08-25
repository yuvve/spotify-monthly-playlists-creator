import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from auxiliary_functions import get_starting_date_from_user
from spotify_functions import(
    get_latest_saved_tracks,
    get_playlists,
    insert_to_playlists
)

def main():
    #logging.basicConfig(level=logging.INFO)

    scope = "user-library-read playlist-read-private playlist-modify-private"
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    last_timestamp = get_starting_date_from_user()
    tracks = get_latest_saved_tracks(spotify, last_timestamp)
    playlists = get_playlists(spotify, tracks)
    insert_to_playlists(spotify, tracks, playlists)

if __name__ == "__main__":
    main()
