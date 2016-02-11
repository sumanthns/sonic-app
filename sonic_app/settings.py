import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DATABASE_QUERY_TIMEOUT = 0.5
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = True
    SECRET_KEY = str(uuid.uuid4())
    HOSTNAME = 'localhost'
    DEBUG = True

    URL_MODULES = [
        'sonic_app.core.urls.routes',
        'sonic_app.device.urls.routes',
    ]

    BLUEPRINTS = [
        'sonic_app.core.core',
        'sonic_app.device.device',
    ]

    PI_MODELS = [
        'A', 'B', 'A+', 'B+', '2'
    ]

    A_TYPE_LAYOUTS = ["A", "B"]
    A_PLUS_TYPE_LAYOUTS = ["A+", "B+", "2"]

    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "secret_password_salt"


class TestConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/sonic_app_test'
    WTF_CSRF_ENABLED = False
    TESTING = True


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/sonic_app'
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    HOSTNAME = os.environ.get("HOSTNAME")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
