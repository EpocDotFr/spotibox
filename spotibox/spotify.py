from spotipy import Spotify, SpotifyOAuth
from flask import url_for
from app import app

SCOPES = (
    'user-read-private',
    'streaming',
    'user-modify-playback-state'
)


def create_api_client() -> Spotify:
    return Spotify(auth_manager=SpotifyOAuth(
        client_id=app.config['SPOTIFY_CLIENT_ID'],
        client_secret=app.config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri=url_for('host'),
        scope=SCOPES,
        open_browser=False
    ))
