from sonic_app.ext import db
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import backref


class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    model = db.Column(db.String(255))
    type = db.Column(db.String(255))
    pins = db.relationship("Pin", backref=backref('device'), cascade='delete,all')
    messages = db.relationship("Message", backref=backref('device'), cascade='delete,all')

    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'devices'
    }

    def create_pins(self):
        for pin in self.allowed_pins:
            self.pins.append(Pin(name="GPIO{}".format(pin),
                                 device_id=self.id,
                                 status=False, ))


class DeviceFactory():
    def __init__(self, model):
        self.model = model

    def get_device(self):
        from sonic_app.app import app
        if self.model in app.config.get("A_TYPE_LAYOUTS"):
            device = DeviceA()
            device.type = 'A'
        elif self.model in app.config.get("A_PLUS_TYPE_LAYOUTS"):
            device = DeviceAPlus()
            device.type = "A_Plus"
        return device


class DeviceA(Device):
    allowed_pins = [2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 10, 9, 25, 11, 8, 7]

    __mapper_args__ = {
        'polymorphic_identity':'A'
    }


class DeviceAPlus(Device):
    allowed_pins = [2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 10, 9, 25, 11, 8, 7,
                    5, 6, 12, 13, 19, 16, 26, 20, 21]

    __mapper_args__ = {
        'polymorphic_identity':'A_Plus'
    }


class Pin(db.Model):
    __tablename__ = "pins"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    value = db.Column(db.String(255))
    description = db.Column(db.String(255))
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    status = db.Column(db.Boolean)

    __tableargs__ = (UniqueConstraint('device_id', 'name', name='device_name_uc'))


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    status = db.Column(db.String(255))
    params = db.Column(db.String(255))


