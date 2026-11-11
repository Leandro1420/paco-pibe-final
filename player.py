import pygame, entidad
from settings import *

class Player(entidad.Entity):
    def __init__(self):
        super().__init__()
        self.wish_direction = pygame.Vector2(0,0)
        self.last_direction = pygame.Vector2(0,0)
        self.animator_weight = 0
        self.old_direction = pygame.Vector2(0,0)


    def tick(self, input):
        #controla input
        if input[pygame.K_UP]:
            self.wish_direction.update(0,-1)
        if input[pygame.K_DOWN]:
            self.wish_direction.update(0,1)
        if input[pygame.K_LEFT]:
            self.wish_direction.update(-1,0)
        if input[pygame.K_RIGHT]:
            self.wish_direction.update(1,0)


        self.move()

        #actualizar sprite
        if self.direction != pygame.Vector2(0,0):
            self.animator_weight += 2
            self.image_index = int((self.animator_weight /10) % 3)
            print (self.animator_weight)

        rotation_angle = self.old_direction.angle - self.direction.angle
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.rotate(self.images[i], rotation_angle)

        self.old_direction = self.direction.copy()


    def move(self):

        #de posicion en pixeles a posicion en tablero
        self.board_position = (self.position // 20)
    
        #poder hacer giros de 180º
        if abs((self.direction - self.wish_direction).x) == 2 or abs((self.direction - self.wish_direction).y) == 2:
            self.direction.update(self.wish_direction)
            self.last_direction.update(self.direction)

        #si se alinea con las paredes
        if self.wall_aligned():

            #si tiene hueco, dobla
            if self.game.board[int(self.board_position.x + self.wish_direction.x) % BOARD_WIDTH][int(self.board_position.y + self.wish_direction.y)] == 0:
                self.direction.update(self.wish_direction)
                self.last_direction.update(self.direction)

            #se frena si choca con una pared
            elif self.game.board[int(self.board_position.x + self.direction.x) % BOARD_WIDTH][int(self.board_position.y + self.direction.y)] == 1:
                self.direction.update(0,0)

        self.position += self.direction * self.speed
        self.position.x = self.position.x % (BOARD_WIDTH * 20)