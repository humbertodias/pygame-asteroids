# -*- coding: utf-8 -*-

import pygame as pg
import codecs
pg.font.init()
from virtual_controller import *

def credit_from_file(file_name, font,color, fps=40, callback = None):
    text = ''
    with codecs.open(file_name, 'r', 'utf-8') as lines:
        for line in lines :
            text += line

    credit(text, font, color, fps, callback)

def credit(text,font,color, fps=40, callback = None):
    """
    Créditos rolando verticalmente
    @param text: Texto
    @param font: Fonte
    @param color: Cor
    """

    try: text = text.decode('utf-8')
    except: pass

    try: color = pg.Color(color)
    except: color = pg.Color(*color)

    clk = pg.time.Clock()

    scr = pg.display.get_surface()
    scrrect = scr.get_rect()
    bg = scr.copy()

    w,h = font.size(' ')
    Rright = scrrect.centerx + w*3
    Rleft  = scrrect.centerx - w*3

    foo = []
    for i,l in enumerate(text.splitlines()):
        a,b,c = l.partition('\\')
        u = False
        if a:
            if a.startswith('_') and a.endswith('_'):
                u = True
                a = a.strip('_')
            rect = pg.Rect((0,0),font.size(a))
            if b: rect.topright = Rleft,scrrect.bottom+h*i
            else: rect.midtop = scrrect.centerx,scrrect.bottom+h*i
            foo.append([a,rect,u])
        u = False
        if c:
            if c.startswith('_') and c.endswith('_'):
                u = True
                c = c.strip('_')
            rect = pg.Rect((0,0),font.size(c))
            rect.topleft = Rright,scrrect.bottom+h*i
            foo.append([c,rect,u])

    y = 0
    while foo and not pg.event.peek(pg.QUIT):

        if callback != None:
            callback(scr)

        # sair se clicar com teclado ou mouse
        if is_event_type_an_input_down(pg.event.get()):
            break

        pg.event.clear()
        y -= 1
        for p in foo[:]:
            r = p[1].move(0,y)

            if r.bottom < 0:
                foo.pop(0)
                continue
            if not isinstance(p[0],pg.Surface):
                if p[2]: font.set_underline(1)
                p[0] = font.render(p[0],1,color)
                font.set_underline(0)
            scr.blit(p[0],r)
            if r.top >= scrrect.bottom:
                break

        clk.tick(fps)
        pg.display.flip()
        scr.blit(bg,(0,0))

    pg.display.flip()



