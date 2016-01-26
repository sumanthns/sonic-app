from flask import Flask
from werkzeug.utils import import_string


class NoBlueprintException(Exception):
    pass


class NoRouteModuleException(Exception):
    pass


def _get_imported_stuff_by_path(path):
    module_name, object_name = path.rsplit('.', 1)
    module = import_string(module_name)

    return module, object_name


class AppFactory(object):
    def __init__(self, config, name):
        self.config = config
        self.name = name

    def _build_app(self):
        app = Flask(self.name)
        self._add_config(app)
        self._init_db(app)
        self._register_blueprints(app)
        self._register_routes(app)
        return app

    def _add_config(self, app):
        app.config.from_object(self.config)

    def _init_db(self, app):
        from app import db
        db.init_app(app)

    def get_app(self):
        app = self._build_app()
        return app

    def _register_blueprints(self, app):
        self._bp = {}
        for blueprint_path in app.config.get('BLUEPRINTS', []):
            module, b_name = \
                _get_imported_stuff_by_path(blueprint_path)
            if hasattr(module, b_name):
                app.register_blueprint(getattr(module, b_name))
            else:
                raise NoBlueprintException(
                    'No {bp_name} blueprint found'.format(bp_name=b_name))

    def _register_routes(self, app):
        for url_module in app.config.get('URL_MODULES', []):
            module, r_name = _get_imported_stuff_by_path(url_module)
            if hasattr(module, r_name):
                self._setup_routes(getattr(module, r_name), app)
            else:
                raise NoRouteModuleException('No {r_name} url module found'.format(r_name=r_name))

    def _setup_routes(self, routes, app):
        for route in routes:
            blueprint, rules = route[0], route[1:]
            for pattern, view in rules:
                if isinstance(blueprint, tuple):
                    blueprint = blueprint[0]
                blueprint.add_url_rule(pattern, view_func=view)
            if blueprint not in app.blueprints:
                app.register_blueprint(blueprint)