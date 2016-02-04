import time
import traceback

from sonic_app.device.models import Message
from sonic_app.ext import db
from sonic_app.lib.amqp_client import publish_message
from sonic_app.lib.sonic_daemon import SonicDaemon
from sonic_app.lib.sonic_daemon_app import SonicDaemonApp


class MessagePusher(SonicDaemonApp):
    def __init__(self):
        self.pidfile_path = "/var/run/sonic_app/message_pusher.pid"
        self.log_path = "/var/log/sonic_app/message_pusher.log"
        SonicDaemonApp.__init__(self)

    def run(self):
        self.logger.debug("Starting message pusher")
        while True:
            try:
                for message in Message.query.filter_by(status='queued').all():
                    queue = message.device.uuid
                    payload = message.params
                    publish_message(queue, payload)
                    message.status = 'pushed'
                    db.session.commit()
                    self.logger.debug("Pushed message {0} for device id {1}".format(payload, message.device_id))
            except Exception as e:
                self.logger.debug("Oops! Error :{}".format(e.message))
                traceback.print_exc()
            time.sleep(10)


if __name__ == "__main__":
    app = MessagePusher()
    SonicDaemon(app).run()
