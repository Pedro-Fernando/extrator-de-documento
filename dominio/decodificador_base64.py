import base64
from pdf2image import convert_from_bytes


# Decodificar o PDF de base64 para bytes
def _get_base64_to_pdf_bytes(pdf_base64):
    return base64.b64decode(pdf_base64)


class Base64ToPDF:

    @staticmethod
    def get_pdf_bytes(pdf_base64):
        return _get_base64_to_pdf_bytes(pdf_base64)

    @staticmethod
    def get_pdf_to_images(pdf_base64):
        pdf_bytes = _get_base64_to_pdf_bytes(pdf_base64)
        return convert_from_bytes(pdf_bytes)
