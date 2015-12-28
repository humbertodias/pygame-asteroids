# coding=utf-8

import pygame as pg
import random, collections, sys

import credit
from font import *
from color import *
from resource import *
from virtual_controller import *

class MenuItem(pg.font.Font):
    """
    Item de Menu
    """
    # https://www.python.org/dev/peps/pep-3113/ python2to3 unpacking parameters
    def __init__(self, text, padding_y=0, font_path=None, font_size=Font.SMALL, font_color=Color.WHITE, pos_x_pos_y=(0,0) ) :
        """
        Construtor
        @param text:
        @param padding_y:
        @param font_path:
        @param font_size:
        @param font_color:
        @param pos_x_pos_y:
        @return: Instância
        """
        pg.font.Font.__init__(self, font_path, font_size)
        self.text = text
        self.font_color = font_color
        self.size = font_size
        self.padding_y = padding_y
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        # evitando erro: AttributeError: attribute 'height' of '_freetype.Font' objects is not writable
        # self.height = self.label.get_rect().height + padding_y
        self.dimensions = (self.width, self.height)
        self.pos_x, self_y = pos_x_pos_y
        self.position = pos_x_pos_y

    def is_mouse_selection(self, posx_posy):
        """
        Seleção feita pelo mouse?
        @param posx_posy: Posição a verificar
        @return: boolean
        """
        posx, posy = posx_posy
        return (posx >= self.pos_x and posx <= self.pos_x + self.width) and (posy >= self.pos_y and posy <= self.pos_y + self.height)
 
    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y
 
    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)

    def get_font_color(self):
        return self.font_color

class Menu():
    """
    Menu
    """
    def __init__(self, game_controller, items, funcs, padding_y=0, padding_item_y=0, bg_color=Color.BLACK, select_color=Color.GREEN, font_path=None, font_size=Font.SMALL, font_color=Color.WHITE):
        """
        Construtor
        @param game_controller:
        @param items:
        @param funcs:
        @param padding_y:
        @param padding_item_y:
        @param bg_color:
        @param select_color:
        @param font_path:
        @param font_size:
        @param font_color:
        @return: Instância
        """
        self.game_controller = game_controller
        self.screen = game_controller.screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.padding_y = padding_y
        self.padding_item_y = padding_item_y
        self.bg_color = bg_color
        self.select_color = select_color
        self.done = False

        self.font_path = font_path
        self.font_size = font_size

        self.funcs = funcs
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item, self.padding_item_y, self.font_path, self.font_size, font_color)
 
            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            # This line includes a bug fix by Ariel (Thanks!)
            # Please check the comments section of pt. 2 for an explanation
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index*2) + index * menu_item.height) + self.padding_y
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
 
        self.mouse_is_visible = game_controller.config.show_mouse
        self.cur_item = None

        if len(self.items) > 0:
            self.set_keyboard_selection(self.items[0])

    def back(self):
        self.done = True

    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pg.mouse.set_visible(True)
        else:
            pg.mouse.set_visible(False)
    
    def set_keyboard_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys.
        """
        for item in self.items:
            # Return all to neutral
            item.set_font_color(Color.WHITE)
 
        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chosen item
            if key == pg.K_UP:
                if self.cur_item > 0:
                    self.cur_item -= 1
                elif self.cur_item == 0:
                    self.cur_item = len(self.items) - 1
            elif key == pg.K_DOWN:
                if self.cur_item < len(self.items) - 1:
                    self.cur_item += 1
                elif self.cur_item == len(self.items) - 1:
                    self.cur_item = 0


        old_color = self.items[self.cur_item].font_color
        if old_color != self.select_color:
            self.items[self.cur_item].set_font_color(self.select_color)
        else:
            self.items[self.cur_item].set_font_color(Color.WHITE)

        # Finally check if Enter or Space is pressed
        if key == pg.K_SPACE or key == pg.K_RETURN:
            text = self.items[self.cur_item].text
            self.funcs[text]()


    def set_mouse_selection(self, item, mpos):
        """Marks the MenuItem the mouse cursor hovers on."""
        is_mouse_hover = item.is_mouse_selection(mpos)

        if self.cur_item == None:
            if is_mouse_hover:

                if item.get_font_color() != self.select_color:
                    self.play_hover_sound()

                item.set_font_color(self.select_color)
            else:
                item.set_font_color(Color.WHITE)

    def play_hover_sound(self):
        self.game_controller.asset_manager.play_sound('hover.wav')

    def play_enter_sound(self):
        self.game_controller.asset_manager.play_sound('enter.wav')

    def draw(self, draw_callback_func=None):
        """
        Desenhar
        @param draw_callback_func:
        """
        mpos = pg.mouse.get_pos()

        for event in pg.event.get():

            if event.type == pg.QUIT:
                # mainloop = False
                self.game_controller.quit()
            if event.type == pg.KEYDOWN:
                self.mouse_is_visible = False
                self.set_keyboard_selection(event.key)

            if event.type == pg.JOYBUTTONDOWN:
                joy_key = decode_joystick_arrow_to_keyboard_key(self.game_controller.joystick)
                if joy_key :
                    self.mouse_is_visible = False
                    self.set_keyboard_selection(joy_key)

            if event.type == pg.MOUSEBUTTONDOWN:
                for item in self.items:
                    if item.is_mouse_selection(mpos):
                        self.play_enter_sound()
                        self.funcs[item.text]()

        if pg.mouse.get_rel() != (0, 0):
            self.mouse_is_visible = True
            self.cur_item = None

        # self.set_mouse_visibility()

        # Redraw the background
        self.screen.fill(self.bg_color)

        if draw_callback_func != None:
            draw_callback_func(self.screen)

        for item in self.items:
            if self.mouse_is_visible:
                self.set_mouse_selection(item, mpos)
            self.screen.blit(item.label, item.position)

        self.game_controller.show_fps()

        # atualiza
        pg.display.flip()

    def run(self, fps, draw_callback_func=None):
        while not self.done:
            # Limit frame per second
            time = self.game_controller.clock.tick(fps)
            self.draw(draw_callback_func)

class MainMenu:
    """
    Menu Principal
    """

    def __init__(self, game_controller, call_back_function=None):
        """
        Construtor
        @param game_controller:
        @param call_back_function:
        @return: Instância
        """
        self.game_controller = game_controller
        # associar referência ao controller
        self.game_controller.main_menu = self
        self.screen = game_controller.screen
        self.scoredat = game_controller.score_data
        self.fps = game_controller.config.fps
        self.call_back_function = call_back_function

        self.font_name = game_controller.asset_manager.get_font_default_name()
        self.font_path = game_controller.asset_manager.get_font_path(self.font_name)
        self.font_size = Font.NORMAL

        self.fontsmall  = game_controller.asset_manager.get_font(Font.SMALL)
        self.fontnormal = game_controller.asset_manager.get_font(Font.NORMAL)
        self.fontlarge  = game_controller.asset_manager.get_font(Font.LARGE)

        self.menu = self.create_main_menu()

    def run(self):
        self.menu.run(self.fps, self.call_back_function)

    def create_main_menu(self):
        """
        Cria menu principal
        """
        funcs = collections.OrderedDict()
        funcs['Jogar'] = self.play
        funcs['Placar'] = self.high_score
        funcs['Como Jogar'] = self.how_to_play
        funcs['Créditos'] = self.credits
        funcs['Sair'] = self.game_controller.quit

        return Menu(self.game_controller, funcs.keys(), funcs, self.screen.get_height()/2-120, 10, Color.BLACK, Color.GREEN, self.font_path, self.font_size, font_color=Color.WHITE)



    def play(self):
        """
        Jogar
        """
        self.game_controller.main(self.screen)

    def high_score(self, position_to_hightlight=None):
        """
        Placar
        """

        def callback_high_score(sc):
            scoretitle=[' ','Nome','Pontos']
            scoretitletext=self.fontlarge.render("Pontuação",True, Color.WHITE)
            sc.blit(scoretitletext,(self.game_controller.width/2-scoretitletext.get_width()/2,80-scoretitletext.get_height()/2))

            hy = 130
            scoretitletext=self.fontsmall.render(scoretitle[0],True,Color.GREEN)
            sc.blit(scoretitletext,(100-scoretitletext.get_width(),hy))
            scoretitletext=self.fontsmall.render(scoretitle[1],True,Color.GREEN)
            sc.blit(scoretitletext,(128,hy))
            scoretitletext=self.fontsmall.render(scoretitle[2],True,Color.GREEN)
            sc.blit(scoretitletext,(self.game_controller.width-128-scoretitletext.get_width(),hy))

            for i in range(len(self.scoredat.hiscore)):

                if i == position_to_hightlight:
                    color = Color.GREEN
                else:
                    color = Color.WHITE

                scorenumber = self.fontsmall.render(str(i+1)+'  ', True, color)
                scorename   = self.fontsmall.render(self.scoredat.hiscorename[i] ,True,color)
                scorescore  = self.fontsmall.render(str(self.scoredat.hiscore[i]),True,color)
                sc.blit(scorenumber,(128-scorenumber.get_width(),176+28*i))
                sc.blit(scorename,(128,176+28*i))
                sc.blit(scorescore,(self.game_controller.width-128-scorescore.get_width(),176+28*i))

        funcs = collections.OrderedDict()
        funcs['Voltar'] = None

        sub_menu = Menu(self.game_controller, funcs.keys(), funcs,220, 10, Color.BLACK, Color.GREEN, self.font_path, self.font_size, font_color=Color.WHITE )
        funcs['Voltar'] = sub_menu.back

        sub_menu.run(self.fps, callback_high_score)


    def how_to_play(self):
        """
        Como Jogar
        """

        self.image = self.game_controller.asset_manager.get_scalled_image('how_to_play.png', 0.5).convert_alpha()

        def callback_how_to_play(sc):
            scoretitletext=self.fontlarge.render("Como Jogar",True, Color.WHITE)
            sc.blit(scoretitletext,(self.game_controller.width/2-scoretitletext.get_width()/2,80-scoretitletext.get_height()/2))

            sc.fill(Color.BLACK)
            sc.blit(self.image, (self.game_controller.width/2-self.image.get_width()/2,(self.game_controller.height/2-self.image.get_height()/2)))


        funcs = collections.OrderedDict()
        funcs['Voltar'] = None

        sub_menu = Menu(self.game_controller, funcs.keys(), funcs, 220, 10, Color.BLACK, Color.GREEN, self.font_path, self.font_size, font_color=Color.WHITE )
        funcs['Voltar'] = sub_menu.back

        sub_menu.run(self.fps, callback_how_to_play)


    def credits(self):
        """
        Créditos
        """
        self.logos = []
        self.logos.append( self.game_controller.asset_manager.get_scalled_image('pygame.png', 0.5).convert_alpha() )
        self.logos.append( self.game_controller.asset_manager.get_scalled_image('pycharm.png', 0.5).convert_alpha() )
        self.logos.append( self.game_controller.asset_manager.get_scalled_image('gimp.png', 0.5).convert_alpha() )
        self.logos.append( self.game_controller.asset_manager.get_scalled_image('inkscape.png', 0.5).convert_alpha() )
        self.logos.append( self.game_controller.asset_manager.get_scalled_image('audacity.png', 0.5).convert_alpha() )

        self.y = 0
        def callback_credits(sc):

            for i, logo in enumerate(self.logos):
                x = self.game_controller.width - logo.get_width()
                sc.blit(logo, (x,self.y + i * 100) )
            self.y += 1

            if self.y > self.game_controller.height:
                self.y = -self.game_controller.height

        self.screen.fill(Color.GRAY)

        credit.credit_from_file('resource/text/credits.txt', self.fontsmall, Color.BLACK, 15, callback_credits)
