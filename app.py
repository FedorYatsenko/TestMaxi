import os
import logging

from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request

import main


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    return app