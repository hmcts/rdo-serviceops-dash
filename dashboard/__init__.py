from flask import Flask, Blueprint


from .routes.main import main
from .routes.az_services.az import az
from .routes.idam_services.idam import idam


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    app.register_blueprint(main)
    app.register_blueprint(az)
    app.register_blueprint(idam)

    return app