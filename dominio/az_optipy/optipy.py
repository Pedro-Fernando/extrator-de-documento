import io
import cv2
import json
import base64
import pytesseract

from PIL import Image
from pytesseract import Output

from typing import Union, Tuple

from dominio.enums.types import FileType
from dominio.decodificador_base64 import PDF2Images, Base64ToPDF
from dominio.az_optipy.imagem_processor import ImagemProcessor
from dominio.readers.reader import TxtReader

# todo problema no caminho do tessdata
CONFIG_TESSERACT = '--tessdata-dir tessdata --psm 4'
NIVEL_DE_CONFIANCA = 40


def _extract_text(img: Image) -> str:
    imagem_tratada = ImagemProcessor.color_rgb(img)
    # resultado = pytesseract.image_to_data(imagem_tratada, config=CONFIG_TESSERACT, lang='por',
    #                                       output_type=Output.DICT)
    # print(json.dumps(resultado, indent=4))
    # return pytesseract.image_to_string(imagem_tratada, lang='por', config=CONFIG_TESSERACT)
    return pytesseract.image_to_string(imagem_tratada, lang='por')


def _apply_ocr_in_images(imagens: list) -> str:
    textos_extraidos: list[str] = []

    for i in range(len(imagens)):
        texto = _extract_text(imagens[i])
        textos_extraidos.append(texto)

    return " ".join(textos_extraidos)


def _apply_ocr_to_image(imagem: Image) -> str:
    return _extract_text(imagem)


def _process_pdf(path: str) -> str:
    imagens = PDF2Images.get_pdf_to_images(path)
    return _apply_ocr_in_images(imagens)


def _process_img(path: str) -> str:
    imagem = cv2.imread(path)
    imagem_tratada = ImagemProcessor.color_rgb(imagem)

    # corrigir caminho tessdata
    # return pytesseract.image_to_string(imagem_tratada, lang='por', config=CONFIG_TESSERACT)
    return pytesseract.image_to_string(imagem_tratada, lang='por')


def _process_base64(path: str) -> Union[Tuple[str, bytes], ValueError]:
    try:
        reader = TxtReader(path)
        reader.read_txt()
        texto_base64 = reader.text

        cabecalho, encoded_data = texto_base64.split(",", 1)
        # Removendo o cabeçalho do tipo de arquivo
        file_type, encoding = cabecalho.split(":")[1].split(";")
        extension = file_type.split('/')[1]
        # Decodificando os dados
        decoded_data = base64.b64decode(encoded_data)

        return extension, decoded_data
    except ValueError as e:
        print(f"Erro ao extrair informações do base64: {e}")


class AzOptipy:
    def __init__(self, path: str, file_type: FileType) -> None:
        self._path = path
        self._file_type = file_type

    def precess_ocr(self) -> Union[str, ValueError]:
        is_arquivo_pdf = self._file_type == FileType.PDF
        is_arquivo_imagem = self._file_type == FileType.JPEG or self._file_type == FileType.PNG

        if is_arquivo_pdf:
            return _process_pdf(self._path)
        elif is_arquivo_imagem:
            return _process_img(self._path)
        else:
            raise ValueError("extensão nao Identificada.")

    def precess_base64_ocr(self) -> Union[str, ValueError]:
        is_arquivo_nao_eh_txt = self._file_type != FileType.TXT

        if is_arquivo_nao_eh_txt:
            raise ValueError("extensão nao Identificada.")

        extension, decoded_data = _process_base64(self._path)

        is_extensao_pdf = extension == FileType.PDF.value
        is_extensao_imagem = extension == FileType.JPEG.value or extension == FileType.PNG.value

        if is_extensao_pdf:
            imagens = PDF2Images.get_pdf_base64_to_images(decoded_data)
            return _apply_ocr_in_images(imagens)

        elif is_extensao_imagem:
            image_file = io.BytesIO(decoded_data)
            image = Image.open(image_file)
            return _apply_ocr_to_image(image)

        else:
            raise ValueError("extensão nao Identificada.")

    def image_to_pdf_searchable(self):
        pdf = pytesseract.image_to_pdf_or_hocr(self._path, extension='pdf')
        with open('test.pdf', 'w+b') as f:
            f.write(pdf)  # pdf type is bytes by default
