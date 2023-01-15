from dominio.entity.documento import Documento
from infra.logger.logger import Logger
from infra.mensageria.consumer import Consumer
from infra.mensageria.publisher import Publisher

IP_ADDRESS_CONTAINER_RABBITMQ = '172.23.0.2'
NOME_EXCHANGE_EXTRACOES = 'ex_extracoes'
NOME_EXCHANGE_EXTRAIDOS = 'ex_extraidos'
TIPO_EXCHANGE = 'direct'
NOME_FILA_PARA_EXTRACOES = 'fila_extracoes'
IS_EXCLUSIVA = True
TAG_EXTRACOES = 'tag_extracoes'
TAG_EXTRAIDOS = 'tag_extraidos'

log = Logger('az_optipy')


def _callback_para_extracoes(ch, method, properties, body):
    publisher = Publisher(IP_ADDRESS_CONTAINER_RABBITMQ)
    publisher.connect()

    d = Documento.converter_para_documento(body)

    log.info(f'publicando documento id: {d.id_documento}, do produto id: {d.id_produto} para fila de extraídos.')

    publisher.publish(NOME_EXCHANGE_EXTRAIDOS, TAG_EXTRAIDOS, body)
    publisher.close()


def main():
    log.info("Iniciando Consumidor da fila de extrações.")

    consumer = Consumer(IP_ADDRESS_CONTAINER_RABBITMQ)
    consumer.connect()
    consumer.exchange(NOME_EXCHANGE_EXTRACOES, TIPO_EXCHANGE)
    consumer.queue_declare(NOME_FILA_PARA_EXTRACOES, IS_EXCLUSIVA)
    consumer.bind(NOME_EXCHANGE_EXTRACOES, NOME_FILA_PARA_EXTRACOES, TAG_EXTRACOES)
    consumer.consume(NOME_FILA_PARA_EXTRACOES, _callback_para_extracoes)
    consumer.close()


if __name__ == "__main__":
    main()
