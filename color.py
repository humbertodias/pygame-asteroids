# coding: utf-8

import random
import pygame as pg


class Color:
    """
    Representa cor
    """
    WHITE = (255, 255, 255)
    """
    Branco
    """
    RED = (255, 0, 0)
    """
    Vermelho
    """
    GREEN = (0, 255, 0)
    """
    Verde
    """
    BLACK = (0, 0, 0)
    """
    Preto
    """

    YELLOW = (255,255, 0)
    """
    Amarelo
    """

    BLUE = (68, 204, 230)
    """
    Azul
    """

    TRANSPARENT = (255,255,255,0)
    """
    Transparente
    """
    PINK = (255, 0, 255, 255)
    """
    Rosa
    """

    GRAY = (228,228,228)
    """
    Cinza
    """

    @staticmethod
    def hex_to_rgb(value):
        """
        Hexadecimal para RGB
        @param value: Valor hexadecimal
        @return: Cor RGB
        """
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    @staticmethod
    def rgb_to_hex(rgb):
        """
        Converte cor rgb em hexadecimal
        @param rgb: Cor rgb
        @return: Cor Hexadecimal
        """
        return '#%02x%02x%02x' % rgb

    @staticmethod
    def random_color():
        """
        Retorna cor aleatória

        @return: Cor (r,g,b)
        """
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        return (r, g, b)

    @staticmethod
    def color_replace(surface, find_color, replace_color):
        """
        Substitui cor da image
        @param surface:  Imagem
        @param find_color: Cor a procurar
        @param replace_color:  Cor a substituir
        @return: Image Modificada
        """
        image = surface.copy()
        width, height = image.get_size()
        for x in range(width):
            for y in range(height):
                pixel_color = image.get_at([x, y])
                # cor encontrada, troque-a
                if pixel_color == find_color:
                    image.set_at([x, y], replace_color)
        return image
