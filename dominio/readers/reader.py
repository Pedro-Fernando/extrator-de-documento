import abc


class Reader(abc.ABC):
    @abc.abstractmethod
    def get_images_for_OCR(self):
        ...
