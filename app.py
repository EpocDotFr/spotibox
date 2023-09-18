from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, abort
from werkzeug.exceptions import HTTPException
from flask_assets import Environment, Bundle
from flask_httpauth import HTTPBasicAuth
from typing import Tuple, Optional
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

    AUTH_USERNAME=env.str('AUTH_USERNAME'),
    AUTH_PASSWORD=generate_password_hash(env.str('AUTH_PASSWORD')),
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

assets.register('css_app', Bundle('css/app.css', filters='cssutils', output='css/app.min.css'))
assets.register('js_app', Bundle('js/app.js', filters='jsmin', output='js/app.min.js'))

# Flask-HTTPAuth
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str) -> Optional[str]:
    if username == app.config['AUTH_USERNAME'] and check_password_hash(app.config['AUTH_PASSWORD'], password):
        return username

    return None


@auth.error_handler
def auth_error(status: int) -> Tuple[str, int]:
    try:
        abort(status)
    except HTTPException as e:
        return http_error_handler(e)


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
