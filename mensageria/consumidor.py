import json

from conexaorabbitmq import ConexaoRabbitmq
from dominio.documento import Documento


IP_ADDRESS_CONTAINER_RABBITMQ = '172.23.0.2'

NOME_EXCHANGE = 'ex_extracoes'
TIPO_EXCHANGE = 'direct'
NOME_FILA_PARA_EXTRACOES = 'fila_extracoes'
IS_EXCLUSIVA = True
TAG_EXTRACOES = 'tag_extracoes'

conexao = ConexaoRabbitmq(IP_ADDRESS_CONTAINER_RABBITMQ)

conexao.criar_exchange(NOME_EXCHANGE, TIPO_EXCHANGE)
conexao.criar_fila(NOME_FILA_PARA_EXTRACOES, IS_EXCLUSIVA)
conexao.criar_vinculo_com_fila(NOME_EXCHANGE, NOME_FILA_PARA_EXTRACOES, TAG_EXTRACOES)


def callback(ch, method, properties, body):
    documento = json.loads(body)
    d = Documento(**documento)

    # print(d.id_documento)
    # print(d.id_produto)
    print('\n '.join(d.texto_documento_extraido))


conexao.canal.basic_consume(queue=NOME_FILA_PARA_EXTRACOES, on_message_callback=callback, auto_ack=True)
conexao.canal.start_consuming()
