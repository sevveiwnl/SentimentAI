from flask import Flask
from flask.logging import create_logger
from dotenv import load_dotenv
import os
import logging

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = os.urandom(24)

    # Set up logging
    app.logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    from app import routes
    app.register_blueprint(routes.main)

    return app