import json


class Documento:
    def __init__(self, id_documento: int, id_produto: int, texto_documento_extraido: str) -> None:
        self.id_documento = id_documento
        self.id_produto = id_produto
        self.texto_documento_extraido = texto_documento_extraido

    @staticmethod
    def converter_para_documento(body):
        document = json.loads(body)
        return Documento(**document)
