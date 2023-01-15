from infra.mensageria.connection_rabbitmq import ConnectionRabbitMQ


def _callback_default(ch, method, properties, body):
    print("[x] Consumido : %r" % body)


class Consumer(ConnectionRabbitMQ):
    def __init__(self, ip_adress=None):
        super().__init__(ip_adress)
        self.callback_function = None

    def bind(self, exchange_name, queue_name, tag):
        self._channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=tag)

    def queue_declare(self, queue_name, is_exclusive):
        self._channel.queue_declare(queue=queue_name, exclusive=is_exclusive)

    def consume(self, queue_name, callback_function=None):
        self.callback_function = callback_function or _callback_default

        self._channel.basic_consume(queue=queue_name, on_message_callback=self.callback_function, auto_ack=True)
        self._channel.start_consuming()


if __name__ == "__main__":
    consumer = Consumer('172.23.0.2')
    consumer.connect()
    consumer.exchange('ex_hello', 'direct')
    consumer.queue_declare('hello', False)
    consumer.bind('ex_hello', 'hello', 'tag_hello')
    consumer.consume('hello', _callback_default)
    consumer.close()
