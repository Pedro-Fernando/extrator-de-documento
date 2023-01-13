import base64
from pdf2image import convert_from_bytes

from dominio.readers.reader import Reader
from dominio.enums.types import FileType


def _get_base64_to_pdf_bytes(pdf_base64):
    return base64.b64decode(pdf_base64)


class PDFReader(Reader):
    def __init__(self, path):
        self._path = path

        try:
            with open(self._path, 'rb') as arquivo:
                pdf_base64 = base64.b64encode(arquivo.read())
                pdf_bytes = _get_base64_to_pdf_bytes(pdf_base64)

            self._images = convert_from_bytes(pdf_bytes)

        except Exception as e:
            print(f"Erro ao ler arquivo PDF: {e}")

    def get_images_for_OCR(self):
        return FileType.PDF, self._images
