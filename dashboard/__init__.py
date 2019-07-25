from flask import Flask, Blueprint

from .routes.main import main
from .routes.az_services.az import az
from .routes.az_services.databases import azdb
from .routes.idam_services.idam import idam


def create_app(config_file='settings.py'):
    app = Flask(__name__, 
                instance_relative_config=False)

    app.config.from_object('config.Config')

    with app.app_context():

        from .routes.main import main
        app.register_blueprint(main)

        from .routes.az_services.az import az
        app.register_blueprint(az)

        from .routes.az_services.databases import azdb
        app.register_blueprint(azdb)

        from .routes.idam_services.idam import idam
        app.register_blueprint(idam)

        from .dash import dashboards
        app = dashboards.add_dash(app)


        return app