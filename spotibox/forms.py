from wtforms import StringField, PasswordField
from spotibox.models import User
from flask_wtf import FlaskForm
import wtforms.validators as validators

ROOM_PASSWORD_LENGTH_VALIDATOR = validators.Length(min=4, max=30)


class RoomSettingsForm(FlaskForm):
    room_password = StringField('Room password', [validators.Optional(), ROOM_PASSWORD_LENGTH_VALIDATOR])

    def populate_user(self, user: User):
        user.room_password = self.room_password.data


class RoomPasswordForm(FlaskForm):
    room_password = PasswordField('Room password', [validators.DataRequired(), ROOM_PASSWORD_LENGTH_VALIDATOR])
