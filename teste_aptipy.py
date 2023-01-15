from dominio.entity.documento import Documento
from infra.logger.logger import Logger
from infra.mensageria.consumer import Consumer

IP_ADDRESS_CONTAINER_RABBITMQ = '172.23.0.2'
NOME_EXCHANGE_EXTRAIDOS = 'ex_extraidos'
TIPO_EXCHANGE = 'direct'
IS_EXCLUSIVA = True
NOME_FILA_EXTRAIDOS = 'fila_extraidos'
TAG_EXTRAIDOS = 'tag_extraidos'

log = Logger('az_optipy')


def _callback_para_extraidos(ch, method, properties, body):
    d = Documento.converter_para_documento(body)

    log.info(f'consumindo documento id: {d.id_documento}, do produto id: {d.id_produto} para fila de extraídos.')
    print(d.id_documento)
    print(d.id_produto)
    print(d.texto_documento_extraido)


def criar_cosumidor_fila_extraidos():
    log.info("Iniciando Consumidor da fila de extraídos.")

    consumer = Consumer(IP_ADDRESS_CONTAINER_RABBITMQ)
    consumer.connect()
    consumer.exchange(NOME_EXCHANGE_EXTRAIDOS, TIPO_EXCHANGE)
    consumer.queue_declare(NOME_FILA_EXTRAIDOS, IS_EXCLUSIVA)
    consumer.bind(NOME_EXCHANGE_EXTRAIDOS, NOME_FILA_EXTRAIDOS, TAG_EXTRAIDOS)
    consumer.consume(NOME_FILA_EXTRAIDOS, _callback_para_extraidos)
    consumer.close()


def iniciar_consumidores():
    criar_cosumidor_fila_extraidos()


if __name__ == "__main__":
    iniciar_consumidores()
