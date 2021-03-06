from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk
from os import environ
from .config import config_by_name
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
ma = Marshmallow()


def create_app(config_name):
    sentry_sdk.init(
        environment=config_name,
        dsn=environ.get('URL_SENTRY', "https://e82e369284cf4b30953d4499e230d9a6@o464193.ingest.sentry.io/5471563"),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    ma.init_app(app)
    flask_bcrypt.init_app(app)
    return app
