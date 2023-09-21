from flask import render_template, redirect, url_for
from spotibox.spotify import create_auth_manager
from flask_login import current_user
from werkzeug import Response
from typing import Union
from app import app


@app.route('/')
def home() -> str:
    if current_user.is_authenticated:
        data = {}
    else:
        auth_manager = create_auth_manager()

        data = {
            'sign_in_spotify_url': auth_manager.get_authorize_url() # TODO state
        }

    return render_template('home.html', **data)


@app.route('/authorize')
def authorize() -> Response:
    return redirect(url_for('home'))


@app.route('/sign-out')
def sign_out() -> Response:
    return redirect(url_for('home'))


@app.route('/rooms')
def public_rooms() -> str:
    return ''


@app.route('/rooms/<room_name>')
def room(room_name: str) -> str:
    return render_template('room.html')


@app.route('/my-rooms')
def my_rooms() -> str:
    return ''


@app.route('/my-rooms/create')
def create_room() -> Union[str, Response]:
    return ''


@app.route('/my-rooms/<room_id>/delete')
def delete_room(room_id: id) -> Response:
    return redirect(url_for('my_rooms'))
