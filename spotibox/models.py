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
    room_name = mapped_column(db.String, nullable=False, unique=True)
    room_password = mapped_column(db.String)

    @property
    def is_room_private(self) -> bool:
        return bool(self.room_password)

    @property
    def is_room_public(self) -> bool:
        return not self.is_room_private
