from wtforms import Field, BooleanField as OriginalBoolean
from wtforms.widgets import TextInput, CheckboxInput
import distutils.util

class JSONField(Field):
    widget = TextInput()

    def __init__(self, *args, type_='list', **kwargs):
        super().__init__(*args, **kwargs)
        self._type = type_

    def process_formdata(self, valuelist):
        if valuelist:
            if self._type == 'list':
                self.data = valuelist
            else:
                self.data = valuelist[0]

    def _value(self):
        return str(self.data) if self.data is not None else ""

class BooleanField(OriginalBoolean):

    """Represents an input checkbox.

    In contrast with the default BooleanField, it respects the default value, and `null` is assigned to data when no value is provided.

    Attributes:
        data (bool): The value of the field.
        default (bool): The default value of the field (if no data provided).
        false_values (tuple): If provided, a sequence of strings each of which is an exact match string of what is considered a "false" value.
    """

    def __init__(self, label=None, validators=None, false_values=None, **kwargs):
        default = kwargs.pop('default', None)
        if default is not None and isinstance(default, str):
            try:
                default = bool(distutils.util.strtobool(default))
            except ValueError:
                default = None
        elif isinstance(default, int):
            default = bool(default)
        elif isinstance(default, bool):
            pass
        else:
            default = None
        super().__init__(label, validators, default=default, **kwargs)
        self.default = default

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0] not in self.false_values
        else:
            self.data = self.default
