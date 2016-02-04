from sonic_app.device.models import Device
from sonic_app.ext import db


class UnsupportedDeviceError(Exception):
    pass


class UnsupportedPinError(Exception):
    pass


class Manager(object):
    def update_pin(self, opts):
        led = opts["led"]
        value = opts["output"]
        device_uuid = opts["device_uuid"]
        device = Device.query.filter_by(uuid=device_uuid).one()
        if not device:
            raise UnsupportedDeviceError()
        pin = device.pins.query.filter_by(name=led).one()
        if not pin:
            raise UnsupportedPinError()
        pin.status = value == "1"
        db.session.commit()
