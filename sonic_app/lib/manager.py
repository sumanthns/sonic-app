from sonic_app.lib.ext_db import init_db, rows_exist


class UnsupportedDeviceError(Exception):
    pass


class UnsupportedPinError(Exception):
    pass


class Manager(object):
    def update_pin(self, opts):
        db = init_db()
        led = opts["led"]
        value = opts["output"]
        device_uuid = opts["device_uuid"]
        devices = db.execute("SELECT id FROM devices"
                             " WHERE uuid = '{}'"
                             .format(device_uuid))
        if not rows_exist(devices):
            raise UnsupportedDeviceError()

        pins = db.execute("SELECT pins.id FROM pins, devices"
                          " WHERE pins.device_id = devices.id"
                          " AND pins.name = '{0}'"
                          " AND devices.uuid = '{1}'".
                          format(led, device_uuid))
        if not rows_exist(pins):
            raise UnsupportedPinError()

        db.execute("UPDATE pins"
                   " JOIN devices ON devices.id = pins.device_id"
                   " SET pins.status = {0}"
                   " WHERE pins.name = '{1}'"
                   " AND devices.uuid = '{2}'".
                   format(int(value), led, device_uuid))

