"""A collection of custom WTForms Validators."""

from wtforms.validators import ValidationError

class Coordinate:
    """Validates a Coordinate field in degrees (EPSG:4326)."""
    def __init__(self, lower, upper, message=None):
        if not message:
            message = "Invalid value: must be in [{lower}, {upper}].".format(lower=lower, upper=upper)
        self.lower = lower
        self.upper = upper
        self.message = message

    def __call__(self, form, field):
        if (field.data < self.lower or field.data > self.upper):
            raise ValidationError(self.message)


class Lat(Coordinate):
    """Validates a Latitude field in degrees (EPSG:4326)."""
    def __init__(self, message=None):
        super().__init__(-90, 90)


class Lon(Coordinate):
    """Validates a Longitude field in degrees (EPSG:4326)."""
    def __init__(self, message=None):
        super().__init__(-180, 180)


class ShapeCSV:
    """Validates a CSV file containing shape information."""
    def __init__(self, message=None):
        if not message:
            message = 'CSV must include a lat and a lon attribute.'
        self.message = message

    def __call__(self, form, field):
        from werkzeug.datastructures import FileStorage
        import csv
        import io

        if not (isinstance(field.data, FileStorage) and field.data):
            return

        if field.data.mimetype != 'text/csv':
            raise ValidationError(self.message)

        try:
            first_line = field.data.readline().decode()
            s = csv.Sniffer()
            delimiter = s.sniff(first_line).delimiter
            reader = csv.DictReader(io.StringIO(first_line), delimiter=delimiter)
            headers = reader.fieldnames
            if 'lat' not in headers or 'lon' not in headers:
                raise ValidationError(self.message)
            field.data.delimiter = delimiter
            field.data.fieldnames = headers
        except Exception as e:
            raise ValidationError(self.message)

class ListForm:
    """Validates a list field."""
    def __init__(self, Form, message=None):
        self.form = Form
        if not message:
            message = 'Not a valid List field.'
        self.message = message

    def __call__(self, form, field):
        from werkzeug.datastructures import ImmutableMultiDict

        CustomForm = self.form
        errors = []
        data = []
        for index, row in enumerate(field.data):
            if not isinstance(row, dict):
                raise ValidationError(self.message)
            rowForm = CustomForm(ImmutableMultiDict(row))
            if not rowForm.validate():
                errors.append({attr + '-' + str(index): rowForm.errors[attr] for attr in rowForm.errors})
            else:
                data.append(rowForm.data)
        if len(errors) > 0:
            raise ValidationError(errors)
        field.data = data

class JSONForm:
    """Validates a JSON field."""
    def __init__(self, Form, message=None):
        self.form = Form
        if not message:
            message = 'Not a valid JSON field.'
        self.message = message

    def __call__(self, form, field):
        from werkzeug.datastructures import ImmutableMultiDict

        CustomForm = self.form
        if not isinstance(field.data, dict):
            raise ValidationError(self.message)
        form = CustomForm(ImmutableMultiDict(field.data))
        if not form.validate():
            raise ValidationError(form.errors)

class SomeOf:
    """Validates a string field as a list of values."""
    def __init__(self, enum, message=None):
        if not message:
            message = "Invalid value, must be a comma separated list of {}.".format(', '.join(enum))
        self.enum = enum
        self.message = message

    def __call__(self, form, field):
        data = [value.strip() for value in field.data.split(',')] if isinstance(field.data, str) else field.data
        for value in data:
            if value not in self.enum:
                raise ValidationError(self.message)
        field.data = data
