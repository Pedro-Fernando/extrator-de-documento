import json


from dominio.az_optipy.optipy import AzOptipy
from dominio.documento import Documento
from dominio.enums.types import FileType

from conexaorabbitmq import ConexaoRabbitmq

IP_ADDRESS_CONTAINER_RABBITMQ = '172.23.0.2'

NOME_EXCHANGE = 'ex_extracoes'
TAG_EXTRACOES = 'tag_extracoes'


az_optipy_imagem = AzOptipy('../dominio/arquivos_testes/trecho-livro.png', FileType.PNG)
texto_extraido = az_optipy_imagem.precess_ocr()

documento = Documento(1, 6, texto_extraido)
documento_imagem_formato_json = json.dumps(documento.__dict__)


az_optipy_imagem_base64 = AzOptipy('../dominio/arquivos_testes/trecho_de_livro.txt', FileType.TXT)
texto_extraido_base64 = az_optipy_imagem_base64.precess_base64_ocr()


documento = Documento(2, 6, texto_extraido_base64)
documento_imagem_base64_formato_json = json.dumps(documento.__dict__)

conexao = ConexaoRabbitmq(IP_ADDRESS_CONTAINER_RABBITMQ)
conexao.canal.basic_publish(exchange=NOME_EXCHANGE, routing_key=TAG_EXTRACOES, body=documento_imagem_formato_json)
conexao.canal.basic_publish(exchange=NOME_EXCHANGE, routing_key=TAG_EXTRACOES, body=documento_imagem_base64_formato_json)
conexao.canal.close()

# Com Imagem
# imagem = cv2.imread('trecho-livro.png')
# imagem_em_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2BGRA)
# texto = pytesseract.image_to_string(imagem_em_rgb, lang='por', config=config_tesseract)
# print(texto)
