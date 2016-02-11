from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class DeviceForm(Form):
    name = StringField("name", validators=[DataRequired()])
    model = SelectField('types', validators=[DataRequired()])

    def __init__(self, ):
        Form.__init__(self)

        from sonic_app.app import app
        self.model.choices = [(m, m) for m in app.config.get('PI_MODELS')]

    def validate(self):
        if not Form.validate(self):
            return False

        from sonic_app.app import app
        allowed_models = []
        for layout_type in ["A_TYPE_LAYOUTS", "A_PLUS_TYPE_LAYOUTS"]:
            allowed_models += app.config.get(layout_type)
        if self.model.data not in allowed_models:
            return False
        return True
