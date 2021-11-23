from wtforms import StringField, FloatField, IntegerField, FieldList, FormField, Field
from wtforms.validators import Optional, DataRequired, AnyOf, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.widgets import TextInput
from .validators import ShapeCSV, Lat, Lon, ListForm, JSONForm, SomeOf
from .fields import JSONField, BooleanField
from . import BaseForm

class SideParameters(BaseForm):
    preferred_side = StringField('preferred_side', validators=[Optional(), AnyOf(['same', 'opposite', 'either'])])
    display_lat = FloatField('display_lat', validators=[Optional(), Lat()])
    display_lon = FloatField('display_lat', validators=[Optional(), Lon()])
    node_snap_tolerance = IntegerField('node_snap_tolerance', validators=[Optional(), NumberRange(min=0)])
    street_side_tolerance = IntegerField('street_side_tolerance', validators=[Optional(), NumberRange(min=0)])
    street_side_max_distance = IntegerField('street_side_max_distance', validators=[Optional(), NumberRange(min=0)])

class SearchFilterParameters(BaseForm):
    exclude_tunnel = BooleanField('exclude_tunnel', validators=[Optional()])
    exclude_bridge = BooleanField('exclude_bridge', validators=[Optional()])
    exclude_closures = BooleanField('exclude_closures', validators=[Optional()])
    min_road_class = StringField('min_road_class', validators=[Optional(), AnyOf(['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'service_other'])])
    max_road_class = StringField('max_road_class', validators=[Optional(), AnyOf(['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'service_other'])])

class LocationsForm(BaseForm):
    lat = FloatField('lat', validators=[DataRequired(), Lat()])
    lon = FloatField('lon', validators=[DataRequired(), Lon()])
    type = StringField('type', validators=[Optional(), AnyOf(['break', 'via'])])
    heading = IntegerField('heading', validators=[Optional(), NumberRange(min=0, max=360)])
    heading_tolerance = IntegerField('heading_tolerance', validators=[Optional(), NumberRange(min=0)])
    minimum_reachability = IntegerField('minimum_reachability', validators=[Optional(), NumberRange(min=0)])
    radius = IntegerField('radius', validators=[Optional(), NumberRange(min=0)])
    rank_candidates = BooleanField('rank_candidates', validators=[Optional()])
    side = JSONField('side', type_="dict", validators=[Optional(), JSONForm(SideParameters)])
    search_filter = JSONField('search_filter', type_="dict", validators=[Optional(), JSONForm(SearchFilterParameters)])
    name = StringField('name', validators=[Optional()])
    city = StringField('city', validators=[Optional()])
    state = StringField('state', validators=[Optional()])
    postal_code = StringField('postal_code', validators=[Optional()])
    country = StringField('country', validators=[Optional()])
    phone = StringField('phone', validators=[Optional()])
    url = StringField('url', validators=[Optional()])

class RoutingBaseForm(BaseForm):
    locations = JSONField('shape', validators=[DataRequired(), ListForm(LocationsForm)])
    units = StringField('units', default="kilometers", validators=[Optional(), AnyOf(['kilometers', 'miles'])])
    language = StringField('language', default="en-US", validators=[Optional(), AnyOf(['bg-BG', 'ca-ES', 'cs-CZ', 'da-DK', 'de-DE', 'el-GR', 'en-GB', 'en-US-x-pirate', 'en-US', 'es-ES', 'et-EE', 'fi-FI', 'fr-FR', 'hi-IN', 'hu-HU', 'it-IT', 'ja-JP', 'nb-NO', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'sk-SK', 'sl-SI', 'sv-SE', 'tr-TR', 'uk-UA'])])
    directions_type = StringField('directions_type', default="instructions", validators=[Optional(), AnyOf(['none', 'maneuvers', 'instructions'])])
    date_time = StringField('date_time', validators=[Optional()])

class _GenericForm(RoutingBaseForm):
    maneuver_penalty = IntegerField('maneuver_penalty', validators=[Optional(), NumberRange(min=0)])
    gate_cost = IntegerField('gate_cost', validators=[Optional(), NumberRange(min=0)])
    gate_penalty = IntegerField('gate_penalty', validators=[Optional(), NumberRange(min=0)])
    country_crossing_cost = IntegerField('country_crossing_cost', validators=[Optional(), NumberRange(min=0)])
    country_costing_penalty = IntegerField('country_costing_penalty', validators=[Optional(), NumberRange(min=0)])
    service_penalty = IntegerField('service_penalty', validators=[Optional(), NumberRange(min=0)])

class _AutomobileForm(_GenericForm):
    use_ferry = FloatField('use_ferry', validators=[Optional(), NumberRange(min=0, max=1)])
    use_tolls = FloatField('use_tolls', validators=[Optional(), NumberRange(min=0, max=1)])
    use_living_streets = FloatField('use_living_streets', validators=[Optional(), NumberRange(min=0, max=1)])
    use_tracks = FloatField('use_tracks', validators=[Optional(), NumberRange(min=0, max=1)])
    private_access_penalty = IntegerField('private_access_penalty', validators=[Optional(), NumberRange(min=0)])
    toll_booth_cost = IntegerField('toll_booth_cost', validators=[Optional(), NumberRange(min=0)])
    toll_booth_penalty = IntegerField('toll_booth_penalty', validators=[Optional(), NumberRange(min=0)])
    ferry_cost = IntegerField('ferry_cost', validators=[Optional(), NumberRange(min=0)])
    service_factor = IntegerField('service_factor', validators=[Optional(), NumberRange(min=0)])
    shortest = BooleanField('shortest', validators=[Optional()])
    top_speed = IntegerField('top_speed', validators=[Optional(), NumberRange(min=10, max=252)])
    ignore_closures = BooleanField('ignore_closures', validators=[Optional()])
    closure_factor = FloatField('closure_factor', validators=[Optional(), NumberRange(min=1, max=10)])

class VehicleForm(_AutomobileForm):
    height = FloatField('height', validators=[Optional(), NumberRange(min=0)])
    width = FloatField('width', validators=[Optional(), NumberRange(min=0)])
    exclude_unpaved = BooleanField('exclude_unpaved', validators=[Optional()])
    exclude_cash_only_tolls = BooleanField('exclude_cash_only_tolls', validators=[Optional()])
    include_hov2 = BooleanField('include_hov2', validators=[Optional()])
    include_hov3 = BooleanField('include_hov3', validators=[Optional()])
    include_hov = BooleanField('include_hov', validators=[Optional()])

class TruckForm(VehicleForm):
    length = FloatField('length', validators=[Optional(), NumberRange(min=0)])
    weight = FloatField('weight', validators=[Optional(), NumberRange(min=0)])
    axle_load = FloatField('axle_load', validators=[Optional(), NumberRange(min=0)])
    hazmat = BooleanField('hazmat', validators=[Optional()])

class BicycleForm(_GenericForm):
    bicycle_type = StringField('bicycle_type', validators=[Optional(), AnyOf(["Road", "Hybrid", "City", "Cross", "Mountain"])])
    cycling_speed = IntegerField('cycling_speed', validators=[Optional(), NumberRange(min=0)])
    use_roads = FloatField('use_roads', validators=[Optional(), NumberRange(min=0, max=1)])
    use_hills = FloatField('use_hills', validators=[Optional(), NumberRange(min=0, max=1)])
    use_ferry = FloatField('use_ferry', validators=[Optional(), NumberRange(min=0, max=1)])
    use_living_streets = FloatField('use_living_streets', validators=[Optional(), NumberRange(min=0, max=1)])
    avoid_bad_surfaces = FloatField('avoid_bad_surfaces', validators=[Optional(), NumberRange(min=0, max=1)])
    shortest = BooleanField('shortest', validators=[Optional()])

class BikeshareForm(BicycleForm):
    bss_return_cost = IntegerField('bss_return_cost', validators=[Optional(), NumberRange(min=0)])
    bss_return_penalty = IntegerField('bss_return_penalty', validators=[Optional(), NumberRange(min=0)])

class MotoScooterForm(_AutomobileForm):
    use_primary = FloatField('use_primary', validators=[Optional(), NumberRange(min=0, max=1)])
    use_hills = FloatField('use_hills', validators=[Optional(), NumberRange(min=0, max=1)])

class MotorcycleForm(_AutomobileForm):
    use_highways = FloatField('use_highways', validators=[Optional(), NumberRange(min=0, max=1)])
    use_trails = FloatField('use_trails', validators=[Optional(), NumberRange(min=0, max=1)])

class PedestrianForm(RoutingBaseForm):
    walking_speed = FloatField('walking_speed', validators=[Optional(), NumberRange(min=0.5, max=25)])
    walkway_factor = FloatField('walkway_factor', validators=[Optional(), NumberRange(min=0)])
    sidewalk_factor = FloatField('sidewalk_factor', validators=[Optional(), NumberRange(min=0)])
    alley_factor = FloatField('alley_factor', validators=[Optional(), NumberRange(min=0)])
    driveway_factor = FloatField('driveway_factor', validators=[Optional(), NumberRange(min=0.)])
    step_penalty = IntegerField('step_penalty', validators=[Optional(), NumberRange(min=0)])
    use_ferry = FloatField('use_ferry', validators=[Optional(), NumberRange(min=0, max=1)])
    use_living_streets = FloatField('use_living_streets', validators=[Optional(), NumberRange(min=0, max=1)])
    use_tracks = FloatField('use_tracks', validators=[Optional(), NumberRange(min=0, max=1)])
    use_hills = FloatField('use_hills', validators=[Optional(), NumberRange(min=0, max=1)])
    service_penalty = IntegerField('service_penalty', validators=[Optional(), NumberRange(min=0)])
    service_factor = IntegerField('service_factor', validators=[Optional(), NumberRange(min=0)])
    max_hiking_difficulty = IntegerField('max_hiking_difficulty', validators=[Optional(), NumberRange(min=1, max=6)])
    shortest = BooleanField('shortest', validators=[Optional()])

class TransitForm(RoutingBaseForm):
    use_bus = FloatField('use_bus', validators=[Optional(), NumberRange(min=0, max=1)])
    use_rail = FloatField('use_rail', validators=[Optional(), NumberRange(min=0, max=1)])
    use_transfers = FloatField('use_transfers', validators=[Optional(), NumberRange(min=0, max=1)])
    transit_start_end_max_distance = IntegerField('transit_start_end_max_distance', validators=[Optional(), NumberRange(min=0)])
    transit_transfer_max_distance = IntegerField('transit_transfer_max_distance', validators=[Optional(), NumberRange(min=0)])
