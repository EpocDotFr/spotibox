from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from spotibox.spotify import create_auth_manager
from spotibox.models import User
from werkzeug import Response
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
    code = request.args.get('code')
    error = request.args.get('error')

    if code:
        auth_manager = create_auth_manager()

        try:
            auth_manager.get_access_token(code)
        except Exception:
            app.logger.exception('Failed to get access token from Spotify')

            if not app.config['DEBUG'] and app.config['SENTRY_DSN']:
                import sentry_sdk

                sentry_sdk.capture_exception()

            flash(f'Failed to get access token from Spotify.', 'danger')

        # TODO récup infos user
        # TODO Créer ou mettre à jour user

        # login_user(user, remember=True)

        flash('Successfully logged in.', 'success')
    elif error:
        if error == 'access_denied':
            flash('You did not authorize Spotibox to access your Spotify account.', 'danger')
        else:
            flash(f'Got error code "{error}" from Spotify.', 'danger')

    return redirect(url_for('home'))


@app.route('/sign-out')
def sign_out() -> Response:
    # TODO access_token et refresh_token à null

    logout_user()

    flash('You are now signed out.', 'success')

    return redirect(url_for('home'))


@app.route('/rooms')
def rooms() -> str:
    return render_template('rooms/list.html')


@app.route('/rooms/<room_name>')
def room(room_name: str) -> str:
    return render_template('rooms/details.html')
