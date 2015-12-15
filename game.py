# coding: utf-8

import random, sys
import pygame as pg

from font import *
from resource import *

from asteroid import *
from ship import *
from color import *


from file import *
from start_field import *

from virtual_keyboard import *
from virtual_controller import *


class Game:
    def __init__(self, map):
        self.map = map
        self.width = int(map.get('janela')[0][0])
        self.height = int(map.get('janela')[0][1])
        self.life = int(map.get('vidas')[0][0])
        self.fps = int(map.get('passo_simulacao')[0][0])
        self.asteroids = map.get('asteroide')
        self.controle = 'keyboard'
        if map.get('controle'):
            self.controle = map.get('controle')[0][0]

        self.full_screen = False
        if map.get('tela_cheia'):
            self.full_screen = map.get('tela_cheia')[0][0] == 'True'

        self.show_mouse = True
        if map.get('mostrar_mouse'):
            self.show_mouse = map.get('mostrar_mouse')[0][0] == 'True'

        self.sound = True
        if map.get('sound'):
            self.sound = map.get('sound')[0][0] == 'True'

    @staticmethod
    def create_empty_actions():
        actions = {}
        actions['left']=0
        actions['right']=0
        actions['accelerate']=0
        actions['shoot']=0
        return actions


from touch_buttons import *

class GameController(object):
    """
    Controlador do Jogo
    """
    running=0
    newhiscore=0

    def __init__(self, game_name, screen, file_manager, asset_manager, config, score_data):
        """
        Construtor
        @param screen:
        @param file_manager:
        @param asset_manager:
        @param config:
        @param score_data:
        """
        self.fps_visible = True
        self.game_name = game_name
        self.screen = screen
        self.file_manager = file_manager
        self.asset_manager = asset_manager
        self.score_data = score_data

        self.config = config
        self.width = config.width
        self.height = config.height
        self.life = config.life
        self.fps = config.fps

        self.font_very_small = asset_manager.get_font(Font.VERY_SMALL)
        self.font_small  = asset_manager.get_font(Font.SMALL)
        self.font_normal = asset_manager.get_font(Font.NORMAL)
        self.font_large  = asset_manager.get_font(Font.LARGE)

        # self.background_image = self.asset_manager.get_image('background.png').convert()

        self.clock = pg.time.Clock()

        if self.config.controle == 'joystick':
            self.initialize_joystick()

    def screen_rect(self):
        """
        Retangulo com o tamanho da tela
        @return: Retangulo
        """
        return pg.Rect((0,0), (self.width, self.height) )


    def show_fps(self):
        """
        Display the current FPS in the window handle if fps_visible is True.
        """
        if self.fps_visible:
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.game_name, fps)
            pg.display.set_caption(with_fps)

    def announcelevel(self,time,screen):
        """
        Mostrar na tela o nível
        @param time: Delta time
        @param screen: Tela
        """
        self.leveltimer-=time
        leveltext=self.font_large.render('Onda ' + str(self.level), True, Color.WHITE)
        screen.blit(leveltext,(self.width/2-leveltext.get_width()/2, (self.height/2-leveltext.get_height()/2)+50 ))

    def create_asteroids(self):
        """
        Criar asteroids
        """

        for arr in self.config.asteroids:
            angle=0

            # última linha do arquivo de entrada
            if arr[0] == arr[1] == arr[2] == '0':
                break

            location = (int(arr[0]), int(arr[1]))
            img_width = 24
            size = int(arr[2]) // img_width
            to_color = Color.hex_to_rgb( arr[3] )

            # evitar asteroid muito pequeno
            if size < 1:
                size = 1

            angle = random.randrange(360) + 1
            Asteroid( location
                     , size
                     , angle
                     , self
                     , Color.PINK
                     , to_color
                     , self.sprites
                     , self.asteroids)


        # adiciona aleatorios de acordo com o nível do jogador
        adicionais = self.create_random_asteroids(self.level-1)
        for a in adicionais:
            Asteroid( a.location
                    , a.size
                    , a.angle
                    , self
                    , a.from_color
                    , a.to_color
                    , self.sprites
                    , self.asteroids)

    def random_position(self):
        x=random.randrange(self.width)
        y=random.randrange(self.height)
        return (x,y)

    def create_random_asteroids(self, count):
        """
        Cria asteroids aleatoriamente
        @param self:
        @return: asteroids
        """

        lasteroids = []
        for i in range(count):
            lasteroids.append(
                Asteroid(self.random_position()
                     , 3
                     , random.randrange(360)+1
                     , self
                     , Color.PINK
                     , Color.random_color()
                     ,[]
                     ,[])
            )
        return lasteroids


    def draw_hud(self, screen, time):
        """
        Desenha head-up display
        @param screen: Tela
        """
        screen.blit(self.scoretext,(self.width-20-self.scoretext.get_width(),10))
        scoredisplay=self.font_small.render(str(self.score), True, Color.WHITE)

        # vidas
        for i in range(self.life):
            screen.blit(self.lifeimg,(15+20*i,20))

        screen.blit(scoredisplay,(self.width-20-scoredisplay.get_width(), scoredisplay.get_height()+5 ) )

        # left
        centerdisplay=self.font_small.render("Asteróides:" + str(len(self.asteroids)), True, Color.WHITE)
        screen.blit(centerdisplay,( (self.width - centerdisplay.get_width())/2, (self.height - centerdisplay.get_height()) ))

        # fps
        self.show_fps()

    def get_user_score_on_ranking(self):
        scoredat = self.score_data
        for i in range(len(scoredat.hiscore)):
            if self.score > scoredat.hiscore[i]:
                return i
        return -1


    def save_score(self, user_name):
        scoredat = self.score_data
        for i in range(len(scoredat.hiscore)):
            if self.score>scoredat.hiscore[i]:
                self.newhiscore=1
                for ii in range(len(scoredat.hiscore)-i):
                    iii=9-ii
                    scoredat.hiscore[iii]=scoredat.hiscore[iii-1]
                    scoredat.hiscorename[iii]=scoredat.hiscorename[iii-1]
                scoredat.hiscore[i]=self.score
                scoredat.hiscorename[i]=user_name
                scoredat.rank=i
                break

        py_version = str(sys.version_info[0])
        score_file_name = 'score_py' + py_version + '.dat'

        self.file_manager.marshal(score_file_name, self.score_data)

    def draw_game_over(self, screen, event, time):
        """
        Desenhar fim de jogo
        @param screen: Tela
        @param event: Evento
        @param time: Delta Time
        """
        game_over_text=self.font_large.render('Fim de Jogo', True, Color.WHITE)
        screen.blit(game_over_text,(self.width/2-game_over_text.get_width()/2,self.height/2-game_over_text.get_height()/2))

        if self.gameovertimer>0.0:
            self.gameovertimer-=time
        else:

            position_ranking = self.get_user_score_on_ranking()

            if position_ranking != -1:

                screen.fill(Color.BLACK)

                def draw_callback_new_record(sc):
                    new_record_text=self.font_normal.render("Novo Recorde %.2f!" % (self.score), True, Color.GREEN)
                    pos_xy = (self.width/2-new_record_text.get_width()/2,100)
                    sc.blit(new_record_text,pos_xy)

                    new_record_text=self.font_normal.render("Informe seu nome.", True, Color.YELLOW)
                    pos_xy = (self.width/2-new_record_text.get_width()/2,130)
                    sc.blit(new_record_text,pos_xy)

                vkeyboard = VirtualKeyboard()
                user_name = vkeyboard.run(screen, self.font_normal, "", draw_callback_new_record)

                self.save_score(user_name)
                self.running = False

                self.main_menu.high_score(position_ranking)


            else:
                if is_event_type_an_input_down(event):
                    self.running = False


    def get_display_center(self):
        info = pg.display.Info()
        return (info.current_w/2, info.current_h/2)


    def initialize_joystick(self):
        # Count the joysticks the computer has
        self.joystick_count = pg.joystick.get_count()
        if self.joystick_count == 0:
            # No joysticks!
            print("Error, I didn't find any joysticks.")
        else:
            # Use joystick #0 and initialize it
            self.joystick = pg.joystick.Joystick(0)
            self.joystick.init()

    def main(self, screen):

        self.leveltimer = 500.0
        self.score = 0
        self.gameover = 0

        self.clock = pg.time.Clock()
        self.running = 1
        self.sprites = SpriteGroup()
        self.asteroids = SpriteGroup()

        self.player=Ship((self.width/2,self.height/2), self, self.sprites)

        self.background=pg.surface.Surface((self.width,self.height))
        # self.background = self.asset_manager.get_image('background.png').convert_alpha()

        self.scoretext=self.font_small.render('Pontos', True, Color.WHITE)
        self.level = 1
        self.levelstart = 0
        self.life = self.config.life
        self.lifeimg = self.asset_manager.get_image('ship.png').convert_alpha()
        self.lifeimg = pg.transform.scale(self.lifeimg,(int(self.lifeimg.get_width()/3), int(self.lifeimg.get_height()/3) ))
        self.gameovertimer = 1500.0
        self.newhiscore = 0


        self.asset_manager.play_music('game.mp3', -1)

        center = self.get_display_center()

        touch_buttons = TouchButtons(screen, 70)

        self.start_field = StarField(self.screen)

        actions = Game.create_empty_actions()
        while self.running:
            time = self.clock.tick(self.config.fps)

            if self.config.controle != 'touch':
                actions = Game.create_empty_actions()

            if self.config.controle == 'mouse':

                mpos = pg.mouse.get_pos()
                rad = vc_get_angle(center, mpos)

                # +90 graus por conta do bico da nave na vertical
                angle = math.degrees(rad) + 90
                self.player.rotate(angle)

                buttons = pg.mouse.get_pressed()
                # first/left button
                if buttons[0]:
                    actions['shoot']=1
                # third/right button
                if buttons[2]:
                    self.player.accelerate(angle)

            elif self.config.controle == 'joystick':

                key = decode_joystick_arrow_to_keyboard_key(self.joystick)
                if key==pg.K_LEFT:
                    actions['left']=1
                if key==pg.K_RIGHT:
                    actions['right']=1
                if key==pg.K_UP:
                    actions['accelerate']=1
                if key==pg.K_SPACE:
                    actions['shoot']=1


            elif self.config.controle == 'keyboard':
                # teclado

                key=pg.key.get_pressed()
                if key[pg.K_LEFT]:
                    actions['left']=1
                if key[pg.K_RIGHT]:
                    actions['right']=1
                if key[pg.K_UP]:
                    actions['accelerate']=1
                if key[pg.K_SPACE]:
                    actions['shoot']=1

            events = pg.event.get()
            for event in events:

                if event.type==pg.QUIT:
                    self.quit()
                if event.type==pg.KEYDOWN and not self.gameover:
                    if event.key==pg.K_ESCAPE:
                        self.quit()

                if self.config.controle == 'touch':
                    ## Check to see if the mousebutton is pressed
                    actions = touch_buttons.detect_actions(event, actions)

            screen.blit(self.background,(0,0))

            self.start_field.draw()


            # 7 = left
            if actions['left']:
                self.player.left(time)
            # 5 = right
            if actions['right']:
                self.player.right(time)
            # 15 = Quadrado
            if actions['shoot']:
                self.player.shoot()
            # 14 = X
            if actions['accelerate']:
                self.player.up()


            self.sprites.update(time)

            self.sprites.draw(screen)
            self.sprites.draw2(screen)

            if self.leveltimer>0.0:
                self.announcelevel(self.clock.tick(self.config.fps),screen)
                self.levelstart=0

            elif self.levelstart==0:
                self.create_asteroids()
                self.levelstart=1

            if len(self.asteroids)==0 and self.levelstart!=0:
                self.leveltimer=500.0
                self.level+=1

            self.draw_hud(screen, time)
            if self.config.controle == 'touch':
                touch_buttons.draw()
            if self.gameover:
                self.draw_game_over(screen, event, time)

            pg.display.flip()

    def quit(self):
        self.running=0
        """
        Sair do jogo
        """
        pg.quit()
        sys.exit()


class SpriteGroup(pg.sprite.Group):
    """
    Agrupado de Sprites
    """
    def draw2(self,screen):
        """
        Desenhar na tela
        @param screen: Tela
        """
        for sprite in self.sprites():
            sprite.draw2(screen)
