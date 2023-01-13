import json


from dominio.az_optipy.optipy import AzOptipy
from dominio.documento import Documento
from dominio.readers.reader_img import ImgReader
from dominio.readers.reader_txt import Base64Reader
from dominio.readers.reader_pdf import PDFReader
from dominio.enums.types import FileType

from conexaorabbitmq import ConexaoRabbitmq

IP_ADDRESS_CONTAINER_RABBITMQ = '172.23.0.2'

NOME_EXCHANGE = 'ex_extracoes'
TAG_EXTRACOES = 'tag_extracoes'

img_reader = ImgReader('../dominio/arquivos_testes/trecho-livro.png')
az_optipy_imagem = AzOptipy(img_reader)
texto_extraido = az_optipy_imagem.precess_ocr()

documento = Documento(1, 6, texto_extraido)
documento_imagem_formato_json = json.dumps(documento.__dict__)

base64_reader = Base64Reader('../dominio/arquivos_testes/trecho_de_livro.txt')
az_optipy_imagem_base64 = AzOptipy(base64_reader)
texto_extraido_base64 = az_optipy_imagem_base64.precess_ocr()

documento = Documento(2, 6, texto_extraido_base64)
documento_imagem_base64_formato_json = json.dumps(documento.__dict__)

pdf_reader = PDFReader('../dominio/arquivos_testes/Undersampling.pdf')
az_optipy_pdf = AzOptipy(pdf_reader)
texto_extraido_pdf = az_optipy_pdf.precess_ocr()

documento = Documento(3, 6, texto_extraido_pdf)
documento_pdf_formato_json = json.dumps(documento.__dict__)

conexao = ConexaoRabbitmq(IP_ADDRESS_CONTAINER_RABBITMQ)

conexao.canal.basic_publish(exchange=NOME_EXCHANGE, routing_key=TAG_EXTRACOES, body=documento_imagem_formato_json)
conexao.canal.basic_publish(exchange=NOME_EXCHANGE, routing_key=TAG_EXTRACOES, body=documento_imagem_base64_formato_json)
conexao.canal.basic_publish(exchange=NOME_EXCHANGE, routing_key=TAG_EXTRACOES, body=documento_pdf_formato_json)

conexao.canal.close()
