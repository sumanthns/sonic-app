import json

from nose.tools import assert_equals

from sonic_app.device.models import Device, Pin, Message
from sonic_app.ext import db
from sonic_app.testing import TestCase


class TestDeviceViews(TestCase):
    def test_create_device_of_model_A(self):
        self.app.post("/device",
                      data={
                          "model": "A",
                          "name": "fu",
                      })
        device = self.get_model(Device, name="fu")

        expected_device_pins = [2, 3, 4, 14, 15, 17, 18, 27,
                                22, 23, 24, 10, 9, 25, 11, 8, 7]
        expected_device_pin_names = ["GPIO{}".format(i) for i in expected_device_pins]
        actual_device_pins = [p.name for p in device.pins]
        assert_equals(expected_device_pin_names, actual_device_pins)

    def test_create_device_of_model_A_Plus(self):
        self.app.post("/device",
                      data={
                          "model": "A+",
                          "name": "fu",
                      })

        device = self.get_model(Device, name="fu")

        expected_device_pins = [2, 3, 4, 14, 15, 17, 18, 27,
                                22, 23, 24, 10, 9, 25, 11, 8,
                                7, 5, 6, 12, 13, 19, 16, 26,
                                20, 21]
        expected_device_pin_names = ["GPIO{}".format(i) for i in expected_device_pins]
        actual_device_pins = [p.name for p in device.pins]
        assert_equals(expected_device_pin_names, actual_device_pins)

    def test_create_device_with_unsupported_model(self):
        self.app.post("/device",
                      data={
                          "model": "C",
                          "name": "fu",
                      })

        device = self.get_model(Device, name="fu")
        assert device is None

    def test_delete_device(self):
        self.create_model(Device, name="fu", model='B+',
                          type="A_Plus")

        device = self.get_model(Device, name="fu", model="B+")
        device.create_pins()
        assert device
        assert len(Pin.query.filter_by(device_id=device.id).all()) is not 0

        self.app.post("/device/{}".format(device.id))

        assert self.get_model(Device, name="fu", model="B+") is None
        assert len(Pin.query.filter_by(device_id=device.id).all()) == 0

    def test_device_list(self):
        self.create_model(Device, name="fu", model='B+',
                          type="A_Plus")
        self.create_model(Device, name="fu1", model='B+',
                          type="A_Plus")
        self.create_model(Device, name="fu2", model='B+',
                          type="A_Plus")

        response = self.app.get("/device/list")
        assert_equals(200, response.status_code)
        assert "fu" in response.data
        assert "fu1" in response.data
        assert "fu2" in response.data

    def test_device_layout_show(self):
        self.create_model(Device, name="fu", model='B+',
                          type="A_Plus")

        device = self.get_model(Device, name="fu", model="B+")
        device.create_pins()
        assert device
        assert len(Pin.query.filter_by(device_id=device.id).all()) is not 0

        response = self.app.get("/device/{}/layout".format(device.id))
        assert_equals(200, response.status_code)
        assert all(map(lambda x: x.name in response.data, device.pins))

    def test_get_pin_status(self):
        self.create_model(Device, name="fu", model='B+',
                          type="A_Plus")

        device = self.get_model(Device, name="fu", model="B+")
        device.create_pins()
        assert device
        assert len(Pin.query.filter_by(device_id=device.id).all()) is not 0

        pin = device.pins[0]
        pin.status = True
        db.session.commit()

        response = self.app.get("/device/{0}/pin/{1}".
                                format(device.id, pin.name))
        assert_equals(200, response.status_code)
        assert_equals("True", response.data)

        pin.status = False
        db.session.commit()
        response = self.app.get("/device/{0}/pin/{1}".
                                format(device.id, pin.name))
        assert_equals("False", response.data)

    def test_update_pin_status(self):
        self.create_model(Device, name="fu", model='B+',
                          type="A_Plus")

        device = self.get_model(Device, name="fu", model="B+")
        device.create_pins()
        assert device
        assert len(Pin.query.filter_by(device_id=device.id).all()) is not 0

        pin = device.pins[0]
        self.app.post("/device/{0}/pin/{1}".
                      format(device.id, pin.name),
                      data={
                          "status": True
                      })
        message = self.get_model(Message, device_id=device.id)
        assert_equals("queued", message.status)

        expected_message_params = json.dumps(
            {"write_signal": {
                "led": pin.name.replace("GPIO", ""),
                "output": True, }})
        assert_equals(expected_message_params, message.params)
