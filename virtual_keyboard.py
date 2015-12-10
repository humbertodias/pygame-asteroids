# coding: utf-8

import pygame as pg
import time

class TextInput(object):
    ''' Handles the text input box and manages the cursor '''
    def __init__(self, background, screen, font, text, x, y):
        self.x = x
        self.y = y
        self.text = text
        self.width = 800
        self.height = 60        
        # self.font = pg.font.Font(None, 50)
        self.font = font
        self.cursorpos = len(text)
        self.rect = pg.Rect(self.x,self.y,self.width,self.height)
        self.layer = pg.Surface((self.width,self.height),pg.SRCALPHA).convert_alpha()
        self.background = pg.Surface((self.width,self.height),pg.SRCALPHA).convert_alpha()
        self.background.blit(background,(0,0),self.rect) # Store our portion of the background
        self.cursorlayer = pg.Surface((3,50))
        self.screen = screen
        self.cursorvis = True
        
        self.draw()
    
    def draw(self):
        ''' Draw the text input box '''
        self.layer.fill([255, 255, 255, 140])
        color = [0,0,0,200]
        pg.draw.rect(self.layer, color, (0,0,self.width,self.height), 1)        

        # evitando
        # pygame_sdl2.error.error: b'Text has zero width'
        if len(self.text) < 1:
            self.text = ' '

        text = self.font.render(self.text, 1, (0, 0, 0))
        self.layer.blit(text,(4,4))
        
        self.screen.blit(self.background,(self.x, self.y))
        self.screen.blit(self.layer,(self.x,self.y))        
        self.drawcursor()
    
    def flashcursor(self):
        ''' Toggle visibility of the cursor '''
        if self.cursorvis:
            self.cursorvis = False
        else:
            self.cursorvis = True
        
        self.screen.blit(self.background,(self.x, self.y))
        self.screen.blit(self.layer,(self.x,self.y))  
        
        if self.cursorvis:
            self.drawcursor()
        pg.display.flip()
        
    def addcharatcursor(self, letter):
        ''' Add a character whereever the cursor is currently located '''
        if self.cursorpos < len(self.text):
            # Inserting in the middle
            self.text = self.text[:self.cursorpos] + letter + self.text[self.cursorpos:]
            self.cursorpos += 1
            self.draw()
            return
        self.text += letter
        self.cursorpos += 1
        self.draw()   
        
    def backspace(self):
        ''' Delete a character before the cursor position '''
        if self.cursorpos == 0: return
        self.text = self.text[:self.cursorpos-1] + self.text[self.cursorpos:]
        self.cursorpos -= 1
        self.draw()
        return

        
    def deccursor(self):
        ''' Move the cursor one space left '''
        if self.cursorpos == 0: return
        self.cursorpos -= 1
        self.draw()
        
    def inccursor(self):
        ''' Move the cursor one space right (but not beyond the end of the text) '''
        if self.cursorpos == len(self.text): return
        self.cursorpos += 1
        self.draw()
        
    def drawcursor(self):
        ''' Draw the cursor '''

        x = 4 + self.x
        y = 5 + self.y
        # Calc width of text to this point
        if self.cursorpos > 0:
            mytext = self.text[:self.cursorpos]
            text = self.font.render(mytext, 1, (0, 0, 0))
            textpos = text.get_rect()
            x = x + textpos.width + 1
        self.screen.blit(self.cursorlayer,(x,y))    
        

class VirtualKey(object):
    ''' A single key for the VirtualKeyboard '''
    def __init__(self, caption, x, y, w=67, h=67):
        self.x = x
        self.y = y
        self.caption = caption
        self.width = w
        self.height = h
        self.enter = False
        self.bskey = False
        self.font = None
        self.selected = False
        self.dirty = True
        self.keylayer = pg.Surface((self.width,self.height)).convert()
        self.keylayer.fill((0, 0, 0))
        self.keylayer.set_alpha(160)
        # Pre draw the border and store in my layer
        pg.draw.rect(self.keylayer, (255,255,255), (0,0,self.width,self.height), 1)
        
    def draw(self, screen, background, shifted=False, forcedraw=False):
        '''  Draw one key if it needs redrawing '''
        if not forcedraw:
            if not self.dirty: return
        
        myletter = self.caption
        if shifted:
            if myletter == 'SHIFT':
                self.selected = True # Draw me uppercase
            myletter = myletter.upper()
        
        
        position = pg.Rect(self.x, self.y, self.width, self.height)
        
        # put the background back on the screen so we can shade properly
        screen.blit(background, (self.x,self.y), position)      
        
        # Put the shaded key background into my layer
        if self.selected: 
            color = (200,200,200)
        else:
            color = (0,0,0)
        
        # Copy my layer onto the screen using Alpha so you can see through it
        pg.draw.rect(self.keylayer, color, (1,1,self.width-2,self.height-2))                
        screen.blit(self.keylayer,(self.x,self.y))    
                
        # Create a new temporary layer for the key contents
        # This might be sped up by pre-creating both selected and unselected layers when
        # the key is created, but the speed seems fine unless you're drawing every key at once
        templayer = pg.Surface((self.width,self.height))
        templayer.set_colorkey((0,0,0))
                       
        color = (255,255,255)
        if self.bskey:
            pg.draw.line(templayer, color, (52,31), (15,31),2)
            pg.draw.line(templayer, color, (15,31), (20,26),2)
            pg.draw.line(templayer, color, (15,32), (20,37),2)
        elif self.enter:
            pg.draw.line(templayer, color, (100,21), (100,31),2)
            pg.draw.line(templayer, color, (100,31), (25,31),2)
            pg.draw.line(templayer, color, (25,31), (30,26),2)
            pg.draw.line(templayer, color, (25,32), (30,37),2)
            
        else:
            text = self.font.render(myletter, 1, (255, 255, 255))
            textpos = text.get_rect()
            blockoffx = (self.width / 2)
            blockoffy = (self.height / 2)
            offsetx = blockoffx - (textpos.width / 2)
            offsety = blockoffy - (textpos.height / 2)
            templayer.blit(text,(offsetx, offsety))
        
        screen.blit(templayer, (self.x,self.y))
        self.dirty = False

class VirtualKeyboard(object):
    ''' Implement a basic full screen virtual keyboard for touchscreens '''
    def run(self, screen, font, text='', callback=None):
        # First, make a backup of the screen        
        self.screen = screen

        info = pg.display.Info()
        self.screen_size = (info.current_w, info.current_h)

        self.background = pg.Surface(self.screen_size)
        
        # Copy original screen to self.background
        self.background.blit(screen,(0,0))
        
        # Shade the background surrounding the keys
        self.keylayer = pg.Surface(self.screen_size)
        self.keylayer.fill((0, 0, 0))
        self.keylayer.set_alpha(100)
        self.screen.blit(self.keylayer,(0,0))
        
        self.keys = []

        x = (self.screen_size[0]-self.screen_size[1])/2
        y = (self.screen_size[1] - 100)/2

        self.textbox = pg.Surface((x,y))
        self.text = text
        self.caps = False
        
        pg.font.init() # Just in case 
        # self.font = pg.font.Font(None, 40)
        self.font = font

        self.input = TextInput(self.background,self.screen,self.font, self.text,x,y)
        
        self.addkeys()
          
        self.paintkeys()
        counter = 0
        # My main event loop (hog all processes since we're on top, but someone might want
        # to rewrite this to be more event based.  Personally it works fine for my purposes ;-)
        while 1:
            time.sleep(.05)
            events = pg.event.get() 
            if events != None:
                for e in events:
                    if e.type == pg.QUIT:
                        self.clear()
                        return self.not_null( self.text ) # Return what we started with

                    if (e.type == pg.KEYDOWN):
                        if e.key == pg.K_ESCAPE:
                            self.clear()
                            return self.not_null( self.text ) # Return what we started with
                        if e.key == pg.K_RETURN:
                            self.clear()
                            return self.not_null(self.input.text) # Return what the user entered
                        if e.key == pg.K_LEFT:
                            self.input.deccursor()
                            pg.display.flip()
                        if e.key == pg.K_RIGHT:
                            self.input.inccursor()
                            pg.display.flip()
                    if (e.type == pg.MOUSEBUTTONDOWN):
                        self.selectatmouse()   
                    if (e.type == pg.MOUSEBUTTONUP):
                        if self.clickatmouse():
                            # user clicked enter if returns True
                            self.clear()
                            return self.not_null(self.input.text) # Return what the user entered
                    if (e.type == pg.MOUSEMOTION):
                        if e.buttons[0] == 1:
                            # user click-dragged to a different key?
                            self.selectatmouse()
                        
            counter += 1
            if counter > 10:                
                self.input.flashcursor()
                counter = 0

            # desenhar
            if callback:
                callback(self.screen)

    def not_null(self,text):
        if len(text) == 0:
            return 'Sem Nome'
        return text

    def unselectall(self, force = False):
        ''' Force all the keys to be unselected
            Marks any that change as dirty to redraw '''
        for key in self.keys:
            if key.selected:
                key.selected = False
                key.dirty = True
    
    def clickatmouse(self):
        ''' Check to see if the user is pressing down on a key and draw it selected '''
        self.unselectall()
        for key in self.keys:
            myrect = pg.Rect(key.x,key.y,key.width,key.height)
            if myrect.collidepoint(pg.mouse.get_pos()):
                key.dirty = True
                if key.bskey:
                    # Backspace
                    self.input.backspace()
                    self.paintkeys() 
                    return False
                if key.caption == 'SPACE':                    
                    self.input.addcharatcursor(' ')
                    self.paintkeys() 
                    return False
                if key.caption == 'SHIFT':
                    self.togglecaps()
                    self.paintkeys() 
                    return False
                if key.enter:
                    return True

                mykey = key.caption
                if self.caps:
                    mykey = mykey.upper()
                self.input.addcharatcursor(mykey)
                self.paintkeys()
                return False
            
        self.paintkeys() 
        return False
        
    def togglecaps(self):
        ''' Toggle uppercase / lowercase '''
        if self.caps: 
            self.caps = False
        else:
            self.caps = True
        for key in self.keys:
            key.dirty = True        
        
    def selectatmouse(self):
        ''' User has clicked a key, let's use it '''
        self.unselectall()
        for key in self.keys:
            myrect = pg.Rect(key.x,key.y,key.width,key.height)
            if myrect.collidepoint(pg.mouse.get_pos()):
                key.selected = True
                key.dirty = True
                self.paintkeys()
                return
            
        self.paintkeys()        
            
    def addkeys(self):
        ''' Adds the setup for the keys.  This would be easy to modify for additional keys
        
         The default start position places the keyboard slightly left of center by design
         so many people have issues with the right side of their touchscreens that I did this
         on purpose. '''
        
        # x = 10
        # y = self.screen_size[1]-140
        x0 = (self.screen_size[0]-self.screen_size[1])/2
        x = x0
        y = (self.screen_size[1]+100)/2
        
        row = ['1','2','3','4','5','6','7','8','9','0']
        for item in row:
            onekey = VirtualKey(item,x,y)
            onekey.font = self.font
            self.keys.append(onekey)
            x += 70
            
        onekey = VirtualKey('<-',x,y)
        onekey.font = self.font
        onekey.bskey = True
        self.keys.append(onekey)
        
        y += 70
        x = x0

        row = ['q','w','e','r','t','y','u','i','o','p']
        for item in row:
            onekey = VirtualKey(item,x,y)
            onekey.font = self.font
            self.keys.append(onekey)
            x += 70
        y += 70
        x = x0
        row = ['a','s','d','f','g','h','j','k','l']
        for item in row:
            onekey = VirtualKey(item,x,y)
            onekey.font = self.font
            self.keys.append(onekey)
            x += 70
            
        onekey = VirtualKey('ENTER',x,y,138)
        onekey.font = self.font
        onekey.enter = True
        self.keys.append(onekey)
        
        x = x0
        y += 70
        onekey = VirtualKey('SPACE',x,y,138)
        onekey.font = self.font
        self.keys.append(onekey)
        x += 140
        
        row = ['z','x','c','v','b','n','m']
        for item in row:
            onekey = VirtualKey(item,x,y)
            onekey.font = self.font
            self.keys.append(onekey)
            x += 70
        onekey = VirtualKey('SHIFT',x,y,138)
        onekey.font = self.font
        self.keys.append(onekey)
            
        
    def paintkeys(self):
        ''' Draw the keyboard (but only if they're dirty.) '''
        for key in self.keys:
            key.draw(self.screen, self.background, self.caps)
        
        pg.display.flip()
    
    def clear(self):    
        ''' Put the screen back to before we started '''
        self.screen.blit(self.background,(0,0))
        pg.display.flip()