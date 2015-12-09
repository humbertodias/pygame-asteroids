# coding: utf-8

import pygame_sdl2 as pg
import math

def is_event_type_an_input_down(event):
    if type(event) is list:
        for evt in event:
            if is_event_type_an_input_down(evt):
                return True
        return False

    return event.type in (pg.KEYDOWN, pg.MOUSEBUTTONDOWN, pg.JOYBUTTONDOWN, pg.QUIT, pg.K_ESCAPE)


def decode_joystick_arrow_to_keyboard_key(joystick):
    key = None

    if joystick:
        # 7 = left
        if joystick.get_button(7):
            key = pg.K_LEFT
        # 5 = right
        if joystick.get_button(5):
            key = pg.K_RIGHT
        # 6 = down
        if joystick.get_button(6):
            key = pg.K_DOWN
        # 4 = up
        if joystick.get_button(4):
            key = pg.K_UP
        # 14 = X
        if joystick.get_button(14):
            key = pg.K_UP
        # 15 = Quadrado
        if joystick.get_button(15):
            key = pg.K_SPACE

    return key



def vc_get_angle(center, pos):
    """
    @param pos: posição do mouse
    @return: ângulo em raidanos da posição do mouse em relação ao centro informado.
    Controle Virtual é dividido em três partes.
    Para o eixo-y :
    1) above the center of the controller
    2) below the center of the controller
    3) at the same height of the center of the controller
    If the mouse point is above the center of the controller, than check
    for one of three conditions:
    1) x is to the right of the controller
    2) x is to the left of the controller
    3) x is at the same point as the centerx of the controller
    """
    x,y = pos
    rad = 0.0
    if y < center[1]:

        if x > center[0]:
            opposite = float(center[1] - y)
            adjacent = float(x - center[0])
            rad = math.atan(opposite/adjacent)
        elif x < center[0]:
            opposite = float(center[0] - x)
            adjacent = float(center[1] - y)
            rad = .5 * math.pi + (math.atan(opposite/adjacent))
        else:
            rad = 0.5 * math.pi

    elif y > center[1]:
        if x < center[0]:
            opposite = float(y - center[1])
            adjacent = float(center[0] - x)
            rad = math.pi + (math.atan(opposite/adjacent))
        elif x > center[0]:
            adjacent = float(y - center[1])
            opposite = float(x - center[0])
            rad = (1.5 * math.pi) + math.atan(opposite/adjacent)
        else:
            rad = 1.5 * math.pi
    else:
        if x < center[0]:
            rad = math.pi
    return rad