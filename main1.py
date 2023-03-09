import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up the Spotify API client
scope = "user-library-read playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id="59acf1b17c394278a22f4a00b05d3959",
                                               client_secret="a7370266cffb4f47b674d421927b1feb",
                                               redirect_uri="http://localhost:8080/callback"))

# Specify the ID of the playlist you want to add songs to
playlist_id = "7rw2tqZQ9u9z9F4t5v4Sfq"

# Get the user's most recently added tracks
results = sp.current_user_saved_tracks(limit=50, offset=0)
tracks = [item["track"]["id"] for item in results["items"]]

# Add any new tracks to the playlist
playlist_tracks = sp.playlist_tracks(playlist_id)["items"]
playlist_track_ids = [item["track"]["id"] for item in playlist_tracks]
new_track_ids = list(set(tracks) - set(playlist_track_ids))
if len(new_track_ids) > 0:
    sp.playlist_add_items(playlist_id, new_track_ids)
    print(f"Added {len(new_track_ids)} new tracks to the playlist!")

# Continuously monitor for new liked songs
while True:
    # Get the user's most recently added tracks
    results = sp.current_user_saved_tracks(limit=50, offset=0)
    tracks = [item["track"]["id"] for item in results["items"]]

    # Add any new tracks to the playlist
    playlist_tracks = sp.playlist_tracks(playlist_id)["items"]
    playlist_track_ids = [item["track"]["id"] for item in playlist_tracks]
    new_track_ids = list(set(tracks) - set(playlist_track_ids))
    if len(new_track_ids) > 0:
        sp.playlist_add_items(playlist_id, new_track_ids)
        print(f"Added {len(new_track_ids)} new tracks to the playlist!")

    # Wait for a specified amount of time before checking again
    time.sleep(2)
