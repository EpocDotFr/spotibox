from flask import render_template
from app import app, auth


@app.route('/')
@auth.login_required()
def home() -> str:
    return render_template('home.html')
