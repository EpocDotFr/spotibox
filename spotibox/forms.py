from flask_wtf import FlaskForm
from wtforms import StringField
import wtforms.validators as validators


class RoomForm(FlaskForm):
    room_name = StringField('Room name', [validators.DataRequired()]) # TODO Must be unique, at least 3 chars
    room_password = StringField('Room password') # TODO At least 6 chars
