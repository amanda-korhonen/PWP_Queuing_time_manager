'''Initializes the queuinghub Flask application.'''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    '''Create and configure the Flask application.'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "queuing.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from queuinghub import database
    from queuinghub import api
    from queuinghub.utils import PlaceConverter, QueueConverter
    app.cli.add_command(database.init_db_command)
    #app.cli.add_command(database.generate_test_data)
    app.url_map.converters["place"] = PlaceConverter
    app.url_map.converters["queue"] = QueueConverter
    app.register_blueprint(api.api_bp)

    return app
