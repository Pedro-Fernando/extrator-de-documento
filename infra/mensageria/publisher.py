from infra.mensageria.connection_rabbitmq import ConnectionRabbitMQ


class Publisher(ConnectionRabbitMQ):
    def __init__(self, ip_adress=None):
        super().__init__(ip_adress)

    def publish(self, exchange_name, tag_name, message):
        self._channel.basic_publish(exchange=exchange_name, routing_key=tag_name, body=message)


if __name__ == "__main__":
    publisher = Publisher('172.23.0.2')
    publisher.connect()
    publisher.publish('ex_hello', 'tag_hello', 'Ola Mundo!')
    publisher.close()
