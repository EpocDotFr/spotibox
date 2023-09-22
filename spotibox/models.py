from sqlalchemy.orm import mapped_column
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from datetime import datetime
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
    access_token = mapped_column(db.String)
    refresh_token = mapped_column(db.String)

    rooms = db.relationship('Room', back_populates='user')

    @property
    def is_connected_to_spotify(self) -> bool:
        return self.access_token and self.refresh_token

    def disconnect_from_spotify(self):
        self.access_token = None
        self.refresh_token = None


class Room(TimestampedMixin, db.Model):
    __tablename__ = 'rooms'

    id = mapped_column(db.Integer, primary_key=True, autoincrement=True)

    name = mapped_column(db.String, nullable=False, unique=True)
    password = mapped_column(db.String)

    user_id = mapped_column(db.Integer, ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='rooms')

    @property
    def is_private(self) -> bool:
        return bool(self.password)

    @property
    def is_public(self) -> bool:
        return not self.is_private
