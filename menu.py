import pygame, button, text_bar, types
from settings import *



class Menu():
    def __init__(self):
        len_to_board = BOARD_WIDTH * SQUARE_SIZE
        #señal para empezar
        self.start_signal = False

        self.game = ''

        self.player_name = ''

        #start button setup
        self.start_button = button.Button()
        self.start_button.text = 'Comenzar'
        self.start_button.rect.update((len_to_board,0),(SCREEN_WIDTH - len_to_board, 200))
        self.start_button.menu = self
        self.start_button.on_press = types.MethodType(on_start_button_press, self.start_button)
        self.valid_name = False

        #name bar setup
        self.name_bar = text_bar.TextBar()
        self.name_bar.rect.update(len_to_board+10, 205, SCREEN_WIDTH - len_to_board-20, 20)
        self.name_bar.menu = self

        


    def update(self, text_input):
        self.start_button.update()
        self.name_bar.update(text_input)

        if self.name_bar.text == '' or self.name_bar.text == 'Nombre':
            self.valid_name = False
        else:
            self.valid_name = True


    def draw(self, screen):
        self.start_button.draw(screen)
        self.name_bar.draw(screen)


def on_start_button_press(self):
    if self.menu.valid_name:
        self.menu.start_signal = not self.menu.start_signal
        self.text = 'Rendirse' if self.menu.game.paused else 'Comenzar'