import json

from sonic_app.lib.amqp_client import AmqpClient
from sonic_app.lib.config import CONF
from sonic_app.lib.manager import Manager
from sonic_app.lib.sonic_daemon import SonicDaemon
from sonic_app.lib.sonic_daemon_app import SonicDaemonApp


class ActionUnsupportedError(Exception):
    pass


class MessageListener(SonicDaemonApp):
    QUEUE = CONF.app_queue

    def __init__(self):
        self.pid = "/var/run/sonic_app/message_listener.pid"
        self.log_path = "/var/log/sonic_app/message_listener.log"
        SonicDaemonApp.__init__(self)
        self.amqp_client = AmqpClient()
        self.manager = Manager()

    def run(self):
        self.amqp_client.channel.queue_declare(queue=self.QUEUE)
        self.amqp_client.channel.basic_consume(self._callback,
                                               queue=self.QUEUE,
                                               no_ack=True)
        self.amqp_client.channel.start_consuming()

    def _callback(self, ch, method, properties, body):
        self.logger.debug("Processing {}".format(body))
        try:
            # message = json.loads(decrypt(body))
            message = json.loads(body)
            for key, val in message.iteritems():
                if hasattr(self.manager, key):
                    getattr(self.manager, key)(val)
                else:
                    raise ActionUnsupportedError(key)
        except Exception as e:
            self.logger.error("Error while processing message - {}"
                              .format(e.message))


if __name__ == "__main__":
    app = MessageListener()
    SonicDaemon(app).run()
