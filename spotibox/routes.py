from flask import render_template, redirect, url_for, request, flash, abort
from spotibox.spotify import create_auth_manager, create_api_client
from flask_login import current_user, login_user, logout_user
from spotibox.models import User
from sqlalchemy import select
from werkzeug import Response
from app import app, db


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

            return redirect(url_for('home'))

        try:
            client = create_api_client(auth_manager)

            user_info = client.me()
        except Exception:
            app.logger.exception('Failed to get Spotify account information')

            if not app.config['DEBUG'] and app.config['SENTRY_DSN']:
                import sentry_sdk

                sentry_sdk.capture_exception()

            flash(f'Failed to get Spotify account information.', 'danger')

            return redirect(url_for('home'))

        if user_info['product'] != 'premium':
            flash('Sorry, you must have a Spotify Premium subscription to use Spotibox.')

            return redirect(url_for('home'))

        user = db.session.scalar(select(User).where(User.spotify_id == user_info['id']))

        if not user:
            user = User()
            user.spotify_id = user_info['id']

        user.display_name = user_info['display_name']
        user.profile_image_url = user_info['images'][0]['url'] if user_info['images'] else None # TODO Use the smallest one (>= 32 px)
        user.access_token = 'todo' # TODO
        user.refresh_token = 'todo' # TODO

        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)

        flash('Successfully logged in.', 'success')
    elif error:
        if error == 'access_denied':
            flash('You did not authorize Spotibox to access your Spotify account.', 'warning')
        else:
            flash(f'Got error code "{error}" from Spotify.', 'warning')
    else:
        abort(400)

    return redirect(url_for('home'))


@app.route('/sign-out')
def sign_out() -> Response:
    current_user.access_token = None
    current_user.refresh_token = None

    db.session.add(current_user)
    db.session.commit()

    logout_user()

    flash('You are now signed out.', 'success')

    return redirect(url_for('home'))


@app.route('/rooms')
def rooms() -> str:
    return render_template('rooms/list.html')


@app.route('/rooms/<room_name>')
def room(room_name: str) -> str:
    return render_template('rooms/details.html')
