from flask_wtf import FlaskForm
from wtforms.meta import DefaultMeta

class BindNameMeta(DefaultMeta):
    def bind_field(self, form, unbound_field, options):
        if 'name' in unbound_field.kwargs:
            options['name'] = unbound_field.kwargs.pop('name')
        return unbound_field.bind(form=form, **options)

class BaseForm(FlaskForm):
    """The WTForms base form, it disables CSRF.

    Extends:
        FlaskForm
    """
    class Meta(BindNameMeta):
        csrf = False
