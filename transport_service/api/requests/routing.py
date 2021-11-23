from flask import Blueprint, make_response, request, jsonify
from werkzeug.utils import secure_filename
import csv
import io
from ..forms.routing import VehicleForm, TruckForm, BicycleForm, BikeshareForm, MotoScooterForm, MotorcycleForm, PedestrianForm, TransitForm
from ..valhalla import Valhalla

bp = Blueprint('routing', __name__, url_prefix='/route')

def _dropNones(value):
    if isinstance(value, dict):
        return {k: _dropNones(v) for k, v in value.items() if v is not None}
    elif isinstance (value, list):
        return [_dropNones(d) for d in value]
    else:
        return value

def _flattenLocations(locations):
    flat = []
    for loc in locations:
        side = loc.pop('side', {})
        flat.append({**loc, **side})
    return flat

def _prepare_parameters(data):
    costing_options = data
    locations = costing_options.pop('locations')
    units = costing_options.pop('units', None)
    language = costing_options.pop('language', None)
    directions_type = costing_options.pop('directions_type', None)
    date_time = costing_options.pop('date_time', None)
    locations = _dropNones(locations)
    locations = _flattenLocations(locations)
    directions_options = _dropNones({"units": units, "language": language, "directions_type": directions_type, "date_time": date_time})
    return locations, directions_options, costing_options


@bp.route('/auto', methods=['POST'])
def routeAuto():
    """**Flask GET rule**.

    Generates the route path for automobiles.
    ---
    post:
        summary: Generates the route path for automobiles.
        description: Standard costing for driving routes by car, motorcycle, truck, and so on that obeys automobile driving rules, such as access and turn restrictions. Auto provides a short time path (though not guaranteed to be shortest time) and uses intersection costing to minimize turns and maneuvers or road name changes. Routes also tend to favor highways and higher classification roads, such as motorways and trunks.
        tags:
            - Route
        requestBody:
            required: true
            content:
                application/json:
                    schema: routingVehicleForm
        responses:
            200: routeResponse
            400: validationErrorResponse
    """
    form = VehicleForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    locations, directions_options, costing_options = _prepare_parameters(form.data)
    return make_response(valhalla.routing('auto', locations, directions_options=directions_options, costing_options=costing_options))

@bp.route('/taxi', methods=['POST'])
def routeTaxi():
    """**Flask GET rule**.

    Generates the route path for taxi.
    ---
    post:
        summary: Generates the route path for taxies.
        description: Standard costing for taxi routes. Taxi costing inherits the auto costing behaviors, but checks for taxi lane access on the roads and favors those roads.
        tags:
            - Route
        requestBody:
            required: true
            content:
                application/json:
                    schema: routingVehicleForm
        responses:
            200: routeResponse
            400: validationErrorResponse
    """
    form = VehicleForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    locations, directions_options, costing_options = _prepare_parameters(form.data)
    return make_response(valhalla.routing('taxi', locations, directions_options=directions_options, costing_options=costing_options))

@bp.route('/bus', methods=['POST'])
def routeBus():
    """**Flask GET rule**.

    Generates the route path for bus.
    ---
    post:
        summary: Generates the route path for buses.
        description: Standard costing for bus routes. Bus costing inherits the auto costing behaviors, but checks for bus access on the roads.
        tags:
            - Route
        requestBody:
            required: true
            content:
                application/json:
                    schema: routingVehicleForm
        responses:
            200: routeResponse
            400: validationErrorResponse
    """
    form = VehicleForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    locations, directions_options, costing_options = _prepare_parameters(form.data)
    return make_response(valhalla.routing('bus', locations, directions_options=directions_options, costing_options=costing_options))

@bp.route('/truck', methods=['POST'])
def routeTruck():
    """**Flask GET rule**.

    Generates the route path for truck.
    ---
    post:
        summary: Generates the route path for trucks.
        description: Standard costing for trucks. Truck costing inherits the auto costing behaviors, but checks for truck access, width and height restrictions, and weight limits on the roads.
        tags:
            - Route
        requestBody:
            required: true
            content:
                application/json:
                    schema: routingTruckForm
        responses:
            200: routeResponse
            400: validationErrorResponse
    """
    form = TruckForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    locations, directions_options, costing_options = _prepare_parameters(form.data)
    return make_response(valhalla.routing('truck', locations, directions_options=directions_options, costing_options=costing_options))

@bp.route('/bicycle', methods=['POST'])
def routeBicycle():
    """**Flask GET rule**.

    Generates the route path for bicycles.
    ---
    post:
        summary: Generates the route path for bicycles.
        description: Standard costing for travel by bicycle, with a slight preference for using cycleways or roads with bicycle lanes. Bicycle routes follow regular roads when needed, but avoid roads without bicycle access.
        tags:
            - Route
        requestBody:
            required: true
            content:
                application/json:
                    schema: routingBicycleForm
        responses:
            200: routeResponse
            400: validationErrorResponse
    """
    form = BicycleForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    locations, directions_options, costing_options = _prepare_parameters(form.data)
    return make_response(valhalla.routing('bicycle', locations, directions_options=directions_options, costing_options=costing_options))

@bp.route('/bikeshare', methods=['POST'])
def routeBikeshare():
    """**Flask GET rule**.

    Generates the route path for bike sharing.
    ---
    post:
        summary: Generates the route path for bike sharing.
        description: A combination of pedestrian and bicycle.
        tags:
            - Route
        requestBody:
            required: true
            content:
                application/json:
                    schema: routingBikeshareForm
        responses:
            200: routeResponse
            400: validationErrorResponse
    """
    form = BikeshareForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    locations, directions_options, costing_options = _prepare_parameters(form.data)
    return make_response(valhalla.routing('bikeshare', locations, directions_options=directions_options, costing_options=costing_options))

@bp.route('motor_scooter', methods=['POST'])
def routeMotorScooter():
    """**Flask GET rule**.

    Generates the route path for motor scooters.
    ---
    post:
        summary: Generates the route path for motor scooters.
        description: Standard costing for travel by motor scooter or moped. By default, motor_scooter costing will avoid higher class roads unless the country overrides allows motor scooters on these roads. Motor scooter routes follow regular roads when needed, but avoid roads without motor_scooter, moped, or mofa access.
        tags:
            - Route
        requestBody:
            required: true
            content:
                application/json:
                    schema: routingMotorScooterForm
        responses:
            200: routeResponse
            400: validationErrorResponse
    """
    form = MotoScooterForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    locations, directions_options, costing_options = _prepare_parameters(form.data)
    return make_response(valhalla.routing('motor_scooter', locations, directions_options=directions_options, costing_options=costing_options))

@bp.route('motorcycle', methods=['POST'])
def routeMotorcycle():
    """**Flask GET rule**.

    Generates the route path for motorcycles.
    ---
    post:
        summary: Generates the route path for motorcycles.
        description: Standard costing for travel by motorcycle. This costing model provides options to tune the route to take roadways (road touring) vs. tracks and trails (adventure motorcycling).
        tags:
            - Route
        requestBody:
            required: true
            content:
                application/json:
                    schema: routingMotorcycleForm
        responses:
            200: routeResponse
            400: validationErrorResponse
    """
    form = MotorcycleForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    locations, directions_options, costing_options = _prepare_parameters(form.data)
    return make_response(valhalla.routing('motorcycle', locations, directions_options=directions_options, costing_options=costing_options))

@bp.route('pedestrian', methods=['POST'])
def routePedestrian():
    """**Flask GET rule**.

    Generates the route path for pedestrians.
    ---
    post:
        summary: Generates the route path for pedestrians.
        description: "Standard walking route that excludes roads without pedestrian access. In general, pedestrian routes are shortest distance with the following exceptions: walkways and footpaths are slightly favored, while steps or stairs and alleys are slightly avoided."
        tags:
            - Route
        requestBody:
            required: true
            content:
                application/json:
                    schema: routingPedestrianForm
        responses:
            200: routeResponse
            400: validationErrorResponse
    """
    form = PedestrianForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    locations, directions_options, costing_options = _prepare_parameters(form.data)
    return make_response(valhalla.routing('pedestrian', locations, directions_options=directions_options, costing_options=costing_options))

@bp.route('transit', methods=['POST'])
def routeTransit():
    """**Flask GET rule**.

    Generates the route path for public transport.
    ---
    post:
        summary: Generates the route path for public transport.
        description: Routes by public transport.
        tags:
            - Route
        requestBody:
            required: true
            content:
                application/json:
                    schema: routingTransitForm
        responses:
            200: routeResponse
            400: validationErrorResponse
    """
    form = TransitForm()
    if not form.validate_on_submit():
        return make_response(form.errors, 400)
    valhalla = Valhalla()
    locations, directions_options, costing_options = _prepare_parameters(form.data)
    return make_response(valhalla.routing('transit', locations, directions_options=directions_options, costing_options=costing_options))
