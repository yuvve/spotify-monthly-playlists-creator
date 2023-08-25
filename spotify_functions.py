"""Batch jobs for Spotify API"""
import logging
from ordered_set import OrderedSet
from auxiliary_functions import string_to_datetime, datetime_to_playlist_name

RESULTS_TRACK_LIMIT = 20
RESULTS_PLAYLIST_LIMIT = 50
RESULTS_TRACKS_PER_PLAYLIST_LIMIT = 100

def get_latest_saved_tracks(spotify, latest_checked):
    """Gets all saved tracks that were saved at a datetime later than latest_checked

    :param spotify: a Spotify object (from spotipy package)
    :param latest_checked: a datetime object
    """

    offset = 0
    tracks = []
    results = spotify.current_user_saved_tracks(limit=RESULTS_TRACK_LIMIT, offset=offset)
    if not results:
        return []
    earliest_date_found = string_to_datetime(results['items'][-1]['added_at'])

    while results and earliest_date_found > latest_checked:
        offset += RESULTS_TRACK_LIMIT
        tracks.extend(results['items'])
        earliest_date_found = string_to_datetime(results['items'][-1]['added_at'])
        results = spotify.current_user_saved_tracks(limit=RESULTS_TRACK_LIMIT, offset=offset)

    tracks.extend(results['items'])

    for item in reversed(tracks):
        if string_to_datetime(item['added_at']) <= latest_checked:
            tracks.pop() # Remember that tracks is ordered after added_at time
        else:
            break

    print(f"Found {len(tracks)} new saved tracks since {latest_checked}!")

    return tracks

def get_playlists(spotify, tracks):
    """Gets or creates monthly playlists for the track list
    in the predefined format, based on their "added_at" time.

    :param spotify: a Spotify object (from spotipy package)
    :param tracks: a list of tracks
    :returns: a dictionary of playlists in the format {name:id}
    """

    needed_playlists = OrderedSet(
        [datetime_to_playlist_name(string_to_datetime(track['added_at']))
        for track in tracks])

    logging.info("We need a total of %i playlists", len(needed_playlists))

    offset = 0
    current_user_playlists = []
    found_playlists = spotify.current_user_playlists(
        limit=RESULTS_PLAYLIST_LIMIT, offset = offset)
    while found_playlists['items']:
        offset += RESULTS_PLAYLIST_LIMIT
        current_user_playlists.extend(found_playlists['items'])
        found_playlists = spotify.current_user_playlists(
            limit=RESULTS_PLAYLIST_LIMIT, offset = offset)

    existing_playlists = { # Might cause problems for duplicate list names...
        playlist['name']:playlist['id'] for playlist in current_user_playlists
    }

    results = {}
    for needed in needed_playlists:
        if needed in existing_playlists.keys():
            results[needed] = existing_playlists[needed]
            logging.info("The playlist %s already exists!", needed)
        else:
            new_playlist = spotify.user_playlist_create(
                user = spotify.me()['id'],
                name = needed,
                public=False,
                collaborative=False,
                description='')
            results[needed] = new_playlist['id']
            print(f"Created the playlist {needed}!")

    return results

def insert_to_playlists(spotify, tracks, playlists):
    """Insert tracks into monthly playlists

    :param spotify: a Spotify object (from spotipy package)
    :param tracks: a list of tracks
    :param playlists: a list of monthly playlists
    """

    combined_dict = {
        playlist_name:{"playlist_id":playlists[playlist_name],"track_ids":[],"track_names":[]}
        for playlist_name in playlists.keys()
    }

    for track in tracks:
        track_added_at = datetime_to_playlist_name(string_to_datetime(track['added_at']))
        combined_dict[track_added_at]['track_ids'].append(track['track']['id'])
        combined_dict[track_added_at]['track_names'].append(track['track']['name'])

    for k,v in combined_dict.items():
        offset = 0
        curr_list_tracks = []
        fetched_tracks = spotify.playlist_items(
            v['playlist_id'], limit=RESULTS_TRACKS_PER_PLAYLIST_LIMIT, offset=offset)
        while fetched_tracks['items']:
            offset += RESULTS_TRACKS_PER_PLAYLIST_LIMIT
            curr_list_tracks.extend([item['track']['id'] for item in fetched_tracks['items']])
            fetched_tracks = spotify.playlist_items(
                v['playlist_id'], limit=RESULTS_TRACKS_PER_PLAYLIST_LIMIT, offset=offset)

        tracks_to_insert = []
        for i, track_id in enumerate(v['track_ids']):
            if track_id not in curr_list_tracks:
                tracks_to_insert.append(track_id)
                logging.info("Will inserted %s (%s) into %s!",
                            combined_dict[k]['track_names'][i], track_id, k)
            else:
                logging.info("Will not insert %s (%s) into %s, since it already exists there!",
                            combined_dict[k]['track_names'][i], track_id, k)

        if tracks_to_insert:
            yes_no = ""
            while yes_no.lower() not in ['n','y']:
                yes_no = input(f"Insert {len(tracks_to_insert)} tracks into {k}, y/n?")[0]

            if yes_no.lower() == 'y':
                spotify.playlist_add_items(v['playlist_id'],tracks_to_insert)
                print(f"Inserted {len(tracks_to_insert)} tracks into {k}!")
            else:
                print(f"Did not insert any tracks into {k}!")
        else:
            print(f"0 tracks to insert into {k}!")
