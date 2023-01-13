import io
import base64
from PIL import Image

from typing import Union, Tuple

from dominio.readers.reader import Reader
from dominio.enums.types import FileType


class Base64Reader(Reader):
    def __init__(self, path):
        self._path = path
        self._text = None

        try:
            with open(self._path, "r") as f:
                self._text = f.read()
        except Exception as e:
            print(f"Erro ao ler arquivo de texto: {e}")

    def get_images_for_OCR(self):
        return _precess_txt_base64_ocr(self._text)


def _get_extension_header(cabecalho):
    file_type, encoding = cabecalho.split(":")[1].split(";")
    return file_type.split('/')[1]


def _break_apart_base64(texto_base64: str) -> Union[Tuple[str, bytes], ValueError]:
    try:
        cabecalho, encoded_data = texto_base64.split(",", 1)
        extension = _get_extension_header(cabecalho)

        decoded_data = base64.b64decode(encoded_data)

        return extension, decoded_data
    except ValueError as e:
        print(f"Erro ao extrair informações do base64: {e}")


def _precess_txt_base64_ocr(texto):
    texto_base64 = texto

    extension, decoded_data = _break_apart_base64(texto_base64)

    is_extensao_pdf = extension == FileType.PDF.value
    is_extensao_imagem = extension == FileType.JPEG.value or extension == FileType.PNG.value

    if is_extensao_pdf:
        imagens = base64.b64decode(decoded_data)
        return FileType.PDF, imagens

    elif is_extensao_imagem:
        image_file = io.BytesIO(decoded_data)
        image = Image.open(image_file)
        return FileType.IMG, image

    else:
        raise ValueError("extensão do Base64 não Identificada.")
