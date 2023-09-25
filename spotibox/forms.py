from flask_wtf import FlaskForm
from wtforms import StringField
import wtforms.validators as validators


class RoomForm(FlaskForm):
    room_name = StringField('Room name', [validators.DataRequired(), validators.Length(min=3)]) # TODO Must be unique
    room_password = StringField('Room password', [validators.Optional(), validators.Length(min=4)])
