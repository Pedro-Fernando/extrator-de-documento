import json

from dominio.documento import Documento
from mensageria.consumer import Consumer


def _callback_para_extracoes(ch, method, properties, body):
    document = json.loads(body)
    d = Documento(**document)

    print(d.id_documento)
    print(d.id_produto)
    print(d.texto_documento_extraido)


def main():
    IP_ADDRESS_CONTAINER_RABBITMQ = '172.23.0.2'
    NOME_EXCHANGE = 'ex_extracoes'
    TIPO_EXCHANGE = 'direct'
    NOME_FILA_PARA_EXTRACOES = 'fila_extracoes'
    IS_EXCLUSIVA = True
    TAG_EXTRACOES = 'tag_extracoes'

    consumer = Consumer(IP_ADDRESS_CONTAINER_RABBITMQ)
    consumer.connect()
    consumer.exchange(NOME_EXCHANGE, TIPO_EXCHANGE)
    consumer.queue_declare(NOME_FILA_PARA_EXTRACOES, IS_EXCLUSIVA)
    consumer.bind(NOME_EXCHANGE, NOME_FILA_PARA_EXTRACOES, TAG_EXTRACOES)
    consumer.consume(NOME_FILA_PARA_EXTRACOES, _callback_para_extracoes)
    consumer.close()


if __name__ == "__main__":
    main()
