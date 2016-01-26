from flask import url_for, render_template, request, flash
from flask.views import MethodView
from sonic_app.device.forms import DeviceForm, LayoutFormFactory
from sonic_app.device.models import Device
from sonic_app.ext import db
from sonic_app.helper import get_object_or_404, flash_errors
from werkzeug.utils import redirect


class CreateDeviceView(MethodView):
    def get(self):
        form = DeviceForm()
        return render_template('device.html', form=form)


    def post(self):
        form = DeviceForm()
        if form.validate_on_submit():
            device = Device(
                name=form.name.data,
                model=form.model.data,
            )
            db.session.add(device)
            db.session.commit()
            return redirect(url_for('device.list_devices'))
        flash_errors(form)
        return render_template('device.html', form=form)


class EditDeviceView(MethodView):
    def get(self, device_id):
        device = get_object_or_404(Device, Device.slug == device_id)
        form = DeviceForm(device)
        return render_template('device.html', form=form)


    def post(self, device_id):
        device = get_object_or_404(Device, Device.slug == device_id)
        form = DeviceForm(device)
        if form.validate_on_submit():
            device.name = request.form.get('name')
            device.model = request.form.get('model')
            db.session.commit()
            return redirect(url_for('device.show_device', device_id=device.id))
        flash_errors(form)
        return render_template('device.html', form=form)


class CreateLayoutView(MethodView):
    def get(self, device_id):
        device = get_object_or_404(Device, Device.slug == device_id)
        form = LayoutFormFactory(device.model).get_layout_form()
        return render_template('layout.html', form=form)

    def post(self, device_id):
        device = get_object_or_404(Device, Device.slug == device_id)
        form = LayoutFormFactory(device.model).get_layout_form()
        if form.validate_on_submit():
            form.create_pins(device)
            flash("Successfully created layout.")
            return redirect(url_for("device.show_layout", device_id=device.id))
        flash_errors(form)
        return render_template('layout.html', form=form)

