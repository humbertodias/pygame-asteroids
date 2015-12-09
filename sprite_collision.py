# coding: utf-8

import pygame_sdl2 as pg

class SpriteCollision:
    """
    Classe principal que controla sprite e aplicada a todos os objetos em movimento
    """

    def initrect(self, location, game_controller):
        """
        Iniciliza retângulo
        @param location:
        @param game_controller:
        """
        self.game_controller = game_controller
        self.horrect=pg.Rect.copy(self.rect)
        self.verrect=pg.Rect.copy(self.rect)
        self.diarect=pg.Rect.copy(self.rect)

        if self.get_class_name()=='Ship':
            for i in (self.horrect,self.verrect,self.diarect):
                i.width*=1/2
                i.height*=1/2
        self.rectupdate()

    def get_class_name(self):
        """
        Retorna nome da classe instanciada
        @return: Nome
        """
        return self.__class__.__name__

    def screencollision(self,time):
        """
        Envolve a tela do jogo para objetos
        @param time: Delta time
        """
        if self.x>self.game_controller.width:
            self.x-=self.game_controller.width
        elif self.x<0:
            self.x+=self.game_controller.width
        if self.y>self.game_controller.height:
            self.y-=self.game_controller.height
        elif self.y<0:
            self.y+=self.game_controller.height
        self.rect.center=(self.x,self.y)
        self.rectupdate()

    def rectupdate(self):
        """
        define qual borda colide com o objeto de colisão / blitting
        """
        self.horrect.center=self.rect.center
        self.verrect.center=self.rect.center
        self.diarect.center=self.rect.center
        x=self.rect.centerx
        y=self.rect.centery
        self.corleft,self.corright,self.corup,self.cordown=0,0,0,0

        if self.rect.left<0:
            self.corleft=1
            self.horrect.center=(x + self.game_controller.width, y)
        elif self.rect.right>self.game_controller.width:
            self.corright=1
            self.horrect.center=(x - self.game_controller.width, y)
        if self.rect.top<0:
            self.corup=1
            self.verrect.center=(x,y+self.game_controller.height)
        elif self.rect.bottom>self.game_controller.height:
            self.cordown=1
            self.verrect.center=(x,y-self.game_controller.height)
        if self.corleft+self.cordown+self.corup+self.corright>1:
            self.diarect.center=(x + self.game_controller.width * self.corleft - self.game_controller.width * self.corright, y + self.game_controller.height * self.corup - self.game_controller.height * self.cordown)

    def draw2(self,screen):
        """
        blit de imagens para corrigir os lugares quando perto cantos / lados.
        @param screen: Tela
        """
        x=self.rect.left
        y=self.rect.top
        if self.corleft==1:
            screen.blit(self.image, (x + self.game_controller.width, y))
        elif self.corright==1:
            screen.blit(self.image, (x - self.game_controller.width, y))
        if self.corup==1:
            screen.blit(self.image, (x,y+self.game_controller.height))
        elif self.cordown==1:
            screen.blit(self.image, (x,y-self.game_controller.height))
        screen.blit(self.image,(x,y))
        if self.corleft+self.cordown+self.corup+self.corright>1:
            screen.blit(self.image, (x + self.game_controller.width * self.corleft - self.game_controller.width * self.corright, y + self.game_controller.height * self.corup - self.game_controller.height * self.cordown))

    def collision(self,object):
        """
        Detecta colisão
        @param object: Objeto
        @return: Booleano
        """
        rect=[self.rect,self.horrect,self.verrect,self.diarect]
        objectrect=[object.rect,object.horrect,object.verrect,object.diarect]
        for i in rect:
            for ii in objectrect:
                if i.colliderect(ii):
                    return True

        return False

