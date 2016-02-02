from sonic_app.device import device
from sonic_app.device.views import CreateDeviceView, EditDeviceView, EditLayoutView

routes = [((device,),
           ('', CreateDeviceView.as_view('create_device')),
           ('/<device_id>', EditDeviceView.as_view('edit_device')),
           ('device', EditLayoutView.as_view('edit_layout')),
           )]
