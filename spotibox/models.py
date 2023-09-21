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


class Room(TimestampedMixin, db.Model):
    __tablename__ = 'rooms'

    id = mapped_column(db.Integer, primary_key=True, autoincrement=True)

    name = mapped_column(db.String, nullable=False)
    password = mapped_column(db.String, nullable=False)

    user_id = mapped_column(db.Integer, ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='rooms')
