import ConfigParser


class Config(object):
    def __init__(self):
        conf = ConfigParser.RawConfigParser()
        conf.read("/etc/sonic_app/sonic_app.conf")

        # amqp related parameters
        self.amqp_host = conf.get("amqp", "host")
        self.amqp_port = conf.getint("amqp", "port")
        self.amqp_username = conf.get("amqp", "username")
        self.amqp_password = conf.get("amqp", "password")
        self.app_queue = conf.get("amqp", "app_queue")

CONF = Config()
