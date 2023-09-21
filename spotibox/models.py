from sqlalchemy.orm import mapped_column
from sqlalchemy_utils import ArrowType
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from app import db
import arrow


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = mapped_column(db.Integer, primary_key=True, autoincrement=True)

    spotify_id = mapped_column(db.String, nullable=False, unique=True)
    display_name = mapped_column(db.String, nullable=False)
    profile_image_url = mapped_column(db.String)
    access_token = mapped_column(db.String)
    refresh_token = mapped_column(db.String)
    created_at = mapped_column(ArrowType, default=lambda: arrow.utcnow().floor('minute'), nullable=False)
    updated_at = mapped_column(ArrowType, default=lambda: arrow.utcnow().floor('minute'), onupdate=lambda: arrow.utcnow().floor('minute'), nullable=False)

    rooms = db.relationship('Room', back_populates='user')


class Room(db.Model):
    __tablename__ = 'rooms'

    id = mapped_column(db.Integer, primary_key=True, autoincrement=True)

    name = mapped_column(db.String, nullable=False)
    password = mapped_column(db.String, nullable=False)
    created_at = mapped_column(ArrowType, default=lambda: arrow.utcnow().floor('minute'), nullable=False)
    updated_at = mapped_column(ArrowType, default=lambda: arrow.utcnow().floor('minute'), onupdate=lambda: arrow.utcnow().floor('minute'), nullable=False)

    user_id = mapped_column(db.Integer, ForeignKey('users.id'))

    user = db.relationship('User', back_populates='rooms')
