import pika


class ConexaoRabbitmq:
    def __init__(self, ip_adress):
        self._conexao = pika.BlockingConnection(pika.ConnectionParameters(ip_adress))
        self._canal = self._conexao.channel()

    @property
    def canal(self):
        return self._canal

    @property
    def conexao(self):
        return self.conexao

    @canal.setter
    def canal(self, value):
        self._canal = value

    @conexao.setter
    def conexao(self, value):
        self._conexao = value

    def criar_exchange(self, nome_exchange, tipo_exchange):
        self._canal.exchange_declare(exchange=nome_exchange, exchange_type=tipo_exchange)

    def criar_fila(self, nome_fila, exclusive):
        self._canal.queue_declare(queue=nome_fila, exclusive=exclusive)

    def criar_vinculo_com_fila(self, nome_exchange, nome_fila, tag):
        self._canal.queue_bind(exchange=nome_exchange, queue=nome_fila, routing_key=tag)
