from werkzeug.exceptions import HTTPException
from flask_assets import Environment, Bundle
from sqlalchemy.orm import DeclarativeBase
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from typing import Tuple, Dict
from flask_restful import Api
from datetime import datetime
from environs import Env

# -----------------------------------------------------------
# App bootstrap

env = Env()
env.read_env()

app = Flask(__name__, static_url_path='')

app.config.update(
    # Default config values that may be overwritten by environment values
    SECRET_KEY=env.str('SECRET_KEY'),
    SERVER_NAME=env.str('SERVER_NAME', default='localhost:8080'),
    PREFERRED_URL_SCHEME=env.str('PREFERRED_URL_SCHEME', default='http'),

    SENTRY_DSN=env.str('SENTRY_DSN', default=None),
    SENTRY_TRACES_SAMPLE_RATE=env.float('SENTRY_TRACES_SAMPLE_RATE', default=None),

    ASSETS_CACHE=env.str('ASSETS_CACHE', default='instance/webassets-cache'),

    DEBUG_TB_INTERCEPT_REDIRECTS=env.bool('DEBUG_TB_INTERCEPT_REDIRECTS', False),

    MINIFY_HTML=env.bool('MINIFY_HTML', default=False),

    COMPRESS_REGISTER=env.bool('COMPRESS_REGISTER', default=False),
    COMPRESS_MIN_SIZE=env.int('COMPRESS_MIN_SIZE', 512),

    SQLALCHEMY_DATABASE_URI=env.str('SQLALCHEMY_DATABASE_URI', default='sqlite:///db.sqlite'),

    SPOTIFY_CLIENT_ID=env.str('SPOTIFY_CLIENT_ID'),
    SPOTIFY_CLIENT_SECRET=env.str('SPOTIFY_CLIENT_SECRET'),

    # Config values that cannot be overwritten
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SESSION_PROTECTION='strong',
    BUNDLE_ERRORS=True,
)

# -----------------------------------------------------------
# Debugging-related behaviours

if app.config['DEBUG']:
    import logging

    logging.basicConfig(level=logging.DEBUG)
elif app.config['SENTRY_DSN']:
    try:
        from sentry_sdk.integrations.flask import FlaskIntegration
        import sentry_sdk

        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            integrations=[
                FlaskIntegration(),
            ],
            traces_sample_rate=app.config['SENTRY_TRACES_SAMPLE_RATE']
        )
    except ImportError:
        pass

# -----------------------------------------------------------
# Flask extensions initialization and configuration

# Flask-DebugToolbar
if app.config['DEBUG']:
    try:
        from flask_debugtoolbar import DebugToolbarExtension

        debug_toolbar = DebugToolbarExtension(app)
    except ImportError:
        pass

# Flask-Compress
try:
    from flask_compress import Compress

    compress = Compress(app)
except ImportError:
    pass

# Flask-HTMLmin
try:
    from flask_htmlmin import HTMLMIN

    htmlmin = HTMLMIN(app)
except ImportError:
    pass

# Flask-Assets
assets = Environment(app)
assets.append_path('assets')

assets.register('js_room', Bundle('js/utils.js', 'js/api.js', 'js/room.js', filters='jsmin', output='js/room.min.js'))
assets.register('css_app', Bundle('css/app.css', filters='cssutils', output='css/app.min.css'))


# Flask-SQLAlchemy
class AppDeclarativeBase(DeclarativeBase):
    pass


db = SQLAlchemy(app, model_class=AppDeclarativeBase)

import spotibox.models

# Flask-Migrate
migrate = Migrate(app, db)

# Flask-Login
login_manager = LoginManager(app)
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id: int):
    from spotibox.models import User

    return db.session.get(User, user_id)


# Flask-RESTful
api = Api(app, prefix='/api', catch_all_404s=True)

import spotibox.api.resources as api_resources

api.add_resource(api_resources.RoomCatalogResource, '/room/<spotify_id>/catalog')
api.add_resource(api_resources.RoomPlaybackResource, '/room/<spotify_id>/playback')
api.add_resource(api_resources.RoomPlaybackVolumeResource, '/room/<spotify_id>/playback/volume')
api.add_resource(api_resources.RoomQueueResource, '/room/<spotify_id>/queue')


# -----------------------------------------------------------
# Context processors

@app.context_processor
def context_processor() -> Dict:
    return {
        'current_year': datetime.now().year,
    }


# -----------------------------------------------------------
# Error pages

@app.errorhandler(HTTPException)
def http_error_handler(e: HTTPException) -> Tuple[str, int]:
    return render_template(
        'error.html',
        title=e.name,
        text=e.description,
    ), e.code


# -----------------------------------------------------------
# After-bootstrap imports

import spotibox.routes
