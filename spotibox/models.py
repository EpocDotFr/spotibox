from flask_login import UserMixin, current_user
from sqlalchemy.orm import mapped_column
from typing_extensions import Self
from flask import url_for, session
from datetime import datetime
from spotipy import Spotify
from typing import Optional
from app import db
import spotibox.exceptions as exceptions
import secrets


class TimestampedMixin:
    created_at = mapped_column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = mapped_column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(TimestampedMixin, UserMixin, db.Model):
    __tablename__ = 'users'

    spotify_id = mapped_column(db.String(255), primary_key=True)

    display_name = mapped_column(db.String(255), nullable=False)
    profile_image_url = mapped_column(db.String(255))
    access_token = mapped_column(db.JSON)
    room_password = mapped_column(db.String(30))
    access_granted_token = mapped_column(db.String(8))

    def get_id(self):
        return self.spotify_id

    def get_room_url(self, absolute: bool = False) -> str:
        return url_for('room', spotify_id=self.spotify_id, _external=absolute)

    def create_spotify_api_client(self) -> Spotify:
        from spotibox.spotify import create_spotipy_auth_manager, create_spotify_api_client

        return create_spotify_api_client(
            create_spotipy_auth_manager(self)
        )

    def grant_access(self):
        session[self.access_granted_key] = self.access_granted_token

    @property
    def is_active(self) -> bool:
        return self.is_authenticated_with_spotify

    @property
    def room_url(self) -> str:
        return self.get_room_url()

    @property
    def room_url_absolute(self) -> str:
        return self.get_room_url(True)

    @property
    def is_authenticated_with_spotify(self) -> bool:
        return bool(self.access_token)

    @property
    def is_room_private(self) -> bool:
        return bool(self.room_password)

    @property
    def is_current_user_room_owner(self) -> bool:
        return current_user.is_authenticated and current_user == self

    @property
    def has_current_user_access_to_room(self) -> bool:
        if self.is_room_private and not self.is_current_user_room_owner and not self.has_access_granted:
            return False

        return True

    @property
    def has_access_granted(self) -> bool:
        return session.get(self.access_granted_key) == self.access_granted_token

    @property
    def access_granted_key(self) -> str:
        return f'agk-{self.spotify_id}'

    @classmethod
    def get_by_spotify_id(cls: Self, spotify_id: str, checks: bool = True) -> Optional[Self]:
        user = db.session.get(cls, spotify_id)

        if not checks:
            return user

        if not user:
            raise exceptions.UserNotFoundException()

        if not user.is_authenticated_with_spotify:
            raise exceptions.UnauthenticatedWithSpotifyException()

        if not user.has_current_user_access_to_room:
            raise exceptions.PasswordRequiredException(user)

        return user

    def __repr__(self):
        return f'User:{self.spotify_id}'


@db.event.listens_for(User.room_password, 'set')
def user_room_password_set(user: User, value, oldvalue, initiator):
    if value:
        if value != oldvalue:
            user.access_granted_token = secrets.token_hex(4)
    else:
        user.access_granted_token = None
