from flask import render_template
from app import app


@app.route('/')
def home() -> str:
    return render_template('home.html')


@app.route('/host')
def host() -> str:
    return render_template('host.html')


@app.route('/join')
def join() -> str:
    return render_template('join.html')


@app.route('/<any(host,join):mode>/<room>')
def room(mode: str, room: str) -> str:
    return render_template('room.html')
