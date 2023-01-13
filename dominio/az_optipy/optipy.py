import json
from typing import Union

import pytesseract
from PIL import Image
from pytesseract import Output

from dominio.az_optipy.imagem_processor import ImagemProcessor
from dominio.enums.types import FileType
from dominio.readers.reader import Reader

# todo problema no caminho do tessdata
# CONFIG_TESSERACT = '--tessdata-dir tessdata --psm 4'
CONFIG_TESSERACT = '--psm 4'
NIVEL_DE_CONFIANCA = 40


def _extract_text(img: Image) -> str:
    imagem_tratada = ImagemProcessor.color_rgb(img)
    resultado = pytesseract.image_to_data(imagem_tratada, config=CONFIG_TESSERACT, lang='por',
                                          output_type=Output.DICT)
    print(json.dumps(resultado, indent=4))
    # return pytesseract.image_to_string(imagem_tratada, lang='por', config=CONFIG_TESSERACT)
    return pytesseract.image_to_string(imagem_tratada, lang='por')


def _apply_ocr_image(image) -> str:
    texto = _extract_text(image)
    return texto


def _apply_ocr_in_images(imagens: list) -> str:
    textos_extraidos: list[str] = []

    for i in range(len(imagens)):
        texto = _extract_text(imagens[i])
        textos_extraidos.append(texto)

    return " ".join(textos_extraidos)


class AzOptipy:
    def __init__(self, reader: Reader) -> None:
        self._type_file, self._images = reader.get_images_for_OCR()

    def precess_ocr(self) -> Union[str, ValueError]:
        is_pdf = self._type_file == FileType.PDF
        is_img = self._type_file == FileType.IMG

        try:
            
            if is_pdf:
                return _apply_ocr_in_images(self._images)
            elif is_img:
                return _apply_ocr_image(self._images)
        except Exception as e:
            print(f"Erro ao ler imagem: {e}")

    # def image_to_pdf_searchable(self):
    #     pdf = pytesseract.image_to_pdf_or_hocr(self._path, extension='pdf')
    #     with open('test.pdf', 'w+b') as f:
    #         f.write(pdf)  # pdf type is bytes by default
