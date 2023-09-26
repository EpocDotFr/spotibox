from spotibox.models import User
from flask_wtf import FlaskForm
from wtforms import StringField
import wtforms.validators as validators


class RoomForm(FlaskForm):
    room_name = StringField('Room name', [validators.DataRequired(), validators.Length(min=3, max=80)]) # TODO Must be unique
    room_password = StringField('Room password', [validators.Optional(), validators.Length(min=4, max=30)])

    def populate_user(self, user: User):
        user.room_name = self.room_name.data
        user.room_password = self.room_password.data
