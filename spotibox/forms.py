from spotibox.models import User
from flask_wtf import FlaskForm
from wtforms import StringField
import wtforms.validators as validators


class RoomForm(FlaskForm):
    room_password = StringField('Room password', [validators.Optional(), validators.Length(min=4, max=30)])

    def populate_user(self, user: User):
        user.room_password = self.room_password.data
