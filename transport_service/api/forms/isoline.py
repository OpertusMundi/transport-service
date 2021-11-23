from wtforms import StringField, FloatField, IntegerField, FieldList, BooleanField
from wtforms.validators import Optional, DataRequired, AnyOf, NumberRange
from .validators import Lat, Lon
from . import BaseForm

class IsolineForm(BaseForm):
    """Base form for isoline requests.

    Extends:
        BaseForm
    """
    lat = FloatField('lat', validators=[DataRequired(), Lat()])
    lon = FloatField('lon', validators=[DataRequired(), Lon()])
    costing = StringField('costing', default='auto', validators=[Optional(), AnyOf(['auto', 'bicycle', 'pedestrian', 'bikeshare', 'bus', 'multimodal'])])
    range_ = FieldList(IntegerField('range', validators=[DataRequired()]), name="range", min_entries=1)
    color = FieldList(StringField('color', validators=[Optional()]))
    polygons = BooleanField('polygons', default=False, validators=[Optional()])
    denoise = FloatField('denoise', default=1.0, validators=[Optional(), NumberRange(min=0.0, max=1.0)])
