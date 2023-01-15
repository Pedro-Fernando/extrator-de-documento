import pika
from abc import ABC


class ConnectionRabbitMQ(ABC):

    def __init__(self, ip_adress=None):
        self._ip_adress = ip_adress
        self._connection = None
        self._channel = None

    def connect(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(self._ip_adress))
        self._channel = self._connection.channel()

    def exchange(self, exchange_name, exchange_type):
        self._channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    def close(self):
        self._connection.close()
