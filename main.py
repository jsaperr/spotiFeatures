import subprocess
from time import sleep

# install spotipy module if it's not already installed
try:
    import spotipy
except ImportError:
    print("Installing Spotipy as it isn't already installed.")
    subprocess.check_call(["pip", "install", "spotipy"])
    import spotipy

    print("Installed Spotipy, script will work now.")

from spotipy.oauth2 import SpotifyOAuth

# set up the Spotify API credentials
client_id = "59acf1b17c394278a22f4a00b05d3959"
client_secret = "a7370266cffb4f47b674d421927b1feb"
redirect_uri = "http://localhost:8080/callback"
scope = "user-library-read playlist-modify-public"

# authenticate with the Spotify API

def liked_song_list(playlist_name):
    playlists = sp.current_user_playlists()['items']
    target_playlist = next((pl for pl in playlists if pl['name'] == playlist_name), None)

    if not target_playlist:
        print(f"Could not find playlist named '{playlist_name}' in your account.")
        liked_song_list()

    print("getting and adding liked songs")
    # get all of the user's liked tracks
    liked_tracks = []
    results = sp.current_user_saved_tracks()
    liked_tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        liked_tracks.extend(results['items'])

    # filter out tracks that are already on the target playlist
    playlist_tracks = []
    results = sp.playlist_items(target_playlist['id'])
    playlist_tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        playlist_tracks.extend(results['items'])

    playlist_track_uris = set(track['track']['uri'] for track in playlist_tracks)
    liked_track_uris = set(track['track']['uri'] for track in liked_tracks)
    new_track_uris = list(liked_track_uris - playlist_track_uris)

    if len(new_track_uris) == 0:
        print(f"All liked tracks are already on playlist '{playlist_name}'!")
        exit()

    # add each new liked track to the target playlist in batches of 100
    total_tracks_added = 0
    for i in range(0, len(new_track_uris), 100):
        track_uris = new_track_uris[i:i + 100]
        sp.user_playlist_add_tracks(user=sp.current_user()['id'], playlist_id=target_playlist['id'], tracks=track_uris)
        total_tracks_added += len(track_uris)

    print(f"Added {total_tracks_added} new tracks to playlist '{playlist_name}'!")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path=".spotifycache",
        open_browser=False
    )
)
name = input("playlist name: ")
while True:
    liked_song_list(name)
    sleep(600)
