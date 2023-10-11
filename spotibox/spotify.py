from spotipy import Spotify, SpotifyOAuth, CacheHandler, FlaskSessionCacheHandler
from flask import url_for, session
from typing import Dict, Optional
from spotibox.models import User
from app import app, db

SCOPES = (
    'user-read-private',
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    # 'streaming',
)


class DatabaseUserCacheHandler(CacheHandler):
    user: User

    def __init__(self, user: User):
        self.user = user

    def get_cached_token(self) -> Optional[Dict]:
        return self.user.access_token

    def save_token_to_cache(self, token_info: Dict):
        self.user.access_token = token_info

        db.session.add(self.user)
        db.session.commit()


def create_spotipy_auth_manager(user: Optional[User] = None) -> SpotifyOAuth:
    cache_handler = DatabaseUserCacheHandler(user) if isinstance(user, User) else FlaskSessionCacheHandler(session)

    return SpotifyOAuth(
        client_id=app.config['SPOTIFY_CLIENT_ID'],
        client_secret=app.config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri=url_for('authorize_callback', _external=True),
        scope=SCOPES,
        open_browser=False,
        cache_handler=cache_handler
    )


def create_spotify_api_client(auth_manager: SpotifyOAuth) -> Spotify:
    return Spotify(auth_manager=auth_manager)
