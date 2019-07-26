from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required
import dash

from .routes.main import main
from .routes.az_services.az import az
from .routes.az_services.databases import azdb
from .routes.idam_services.idam import idam


def create_app():
    server = Flask(__name__)

    server.config.from_object('config.Config')

    from app.dashapps.dashapp1.layout import layout as layout1
    from app.dashapps.dashapp1.callbacks import register_callbacks as register_callbacks1

    register_dashapp(server, 'Dashapp 1', 'dashapp1',
                     layout1, register_callbacks1)

    from app.dashapps.dashapp2.layout import layout as layout2
    from app.dashapps.dashapp2.callbacks import register_callbacks as register_callbacks2

    register_dashapp(server, 'Dashapp 2', 'dashapp2',
                     layout2, register_callbacks2)

    from .routes.main import main
    server.register_blueprint(main)

    from .routes.az_services.az import az
    server.register_blueprint(az)

    from .routes.az_services.databases import azdb
    server.register_blueprint(azdb)

    from .routes.idam_services.idam import idam
    server.register_blueprint(idam)

    return server


def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(__name__,
        server=app,
        url_base_pathname="/{}/".format(base_pathname),
        assets_folder=get_root_path(__name__) + "/assets/",
        meta_tags=[meta_viewport])

    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)
    _protect_dashviews(my_dashapp)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])

