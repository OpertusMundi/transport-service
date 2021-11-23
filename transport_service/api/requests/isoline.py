from flask import Blueprint, make_response, request
from ..forms.isoline import IsolineForm
from ..valhalla import Valhalla

bp = Blueprint('isoline', __name__, url_prefix='/isoline')

@bp.route('/isodistance', methods=['GET'])
def isodistance():
    """**Flask GET rule**.

    Compute areas that are within specified distance from a location.
    ---
    get:
        summary: Compute areas that are within specified distance.
        description: Computes areas that are within specified distance from a location, and returns the reachable regions as contours of polygons or lines that you can display on a map.
        tags:
            - Isoline
        parameters:
            - lat
            - lon
            - costing
            - rangeDistance
            - color
            - polygons
            - denoise
        responses:
            200: isochroneResponse
            400: validationErrorResponse
    """
    form = IsolineForm(request.args)
    if not form.validate():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    return make_response(valhalla.isodistance(**form.data))

@bp.route('/isochrone', methods=['GET'])
def isochrone():
    """**Flask GET rule**.

    Compute areas that are reachable within specified time intervals from a location.
    ---
    get:
        summary: Compute areas that are reachable within specified time intervals.
        description: Computes areas that are reachable within specified time intervals from a location, and returns the reachable regions as contours of polygons or lines that you can display on a map.
        tags:
            - Isoline
        parameters:
            - lat
            - lon
            - costing
            - rangeTime
            - color
            - polygons
            - denoise
        responses:
            200: isochroneResponse
            400: validationErrorResponse
    """
    form = IsolineForm(request.args)
    if not form.validate():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    return make_response(valhalla.isochrone(**form.data))
