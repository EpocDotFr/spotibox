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


@app.route('/authorize-callback')
def authorize_callback() -> Response:
    return redirect(url_for('home'))


@app.route('/sign-out')
def sign_out() -> Response:
    return redirect(url_for('home'))


@app.route('/rooms')
def public_rooms() -> str:
    return render_template('rooms/list_public.html')


@app.route('/rooms/<room_name>')
def room(room_name: str) -> str:
    return render_template('rooms/details.html')


@app.route('/my-rooms')
def my_rooms() -> str:
    return render_template('rooms/list_mine.html')


@app.route('/my-rooms/create')
def create_room() -> Union[str, Response]:
    return render_template('rooms/create.html')


@app.route('/my-rooms/<int:room_id>/edit')
def edit_room(room_id: int) -> Union[str, Response]:
    return render_template('rooms/edit.html')


@app.route('/my-rooms/<int:room_id>/delete')
def delete_room(room_id: int) -> Response:
    return redirect(url_for('my_rooms'))
