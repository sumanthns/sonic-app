import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DATABASE_QUERY_TIMEOUT = 0.5
    WTF_CSRF_ENABLED = True
    SECRET_KEY = str(uuid.uuid4())
    HOSTNAME = 'localhost'
    DEBUG = True

    URL_MODULES = [
        'core.urls.routes',
        'device.urls.routes',
    ]

    BLUEPRINTS = [
        'core.core',
        'device.device'
    ]

    PI_MODELS = [
        'A', 'B', 'A+', 'B+', '2'
    ]

    PI_MODEL_LAYOUTS = [
        ('A', 'sonic_app.device.forms.ModelALayoutForm'),
        ('B', 'sonic_app.device.forms.ModelALayoutForm'),
        ('A+', 'sonic_app.device.forms.ModelAPlusLayoutForm'),
        ('B+', 'sonic_app.device.forms.ModelAPlusLayoutForm'),
        ('2', 'sonic_app.device.forms.ModelAPlusLayoutForm'),
    ]

    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "secret_password_salt"


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    WTF_CSRF_ENABLED = False
    TESTING = True


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    HOSTNAME = os.environ.get("HOSTNAME")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")