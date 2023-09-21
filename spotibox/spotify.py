from spotipy import Spotify, SpotifyOAuth
from flask import url_for
from app import app

SCOPES = (
    'user-read-private',
    'streaming',
    'user-modify-playback-state'
)

def create_auth_manager() -> SpotifyOAuth:
    return SpotifyOAuth(
        client_id=app.config['SPOTIFY_CLIENT_ID'],
        client_secret=app.config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri=url_for('authorize', _external=True),
        scope=SCOPES,
        open_browser=False
    )


def create_api_client(auth_manager: SpotifyOAuth) -> Spotify:
    return Spotify(auth_manager=auth_manager)
