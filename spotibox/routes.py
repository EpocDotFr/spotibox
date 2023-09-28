from flask import render_template, redirect, url_for, request, flash, abort, session
from flask_login import current_user, login_user, logout_user, login_required
from spotibox.spotify import create_auth_manager, create_api_client
from spotibox.forms import RoomForm
from spotibox.models import User
from sqlalchemy import select
from werkzeug import Response
from typing import Union
from app import app, db


@app.route('/', methods=['GET', 'POST'])
def home() -> Union[str, Response]:
    if current_user.is_authenticated:
        form = RoomForm(obj=current_user)

        if form.validate_on_submit():
            form.populate_user(current_user)

            db.session.add(current_user)
            db.session.commit()

            flash('Your room\'s settings have been saved.', 'success')

            return redirect(url_for('home'))

        data = {
            'form': form
        }
    else:
        data = {
            'sign_in_spotify_url': create_auth_manager().get_authorize_url()
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

            flash('Sorry, there was an error while authenticating with Spotify.', 'danger')

            return redirect(url_for('home'))

        try:
            client = create_api_client(auth_manager)

            user_info = client.me()
        except Exception:
            app.logger.exception('Failed to get Spotify account information')

            if not app.config['DEBUG'] and app.config['SENTRY_DSN']:
                import sentry_sdk

                sentry_sdk.capture_exception()

            flash('Sorry, there was an error while getting your Spotify account information.', 'danger')

            return redirect(url_for('home'))

        if user_info['product'] != 'premium':
            flash('Sorry, you must have a Spotify Premium subscription to use Spotibox.', 'warning')

            return redirect(url_for('home'))

        user = db.session.scalar(select(User).where(User.spotify_id == user_info['id']))
        new_user = False

        if not user:
            user = User()
            user.spotify_id = user_info['id']

            new_user = True

        user.display_name = user_info['display_name']
        user.access_token = session.pop('token_info', None)

        if not user.access_token:
            flash('Sorry, there was a technical error (empty access token after authorization).', 'danger')

            return redirect(url_for('home'))

        if user_info['images']:
            user_info['images'].sort(key=lambda i: i['height'])

            user.profile_image_url = user_info['images'][0]['url']

        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)

        flash('Welcome{}, {}.'.format(' back' if not new_user else '', user.display_name), 'success')
    elif error:
        if error == 'access_denied':
            flash('You did not authorize Spotibox to access your Spotify account.', 'warning')
        else:
            flash(f'Got error code "{error}" from Spotify.', 'warning')
    else:
        abort(400)

    return redirect(url_for('home'))


@app.route('/sign-out')
@login_required
def sign_out() -> Response:
    current_user.access_token = None

    db.session.add(current_user)
    db.session.commit()

    flash(f'See you later, {current_user.display_name}.', 'success')

    logout_user()

    return redirect(url_for('home'))


@app.route('/rooms')
def rooms() -> str:
    abort(404) # TODO

    return render_template('rooms.html')


@app.route('/room/<spotify_id>')
def room(spotify_id: str) -> str:
    return render_template('room.html')
