from wtforms import StringField, FloatField, IntegerField, FieldList, BooleanField, FormField
from wtforms.validators import Optional, DataRequired, AnyOf, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from .validators import ShapeCSV, Lat, Lon, ListForm, SomeOf
from .fields import JSONField
from . import BaseForm

filters_enum = ['edge.names', 'edge.length', 'edge.speed', 'edge.road_class', 'edge.begin_heading', 'edge.end_heading', 'edge.begin_shape_index', 'edge.end_shape_index', 'edge.traversability', 'edge.use', 'edge.toll', 'edge.unpaved', 'edge.tunnel', 'edge.bridge', 'edge.roundabout', 'edge.internal_intersection', 'edge.drive_on_right', 'edge.surface', 'edge.sign.exit_number', 'edge.sign.exit_branch', 'edge.sign.exit_toward', 'edge.sign.exit_name', 'edge.travel_mode', 'edge.vehicle_type', 'edge.pedestrian_type', 'edge.bicycle_type', 'edge.transit_type', 'edge.id', 'edge.way_id', 'edge.weighted_grade', 'edge.max_upward_grade', 'edge.max_downward_grade', 'edge.mean_elevation', 'edge.lane_count', 'edge.cycle_lane', 'edge.bicycle_network', 'edge.sac_scale', 'edge.shoulder', 'edge.sidewalk', 'edge.density', 'edge.speed_limit', 'edge.truck_speed', 'edge.truck_route', 'node.intersecting_edge.begin_heading', 'node.intersecting_edge.from_edge_name_consistency', 'node.intersecting_edge.to_edge_name_consistency', 'node.intersecting_edge.driveability', 'node.intersecting_edge.cyclability', 'node.intersecting_edge.walkability', 'node.intersecting_edge.use', 'node.intersecting_edge.road_class', 'node.intersecting_edge.lane_count', 'node.elapsed_time', 'node.admin_index', 'node.type', 'node.fork', 'node.time_zone', 'osm_changeset', 'shape', 'admin.country_code', 'admin.country_text', 'admin.state_code', 'admin.state_text', 'matched.point', 'matched.type', 'matched.edge_index', 'matched.begin_route_discontinuity', 'matched.end_route_discontinuity', 'matched.distance_along_edge', 'matched.distance_from_trace_point']

class MapMatchForm(BaseForm):
    """Base form for map matching requests.

    Extends:
        BaseForm
    """
    costing = StringField('costing', default='auto', validators=[Optional(), AnyOf(['auto', 'auto_shorter', 'bicycle', 'bus', 'pedestrian'])])

class ShapeForm(BaseForm):
    lat = FloatField('lat', validators=[DataRequired(), Lat()])
    lon = FloatField('lon', validators=[DataRequired(), Lon()])
    time = IntegerField('time', validators=[Optional(), NumberRange(min=0)])

class ShapeFormWithType(ShapeForm):
    type = StringField('type', name="type", default="break", validators=[Optional(), AnyOf(['break', 'via'])])

class TraceRouteForm(MapMatchForm):
    search_radius = IntegerField('search_radius', validators=[Optional()])
    interpolation_distance = IntegerField('interpolation_distance', validators=[Optional()])
    gps_accuracy = IntegerField('gps_accuracy', validators=[Optional()])
    breakage_distance = IntegerField('breakage_distance', validators=[Optional()])
    language = StringField('language', default="en-US", validators=[Optional(), AnyOf(['bg-BG', 'ca-ES', 'cs-CZ', 'da-DK', 'de-DE', 'el-GR', 'en-GB', 'en-US-x-pirate', 'en-US', 'es-ES', 'et-EE', 'fi-FI', 'fr-FR', 'hi-IN', 'hu-HU', 'it-IT', 'ja-JP', 'nb-NO', 'nl-NL', 'pl-PL', 'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'sk-SK', 'sl-SI', 'sv-SE', 'tr-TR', 'uk-UA'])])
    directions_type = StringField('directions_type', default="instructions", validators=[Optional(), AnyOf(['none', 'maneuvers', 'instructions'])])
    units = StringField('units', default="kilometers", validators=[Optional(), AnyOf(['kilometers', 'miles'])])

class TraceRouteFileForm(TraceRouteForm):
    shape = FileField('shape', validators=[FileRequired(), FileAllowed(['csv']), ShapeCSV()])

class TraceRouteBodyForm(TraceRouteForm):
    shape = JSONField('shape', validators=[DataRequired(), ListForm(ShapeFormWithType)])

class TraceAttributesForm(MapMatchForm):
    filter_action = StringField('filter_action', default="exclude", validators=[Optional(), AnyOf(['exclude', 'include'])])

class TraceAttributesFileForm(MapMatchForm):
    filters = StringField('filters', validators=[Optional(), SomeOf(filters_enum)])
    shape = FileField('shape', validators=[FileRequired(), FileAllowed(['csv']), ShapeCSV()])

class TraceAttributesBodyForm(MapMatchForm):
    filters = JSONField('filters', validators=[Optional(), SomeOf(filters_enum)])
    shape = JSONField('shape', validators=[DataRequired(), ListForm(ShapeFormWithType)])
