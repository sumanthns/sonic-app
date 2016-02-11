from sonic_app.device import device
from sonic_app.device.views import CreateDeviceView, \
    LayoutView, PinView, DeleteDeviceView, ListDeviceView

routes = [((device,),
           ('', CreateDeviceView.as_view('create')),
           ('/<device_id>', DeleteDeviceView.as_view('delete')),
           ('/list', ListDeviceView.as_view('list')),
           ('/<device_id>/layout', LayoutView.as_view('show_layout')),
           ('/<device_id>/pin/<name>', PinView.as_view('edit_pin')),
           )]
