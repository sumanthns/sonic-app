from .views import IndexView
from sonic_app.core import core

routes = [((core,), ('', IndexView.as_view('index')), )]
