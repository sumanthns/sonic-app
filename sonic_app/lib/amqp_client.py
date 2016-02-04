import json
import pika
from sonic_app.lib.config import CONF


class AmqpClient():
    def __init__(self):
        host = CONF.amqp_host
        port = CONF.amqp_port
        username = CONF.amqp_username
        password = CONF.amqp_password
        credentials = pika.PlainCredentials(username, password)
        self.connection_parameters = pika.ConnectionParameters(
            host, port, '/', credentials)

    def open_connection(self):
        self.connection = pika.BlockingConnection(self.connection_parameters)
        self.channel = self.connection.channel()

    def close_connection(self):
        self.connection.close()

    def with_open_connection(func):
        def inner(self, *args, **kwargs):
            self.open_connection()
            func(self, *args, **kwargs)
            self.close_connection()

        return inner

    @with_open_connection
    def publish(self, queue, msg):
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue,
                                   body=msg)


def publish_message(queue, message):
    amqp_client = AmqpClient()
    amqp_client.publish(queue, message)




