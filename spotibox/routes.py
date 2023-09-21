from flask import render_template, redirect, url_for
from werkzeug import Response
from typing import Union
from app import app


@app.route('/')
def home() -> str:
    return render_template('home.html')


@app.route('/authorize')
def authorize() -> Response:
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
