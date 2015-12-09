# coding: utf-8

import math
import pygame_sdl2 as pg

from color import *
from sprite_collision import *
from bullet import *
from resource import *

class Ship(SpriteCollision,pg.sprite.Sprite):

    """
    Nave
    """
    SPEED_ACCELERATE = 0.025
    """
    Velociadade de aceleração
    """

    SPEED_ROTATE = 0.4
    """
    Velocidade de rotação
    """

    TIME_LOAD = 200.0
    """
    Tempo para carregar
    """

    TIME_RELOAD_SHOT = 100
    """
    Tempo para recarregar
    """

    def __init__(self, location, game_controller, *groups):
        """
        Construtor
        @param location:
        @param game_controller:
        @param groups:
        @return: Instância
        """
        super(Ship,self).__init__(*groups)
        self.game_controller = game_controller
        self.originalimage = game_controller.asset_manager.get_image("ship.png").convert_alpha()
        self.rect=pg.rect.Rect(location,(self.originalimage.get_width(),self.originalimage.get_height()))
        (self.rect.centerx,self.rect.centery)=location

        self.original_fire_image = game_controller.asset_manager.get_image("fire.png").convert()
        self.explotion_image = game_controller.asset_manager.get_image("explosion1.png").convert_alpha()


        self.angle = 0.0
        self.speedx = 0
        self.speedy = 0
        self.shot = 0
        self.load=self.TIME_LOAD
        self.invincibility=0.0
        self.alive=1
        # ponto central
        (self.x,self.y)=self.rect.center
        self.initrect(location, self.game_controller)


    def accelerate(self, angle):
        self.speedx,self.speedy=self.accelerate_speed(angle,self.speedx,self.speedy)

    def accelerate_speed(self,angle,x,y):
        """
        Acelerar
        @param angle: Ângulo
        @param x: Posição X
        @param y: Posição Y
        """

        if not pg.mixer.get_busy():
            self.game_controller.asset_manager.play_sound('accelerate.wav')


        realangle=angle+90
        if realangle>360:
            realangle-=360.0
        realangle*=math.pi/180
        rady=-math.sin(realangle)
        radx=math.cos(realangle)
        if (rady<0 and not y<-0.5) or (rady>0 and not y>0.5):
            y+=rady*self.SPEED_ACCELERATE
        if (radx<0 and not x<-0.5) or (radx>0 and not x>0.5):    
            x+=radx*self.SPEED_ACCELERATE

        return x,y

    def shoot(self):
        """
        Atirar
        """

        if self.load>=self.TIME_RELOAD_SHOT:
            Bullet(self.rect.center, self.angle, self.game_controller, self.game_controller.sprites)
            self.load=0.0

            self.game_controller.asset_manager.play_sound('laser_shoot.wav')

    def get_center(self):
        rce = self.rect.center
        rce = (rce[0] - self.explotion_image.get_width()/2, rce[1] - self.explotion_image.get_height()/2)
        return rce

    def explode(self,time):
        """
        Explidir nave
        @param time: Delta Time
        """

        # if not pg.mixer.get_busy():
        self.game_controller.asset_manager.play_sound('explosion.wav')

        # centraliza
        self.game_controller.screen.blit(self.explotion_image, self.get_center() )


        if self.game_controller.life>0 and self.alive:
            self.invincibility=2000.0
            self.angle=0.0
            self.speedx=0
            self.speedy=0
            self.load=self.TIME_LOAD
            (self.x,self.y)=(self.game_controller.width / 2, self.game_controller.height / 2)
            self.game_controller.life-=1
            self.image=pg.transform.rotate(self.originalimage, self.angle)
            self.rectupdate()
        else:
            self.game_controller.gameover=1
            self.alive=0
            self.kill()

    def left(self, time):
        self.angle+= self.SPEED_ROTATE * time
        if self.angle>360.0:
            self.angle-=360.0

    def right(self, time):
        self.angle-= self.SPEED_ROTATE * time
        if self.angle<0.0:
            self.angle+=360.0

    def up(self):
        self.accelerate(self.angle)


    def rotate(self, angle):
        self.angle = angle

    def update(self,time):
        """
        Atualizar
        @param time: Delta Time
        """

        if self.load < self.TIME_LOAD:
            self.load+=time

        self.x+=self.speedx*time
        self.y+=self.speedy*time
        self.rect.center=(self.x,self.y)

        if self.invincibility>0.0:
            self.invincibility-=time

            for i in range(40):
                if self.invincibility<=i*50 and self.invincibility>(i-1)*50 and i%2==0:
                    self.rect.center=(self.x,self.y)
                    self.image=pg.transform.rotate(self.originalimage, self.angle)
                    self.rect = self.image.get_rect(center=self.rect.center)
                    break
                elif self.invincibility<=i*50 and self.invincibility>(i-1)*50 and i%2!=0:
                    self.image=pg.Surface((self.rect.width,self.rect.height)).convert_alpha()
                    self.image.fill(Color.TRANSPARENT)
        else:
            self.image = pg.transform.rotate(self.originalimage, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        self.screencollision(time)
