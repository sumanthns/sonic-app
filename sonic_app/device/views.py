import json
import uuid

from flask import url_for, render_template, request
from flask.views import MethodView
from sonic_app.device.forms import DeviceForm
from sonic_app.device.models import Device, Pin, DeviceFactory, Message
from sonic_app.ext import db
from sonic_app.helper import get_object_or_404, flash_errors
from werkzeug.exceptions import abort
from werkzeug.utils import redirect


class CreateDeviceView(MethodView):
    def get(self):
        form = DeviceForm()
        return render_template('device.html', form=form)

    def post(self):
        form = DeviceForm()
        if form.validate_on_submit():
            model = form.model.data
            device = DeviceFactory(model).get_device()
            device.name = form.name.data
            device.model = model
            device.uuid = str(uuid.uuid4())
            device.create_pins()
            db.session.add(device)
            db.session.commit()
            return redirect(url_for('device.edit_device', device_id=device.id))
        flash_errors(form)
        return render_template('device.html', form=form)


class EditDeviceView(MethodView):
    def get(self, device_id):
        device = get_object_or_404(Device, Device.id == device_id)
        form = DeviceForm(device)
        return render_template('device.html', form=form)

    def post(self, device_id):
        device = get_object_or_404(Device, Device.id == device_id)
        form = DeviceForm(device)
        if form.validate_on_submit():
            device.name = request.form.get('name')
            device.model = request.form.get('model')
            db.session.commit()
            return redirect(url_for('device.edit_device', device_id=device.id))
        flash_errors(form)
        return render_template('device.html', form=form)


class LayoutView(MethodView):
    def get(self, device_id):
        device = get_object_or_404(Device, Device.id == device_id)
        return render_template('layout.html', device=device)


class PinView(MethodView):
    def get(self, device_id, name):
        pin = get_object_or_404(Pin, Pin.device_id == device_id, Pin.name == name)
        return str(pin.status), 200

    def post(self, device_id, name):
        status = request.form.get('status', None)
        if status:
            output = status == "True"
            params = {"write_signal": {"led": name.replace("GPIO", ""), "output": output}}
            message = Message(
                device_id=device_id,
                status="queued",
                params=json.dumps(params)
            )
            db.session.add(message)
            db.session.commit()
            return "", 200
        abort(400)
