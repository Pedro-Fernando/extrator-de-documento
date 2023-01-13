import cv2

from dominio.enums.types import FileType
from dominio.readers.reader import Reader


class ImgReader(Reader):
    def __init__(self, path):
        self._path = path

        try:
            self._images = cv2.imread(self._path)

        except Exception as e:
            print(f"Erro ao ler imagem: {e}")

    def get_images_for_OCR(self):
        return FileType.IMG, self._images
