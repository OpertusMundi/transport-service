from flask import Blueprint, make_response, request, jsonify
from werkzeug.utils import secure_filename
import csv
import io
from ..forms.mapmatch import TraceRouteFileForm, TraceRouteBodyForm, TraceAttributesFileForm, TraceAttributesBodyForm
from ..valhalla import Valhalla

bp = Blueprint('mapmatch', __name__, url_prefix='/map_matching')

@bp.route('/trace_route', methods=['POST'])
def traceRoute():
    """**Flask GET rule**.

    Turn a list of coordinates into a route.
    ---
    post:
        summary: Turn a list of coordinates into a route.
        description: Takes the costing mode and a list of latitude, longitude coordinates to turn them into a route with the shape snapped to the road network and a set of guidance directions.
        tags:
            - MapMatching
        requestBody:
            required: true
            content:
                application/json:
                    schema: traceRouteForm
                multipart/form-data:
                    schema: traceRouteFileForm
                    encoding:
                        shape:
                            contentType: text/csv
        responses:
            200: routeResponse
            400: validationErrorResponse
    """
    form = TraceRouteFileForm() if 'shape' in request.files.keys() else TraceRouteBodyForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    if isinstance(form, TraceRouteFileForm):
        reader = csv.DictReader(io.StringIO(form.shape.data.read().decode()), fieldnames=form.shape.data.fieldnames, delimiter=form.shape.data.delimiter)
        form.shape.data = [{attr: row[attr] for attr in ['lat', 'lon', 'time', 'type'] if attr in form.shape.data.fieldnames} for row in reader]
    data = {attr: form[attr].data for attr in form.data if form[attr].data}
    valhalla = Valhalla()
    return make_response(valhalla.traceRoute(**data))

@bp.route('/trace_attributes', methods=['POST'])
def traceAttributes():
    """**Flask GET rule**.

    Match a list of coordinates to a detailed attribution along the route.
    ---
    post:
        summary: Match a list of coordinates to a detailed attribution along the route.
        description: Takes the costing mode and latitude, longitude positions and returns detailed attribution along the portion of the route. This includes details for each section of road along the path, as well as any intersections along the path.
        tags:
            - MapMatching
        requestBody:
            required: true
            content:
                application/json:
                    schema: traceAttributesForm
                multipart/form-data:
                    schema: traceAttributesFileForm
                    encoding:
                        shape:
                            contentType: text/csv
        responses:
            200: traceAttributesResponse
            400: validationErrorResponse
    """
    form = TraceAttributesFileForm() if 'shape' in request.files.keys() else TraceAttributesBodyForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    if isinstance(form, TraceAttributesFileForm):
        reader = csv.DictReader(io.StringIO(form.shape.data.read().decode()), fieldnames=form.shape.data.fieldnames, delimiter=form.shape.data.delimiter)
        form.shape.data = [{attr: row[attr] for attr in ['lat', 'lon', 'time', 'type'] if attr in form.shape.data.fieldnames} for row in reader]
    valhalla = Valhalla()
    return make_response(valhalla.traceAttributes(**form.data))
