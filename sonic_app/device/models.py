from sonic_app.ext import db
from sqlalchemy.orm import backref


class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    model = db.Column(db.String(255))
    pins = db.relationship("Pin", backref=backref('device'), cascade='delete,all')


class Pin(db.Model):
    __tablename__ = "pins"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    value = db.Column(db.String(255))
    description = db.Column(db.String(255))
    device_id = db.Column(db.Integer, db.Foreignkey('devices.id'))
