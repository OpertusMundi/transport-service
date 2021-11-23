"""
### A service to perform transport-related operations on OSM network.

*Transport service* is a wrapper on services around the OSM (or OSM-like) network. It supports:

- **isodistance** and **isochrone** operations, which compute areas that are reachable within specified distance or time intervals from a location, and return the reachable regions as contours of polygons or lines that can be displayed on a map,
- **map-matching**, which turns a path into a route with narrative instructions or retrieves the attribute values from that matched line,
- **routing**, which returns detailed navigation and trip information,
- **geocoding** and **reverse geocoding** (work in progress).
"""

import os, sys
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from ._version import __version__
from .api.doc_components import add_components
from .logging import mainLogger, exception_as_rfc5424_structured_data

# OpenAPI documentation
mainLogger.debug('Initializing OpenAPI specification.')
spec = APISpec(
    title="Transport API",
    version=__version__,
    info=dict(
        description=__doc__,
        contact={"email": "pmitropoulos@getmap.gr"}
    ),
    externalDocs={"description": "GitHub", "url": "https://github.com/OpertusMundi/transport-service"},
    openapi_version="3.0.2",
    plugins=[FlaskPlugin()],
)
mainLogger.debug('Adding OpenAPI specification components.')
add_components(spec)

# Check environment variables
if os.getenv('SECRET_KEY') is None:
    mainLogger.fatal('Environment variable not set [variable="SECRET_KEY"]')
    sys.exit(1)
if os.getenv('VALHALLA_URL') is None:
    mainLogger.fatal('Environment variable not set [variable="VALHALLA_URL"]')
    sys.exit(1)
if os.getenv('CORS') is None:
    os.environ['CORS'] = '*'
    mainLogger.info('Set environment variable [CORS="*"]')


def create_app():
    """Create flask app."""
    from flask import Flask, make_response, g, request
    from flask_cors import CORS
    from werkzeug.exceptions import HTTPException, InternalServerError
    from transport_service.api import isoline, mapmatch, routing, misc

    mainLogger.debug('Initializing app.')
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        JSON_SORT_KEYS=False
    )

    #Enable CORS
    if os.getenv('CORS') is not None:
        if os.getenv('CORS')[0:1] == '[':
            origins = json.loads(os.getenv('CORS'))
        else:
            origins = os.getenv('CORS')
        cors = CORS(app, origins=origins)

    # Add blueprints
    mainLogger.debug('Registering blueprints.')
    app.register_blueprint(isoline.bp)
    app.register_blueprint(mapmatch.bp)
    app.register_blueprint(routing.bp)
    app.register_blueprint(misc.bp)

    # Register documentation
    mainLogger.debug('Registering documentation.')
    with app.test_request_context():
        for view in app.view_functions.values():
            spec.path(view=view)

    @app.route("/", methods=['GET'])
    def index():
        """The index route, returns the JSON OpenAPI specification."""
        mainLogger.info('Generating the OpenAPI document...')
        return make_response(spec.to_dict(), 200)

    # Register cli commands
    with app.app_context():
        import transport_service.cli

    # Exception handlers
    #
    # Define a catch-all exception handler that simply logs a proper error message.
    # Note: If actual error handling is needed, consider defining handlers targeting
    #   more specific exception types (derived from Exception).
    @app.errorhandler(Exception)
    def handle_any_error(ex):
        exc_message = str(ex)
        mainLogger.error("Unexpected error: %s", exc_message, extra=exception_as_rfc5424_structured_data(ex))
        # Convert and return an HTTPException (is a valid response object for Flask)
        if isinstance(ex, HTTPException):
            return ex
        else:
            return InternalServerError(exc_message)

    mainLogger.debug('Created app.')
    return app
