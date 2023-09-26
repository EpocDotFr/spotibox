from wtforms.validators import ValidationError
from spotibox.models import User
from flask_wtf import FlaskForm
from wtforms import StringField
from sqlalchemy import select
from app import db
import wtforms.validators as validators

ROOM_NAME_REGEX = r'^[a-zA-Z0-9\-_\+]+$'


class RoomForm(FlaskForm):
    room_name = StringField('Room name', [validators.DataRequired(), validators.Length(min=3, max=80), validators.Regexp(ROOM_NAME_REGEX, message='Please use the following characters only: alphabetic, numeric and - _ +')])
    room_password = StringField('Room password', [validators.Optional(), validators.Length(min=4, max=30)])

    def validate_room_name(form, field):
        if db.session.scalar(select(User).where(User.room_name == field.data)): # TODO Use count; validation only if field value has changed
            raise ValidationError('Please use a different room name.')

    def populate_user(self, user: User):
        user.room_name = self.room_name.data
        user.room_password = self.room_password.data
