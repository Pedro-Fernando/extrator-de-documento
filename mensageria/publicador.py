import base64
import pytesseract
import json
import cv2

from dominio.decodificador_base64 import Base64ToPDF
from dominio.documento import Documento
from dominio.tratar_image import TratadorDeImagem
from conexaorabbitmq import ConexaoRabbitmq

IP_ADDRESS_CONTAINER_RABBITMQ = '172.23.0.2'

NOME_EXCHANGE = 'ex_extracoes'
TAG_EXTRACOES = 'tag_extracoes'

# abrir pdf de uma pasta
with open('../dominio/arquivos_testes/trecho_livro_2.pdf', 'rb') as arquivo:
    pdf_base64 = base64.b64encode(arquivo.read())

# Converter o PDF para imagem
images = Base64ToPDF.get_pdf_to_images(pdf_base64)
config_tesseract = '--tessdata-dir tessdata --psm 4'
texto_extraido = []
for i in range(len(images)):
    # todo -> aqui entrará o tratamento da imagem para depois adicionar na lista
    # imagem_tratada = TratadorDeImagem.color_gray(images[i])

    imagem_tratada = TratadorDeImagem.color_rgb(images[i])

    texto = pytesseract.image_to_string(imagem_tratada, lang='por', config=config_tesseract)
    texto_extraido.append(texto)

documento = Documento(99, 50, texto_extraido)
documento_formato_json = json.dumps(documento.__dict__)

conexao = ConexaoRabbitmq(IP_ADDRESS_CONTAINER_RABBITMQ)
conexao.canal.basic_publish(exchange=NOME_EXCHANGE, routing_key=TAG_EXTRACOES, body=documento_formato_json)
conexao.canal.close()

# Com Imagem
# imagem = cv2.imread('trecho-livro.png')
# imagem_em_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2BGRA)
# texto = pytesseract.image_to_string(imagem_em_rgb, lang='por', config=config_tesseract)
# print(texto)
