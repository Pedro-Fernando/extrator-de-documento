import cv2
import numpy as np


def _exibir_imagem(imagem):
    cv2.namedWindow('Imagem alterada', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Imagem alterada', 800, 600)
    cv2.imshow('Imagem alterada', imagem)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


class ImagemProcessor:

    @staticmethod
    def color_rgb(imagem):
        imagem_em_rgb = cv2.cvtColor(np.array(imagem), cv2.COLOR_BGR2BGRA)
        # _exibir_imagem(imagem_em_rgb)
        return imagem_em_rgb

    @staticmethod
    def img_color_rgb(imagem):
        imagem_em_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2BGR)
        # _exibir_imagem(imagem_em_rgb)
        return imagem_em_rgb

    @staticmethod
    def color_gray(imagem):
        imagem_acinzentada = cv2.cvtColor(np.array(imagem), cv2.COLOR_BGR2GRAY)
        # _exibir_imagem(imagem_acinzentada)
        return imagem_acinzentada
