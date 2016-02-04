import time
import traceback

from sonic_app.lib.amqp_client import AmqpClient
from sonic_app.lib.ext_db import init_db
from sonic_app.lib.sonic_daemon import SonicDaemon
from sonic_app.lib.sonic_daemon_app import SonicDaemonApp


class MessagePusher(SonicDaemonApp):
    def __init__(self):
        self.pidfile_path = "/var/run/sonic_app/message_pusher.pid"
        self.log_path = "/var/log/sonic_app/message_pusher.log"
        self.amqp_client = AmqpClient()
        SonicDaemonApp.__init__(self)

    def run(self):
        self.logger.debug("Starting message pusher")
        self.amqp_client.open_connection()
        while True:
            db = init_db()
            try:
                messages = db.execute(
                    "SELECT devices.uuid, messages.params, messages.id"
                    " FROM messages, devices"
                    " WHERE messages.device_id = devices.id"
                    " AND messages.status = 'queued'")
                for message in messages:
                    self.logger.debug(message)
                    payload = message['params']
                    queue = message['uuid']
                    message_id = message['id']
                    self.logger.debug(queue)
                    self.amqp_client.publish(queue, payload)
                    db.execute("UPDATE messages SET status = 'pushed'"
                               " WHERE id = {}".format(message_id))
                    self.logger.debug("Pushed message {0} for device uuid {1}"
                                      .format(payload, queue))
            except Exception as e:
                self.logger.debug("Oops! Error :{0}\n{1}"
                                  .format(e.message, traceback.format_exc()))
            db.close()
            time.sleep(10)


if __name__ == "__main__":
    message_pusher = MessagePusher()
    SonicDaemon(message_pusher).run()
