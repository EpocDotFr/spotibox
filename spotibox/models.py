from sqlalchemy.orm import mapped_column
from flask_login import UserMixin
from datetime import datetime
from flask import url_for
from app import db


class TimestampedMixin:
    created_at = mapped_column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = mapped_column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(TimestampedMixin, UserMixin, db.Model):
    __tablename__ = 'users'

    id = mapped_column(db.Integer, primary_key=True, autoincrement=True)

    spotify_id = mapped_column(db.String, nullable=False, unique=True)
    display_name = mapped_column(db.String)
    profile_image_url = mapped_column(db.String)
    access_token = mapped_column(db.JSON)
    room_password = mapped_column(db.String(30))

    def build_room_url(self, absolute: bool = False) -> str:
        return url_for('room', spotify_id=self.spotify_id, _external=absolute)

    @property
    def room_url(self) -> str:
        return self.build_room_url()

    @property
    def room_url_absolute(self) -> str:
        return self.build_room_url(True)

    @property
    def is_authenticated_with_spotify(self) -> bool:
        return bool(self.access_token)

    @property
    def is_room_private(self) -> bool:
        return bool(self.room_password)

    @property
    def is_room_active(self) -> bool:
        return self.is_authenticated_with_spotify
