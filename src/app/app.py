# -*- coding: utf-8 -*-
#
import os
from functools import wraps
from conf import Prod, Dev
from db.core import db
from flask import Flask
from flask import jsonify
from helpers import JSONEncoder, register_blueprints
from http_status import on_404
from middleware import HTTPMethodOverrideMiddleware
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware


def create_flask_app(package_name, package_path, settings_override=None, register_security_blueprint=True):

    app = Flask(package_name, instance_relative_config=register_security_blueprint)
    # app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    db.init_app(app)

    register_blueprints(app, package_name, package_path)
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app


def create_app(settings_override=None, register_security_blueprint=False):
    app = create_flask_app(__name__, __path__, settings_override, register_security_blueprint=register_security_blueprint)
    app.json_encoder = JSONEncoder
    app.errorhandler(404)(on_404)
    return app


def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            return jsonify(dict(status=0, data=rv, message=None)), sc
        return f

    return decorator


def enhance_app(app):

    from src.rest.test import bp

    app.register_blueprint(bp, url_prefix='/test')

    return app


config = Prod if os.path.exists('/home/q') else Dev
server = create_app(settings_override=config)
server = enhance_app(server)
application = DispatcherMiddleware(server)


if __name__ == '__main__':
    run_simple('0.0.0.0', 8000, application, use_reloader=True, use_debugger=True)