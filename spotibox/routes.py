from flask import render_template
from app import app, auth


@app.route('/')
@auth.login_required()
def home() -> str:
    return render_template('home.html')


@app.route('/host')
@auth.login_required()
def host() -> str:
    return render_template('host.html')


@app.route('/listen')
@auth.login_required()
def listen() -> str:
    return render_template('listen.html')


@app.route('/<any(host,listen):mode>/<room>')
@auth.login_required()
def room(mode: str, room: str) -> str:
    return render_template('room.html')
