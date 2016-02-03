from sonic_app.device import device
from sonic_app.device.views import CreateDeviceView,\
    EditDeviceView, LayoutView, PinView

routes = [((device,),
           ('', CreateDeviceView.as_view('create_device')),
           ('/<device_id>', EditDeviceView.as_view('edit_device')),
           ('/<device_id>/layout', LayoutView.as_view('edit_layout')),
           ('/<device_id>/pin/<name>', PinView.as_view('show_pin')),
           )]
