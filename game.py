import pygame, player, fantasma, data_saver, button
from settings import *

#carga las imagenes del tablero una sola vez
board_images = [pygame.image.load('assets/board/B_I.png'),
                pygame.image.load('assets/board/BL_C.png'), 
                pygame.image.load('assets/board/BL_L.png'),
                pygame.image.load('assets/board/BR_C.png'), 
                pygame.image.load('assets/board/BR_L.png'), 
                pygame.image.load('assets/board/L_I.png'), 
                pygame.image.load('assets/board/R_I.png'), 
                pygame.image.load('assets/board/T_I.png'), 
                pygame.image.load('assets/board/TL_C.png'), 
                pygame.image.load('assets/board/TL_L.png'), 
                pygame.image.load('assets/board/TR_C.png'), 
                pygame.image.load('assets/board/TR_L.png'), 
                pygame.image.load('assets/board/FULL.png')]

#se encarga de asignarle una imagen a cada pared
imaged_board = []

for i in range(len(board)):
    row = []
    for j in range(len(board[i])):
        block = -1
        neighbours =   [board[(i-1)%len(board)][(j-1)%len(board[i])], board[(i-1)%len(board)][(j  )%len(board[i])], board[(i-1)%len(board)][(j+1)%len(board[i])],
                        board[(i  )%len(board)][(j-1)%len(board[i])], board[(i  )%len(board)][(j  )%len(board[i])], board[(i  )%len(board)][(j+1)%len(board[i])],
                        board[(i+1)%len(board)][(j-1)%len(board[i])], board[(i+1)%len(board)][(j  )%len(board[i])], board[(i+1)%len(board)][(j+1)%len(board[i])]]
        
        if neighbours == [0,1,1,0,1,1,0,1,1] or neighbours == [1,1,1,0,1,1,0,1,1] or neighbours == [0,1,1,0,1,1,1,1,1]:
            block = 0
        if neighbours == [0,1,1,0,1,1,0,0,0]:
            block = 1
        if neighbours == [1,1,1,1,1,1,0,1,1]:
            block = 2
        if neighbours == [0,0,0,0,1,1,0,1,1]:
            block = 3
        if neighbours == [0,1,1,1,1,1,1,1,1]:
            block = 4
        if neighbours == [1,1,1,1,1,1,0,0,0] or neighbours == [1,1,1,1,1,1,1,0,0] or neighbours == [1,1,1,1,1,1,0,0,1] or neighbours == [1,1,1,1,1,1,1,0,1]:
            block = 5
        if neighbours == [0,0,0,1,1,1,1,1,1] or neighbours == [1,0,0,1,1,1,1,1,1] or neighbours == [0,0,1,1,1,1,1,1,1] or neighbours == [1,0,1,1,1,1,1,1,1]:
            block = 6
        if neighbours == [1,1,0,1,1,0,1,1,0] or neighbours == [1,1,1,1,1,0,1,1,0] or neighbours == [1,1,0,1,1,0,1,1,1]:
            block = 7
        if neighbours == [1,1,0,1,1,0,0,0,0]:
            block = 8
        if neighbours == [1,1,1,1,1,1,1,1,0]:
            block = 9
        if neighbours == [0,0,0,1,1,0,1,1,0]:
            block = 10
        if neighbours == [1,1,0,1,1,1,1,1,1]:
            block = 11
        if neighbours == [1,1,1,1,1,1,1,1,1]:
            block = 12

        row.append(block)
    imaged_board.append(row)
#algunas correcciones
imaged_board[12][13] = 8
imaged_board[15][13] = 10


class Game():
    def __init__(self):
        self.paused = True
        self.board = board
        self.square_size = SQUARE_SIZE
        self.player_points = 0
        self.add_balls()
        self.lifes = 3
        self.have_data = False
        self.menu = ''
        self.timer = 0
        self.points = button.Button()
        self.points.hovering_color = self.points.default_color
        self.points.pressed_color = self.points.default_color
        self.points.rect = pygame.rect.Rect(BOARD_WIDTH * SQUARE_SIZE + 10, 250, SCREEN_WIDTH - BOARD_WIDTH * SQUARE_SIZE - 20, 40)
        self.points.text = 'puntos: 0'
        self.points.border_width = 0

        #player setup
        self.player = player.Player()
        self.player.position.update(290,470)
        self.player.game = self
        self.player.images = [pygame.image.load('assets/pacman/pac-man_0.png'),
                              pygame.image.load('assets/pacman/pac-man_1.png'),
                              pygame.image.load('assets/pacman/pac-man_2.png')]

        #blinky setup (el rojo)
        self.blinky = fantasma.Ghost()
        self.blinky.game = self
        self.blinky.images = [pygame.image.load('assets/fantasmitas/blinky_l.png')]
        self.blinky.type = 'chaser'

        #pinky setup (el rosa)
        self.pinky = fantasma.Ghost()
        self.pinky.game = self
        self.pinky.images = [pygame.image.load('assets/fantasmitas/pinky_l.png')]
        self.pinky.type = 'fronter'

        #inky setup (el celeste)
        self.inky = fantasma.Ghost()
        self.inky.game = self
        self.inky.images = [pygame.image.load('assets/fantasmitas/inky_l.png')]
        self.inky.type = 'flanker'

        #clide setup (el naranja)
        self.clide = fantasma.Ghost()
        self.clide.game = self
        self.clide.images = [pygame.image.load('assets/fantasmitas/clide_l.png')]
        self.clide.type = 'roamer'


    def tick(self, input):
        self.have_data = True
        if not self.paused:
            #actualiza las entidades
            self.player.tick(input)
            self.blinky.tick()
            self.inky.tick()
            self.pinky.tick()
            self.clide.tick()


            #pierde vida si choca con un fantasma
            if (self.player.position - self.blinky.position).length() < 5 or (self.player.position - self.inky.position).length() < 5 or (self.player.position - self.pinky.position).length() < 5 or (self.player.position - self.clide.position).length() < 5:
                self.lose_life()

            #sube el timer
            self.timer += 1

            #subir puntaje y remueve pelotas
            if self.player.wall_aligned():
                if self.player.board_position in self.point_balls:
                    self.point_balls.remove(self.player.board_position)
                    self.player_points += 1000

            if self.point_balls == []:
                self.reset()

            points = self.player_points + (4000 * self.lifes)
            points -= int(self.timer // FPS)

            self.points.text = 'puntos: ' + str(points)


    def draw(self, surface: pygame.surface.Surface):
        #draw board
        for i in range(len(imaged_board)):
            for j in range(len(imaged_board[i])):
                if imaged_board[i][j] != -1:
                    surface.blit(board_images[imaged_board[i][j]],(i*20,j*20))

        #draw balls
        for ball in self.point_balls:
            pygame.draw.circle(surface, 'white', (ball[0]*20+10, ball[1]*20+10), 4)

        #draw player
        self.player.draw(surface)
        self.blinky.draw(surface)
        self.inky.draw(surface)
        self.pinky.draw(surface)
        self.clide.draw(surface)

        #draw points
        self.points.draw(surface)


    def lose_life(self):
        self.lifes -= 1

        #GAME OVER
        if self.lifes == 0:
            self.reset()
            return

        #resetea posiciones
        self.player.position.update(290,470)
        self.player.direction.update(0,0)
        self.player.wish_direction.update(0,0)
        self.player.animator_weight = 0

        self.blinky.position.update(250,290)
        self.pinky.position.update(270,290)
        self.inky.position.update(290,290)
        self.clide.position.update(310,290)


    def reset(self):
        #resetea todos los estados del juego
        self.paused = True

        self.lifes = 3

        self.timer = 0

        self.player.position.update(290,470)
        self.player.direction.update(0,0)
        self.player.wish_direction.update(0,0)
        self.player.animator_weight = 0

        if self.have_data:
            points = self.player_points + (7000 * self.lifes)
            points -= int(self.timer // FPS)
            self.save_data(points)

        self.add_balls()
        self.player_points = 0

        self.blinky.position.update(250,290)
        self.pinky.position.update(270,290)
        self.inky.position.update(290,290)
        self.clide.position.update(310,290)


    def add_balls(self):
        self.point_balls = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:

                    #no-balls space
                    free_space0 = pygame.rect.Rect(7,9,14,11)
                    free_space1 = pygame.rect.Rect(0,11,6,7)
                    free_space2 = pygame.rect.Rect(22,11,6,7)

                    if not free_space0.collidepoint((i,j)) and not free_space1.collidepoint((i,j)) and not free_space2.collidepoint((i,j)):
                        self.point_balls.append([i,j])


    def save_data(self, score):

        data = {'score': score, 'name': self.menu.name_bar.text}
        print("mondongo")
        data_saver.save_score(data)