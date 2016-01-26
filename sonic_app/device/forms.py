from flask_wtf import Form
from sonic_app.device.models import Pin
from sonic_app.ext import db
from werkzeug.utils import import_string
from wtforms import StringField, FormField, FieldList, SelectField
from wtforms.validators import DataRequired


class DeviceForm(Form):
    name = StringField("name", validators=[DataRequired()])
    model = SelectField('types', validators=[DataRequired()])

    def __init__(self, device=None):
        Form.__init__(self)

        from sonic_app.app import app

        self.model.choices = [(m, m) for m in app.config.get('PI_MODELS')]
        if device:
            self.name.data = device.name
            self.model.data = device.model


class PinForm(Form):
    name = StringField('name')
    description = StringField('description')


class ModelALayoutForm(Form):
    PINS = [2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 10, 9, 25, 11, 8, 7]
    def __init__(self, device=None):
        Form.__init__(self)
        for i in self.PINS:
            setattr(self, "gpio{}".format(i), StringField("GPIO{}".format(i)))

        if device and device.pins:
            self._set_pin_descriptions(device)

    def _set_pin_descriptions(self, device):
        for pin in device.pins:
            if hasattr(self, pin.name):
                setattr(self, pin.name, StringField())
                setattr(getattr(self, pin.name), "data", pin.description)

    def create_pins(self, device):
        for pin in self.PINS:
            pin_form_field = getattr(self, "gpio{}".format(pin))
            pin_form_data = getattr(pin_form_field, "data", None)
            if pin_form_data:
                pin_obj = Pin(name="gpio{}".format(pin),
                              description=pin_form_data,
                              device_id=device.id, )
                db.session.add(pin_obj)
                db.session.commit()



class ModelAPlusLayoutForm(ModelALayoutForm):
    PINS = [2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 10, 9, 25, 11, 8, 7,
            5, 6, 12, 13, 19, 16, 26, 20, 21]


class LayoutNotSupportedException(Exception):
    pass


class LayoutFormFactory(object):
    def __init__(self, model):
        self.model = model

    def get_layout_form(self):
        from sonic_app.app import app

        for ml in app.config.get("PI_MODEL_LAYOUTS", []):
            model, form = ml
            if self.model == model:
                form = import_string(form)
                return form()

        raise LayoutNotSupportedException()
