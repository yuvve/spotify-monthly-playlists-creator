# spotify-monthly-playlists-creator
An alternative to the [IFTTT automation (that now requires pro subscription) "Add saved songs to a monthly playlist"](https://ifttt.com/applets/rC5QtGu6-add-saved-songs-to-a-monthly-playlist). You must manually run this script periodically.
## Functionality
This script will go X days backwards (it will ask you when you run it) in your saved songs list (favorites), and then place all songs it found into playlists (without allowing duplicates) in the format "Month 'yy" (i.e. "December '22") - creating the playlists if they do not exist.

Notice that preventing duplicates is done by the track ID, so there might be duplicates by name (as long as they are from different tracks).
## How to setup
1. Install Python.
2. Clone the repo.
3. `pip install -r requirements.txt`
4. Create a [Spotify app](https://developer.spotify.com/) with redirect url: "http://google.com" (or any fake url you want).
5. Change the name of `.env-example` to `.env`, and fill it using the Spotify developer dashboard.
## How to run
Just run the program and let it authenticate (don't forget to copy the url and paste it in the terminal). It will then ask you how many days back to look, and you will also have to answer y/n before tracks are inserted to a playlist (once for each playlist). 