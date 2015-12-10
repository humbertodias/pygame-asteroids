import pygame as pg
import virtual_keyboard

def main():

    pg.init()
    screen = pg.display.set_mode((1024, 762))

    font_path = 'resource/fonts/hyperspace.ttf'
    font = pg.font.Font(font_path, 40)

    vkeyboard = virtual_keyboard.VirtualKeyboard()
    userinput = vkeyboard.run(screen, font, "Seu nome")
    print(userinput)

if __name__ == "__main__":
    main()