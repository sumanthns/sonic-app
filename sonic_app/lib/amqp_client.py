import functools
import pika
import json


class AmqpClient():
    def __init__(self):
        host = 'localhost'
        self.connection_parameters = pika.ConnectionParameters(host)

    def _open_connection(self):
        self.connection = pika.BlockingConnection(self.connection_parameters)
        self.channel = self.connection.channel()

    def _close_connection(self):
        self.connection.close()

    def with_open_connection(func):
        def inner(self, *args, **kwargs):
            self._open_connection()
            func(self, *args, **kwargs)
            self._close_connection()

        return inner

    @with_open_connection
    def publish(self, queue, msg):
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue,
                                   body=json.dumps(msg))


def publish_message(queue, message):
    amqp_client = AmqpClient()
    amqp_client.publish(queue, message)




