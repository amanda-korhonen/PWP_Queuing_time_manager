'''
Initializes the queuinghub Flask application.

This file is modified from this pwp-sensorhub-example in branch ex2-project-layout
https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-project-layout/sensorhub/__init__.py

Modifications: variable names.
'''
import os
from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
#added for client testing
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
cache = Cache()

def create_app(test_config=None):
    '''
    Create and configure the Flask application.

    Args:
        test_config (string): defines resource tests (otherwise None)

    Returns:
        flask app

    Exceptions:
        OSError
    '''
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "queuing.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CACHE_TYPE="FileSystemCache",
        CACHE_DIR=os.path.join(app.instance_path, "cache"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    elif test_config == "resourcetest":
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "testing.db"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True,
            CACHE_TYPE="SimpleCache",
            CACHE_DIR=os.path.join(app.instance_path, "testing_cache"),
        )
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config["SWAGGER"] = {
        "title": "Queuinghub API",
        "openapi": "3.0.4",
        "uiversion": 3,
        "doc_dir": "queuinghub/doc"
    }
    db.init_app(app)
    cache.init_app(app)
    _swagger = Swagger(app, template_file="doc/base.yml")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    from queuinghub import database
    from queuinghub import api
    from queuinghub.utils import PlaceConverter
    #, QueueConverter
    app.cli.add_command(database.init_db_command)
    #app.cli.add_command(database.generate_test_data)
    app.url_map.converters["place"] = PlaceConverter
    #app.url_map.converters["queue"] = QueueConverter
    app.register_blueprint(api.api_bp)

    return app
