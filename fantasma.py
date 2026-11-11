import pygame, entidad
from settings import *

class Ghost(entidad.Entity):
    def __init__(self):
        super().__init__()
        self.wish_direction = pygame.Vector2(0,0)
        self.target = pygame.Vector2(0,0)
        self.game = []
        self.type = 'chaser'
        self.state = 'scatering'
        self.frame = 0


    def tick(self):
        self.frame += 1
        self.change_state()
        self.move()


    def move(self):
        #de posicion en pixeles a posicion en tablero
        self.board_position = (self.position // 20)
    
        #poder hacer giros de 180º
        if abs((self.direction - self.wish_direction).x) == 2 or abs((self.direction - self.wish_direction).y) == 2:
            self.direction.update(self.wish_direction)

        #si se alinea con las paredes
        if self.wall_aligned():
            self.move_to_target()

            #si tiene hueco, dobla
            if self.game.board[int(self.board_position.x + self.wish_direction.x) % BOARD_WIDTH][int(self.board_position.y + self.wish_direction.y)] == 0:
                self.direction.update(self.wish_direction)

            #se frena si choca con una pared
            elif self.game.board[int(self.board_position.x + self.direction.x) % BOARD_WIDTH][int(self.board_position.y + self.direction.y)] == 1:
                self.direction.update(0,0)

        self.position += self.direction * self.speed
        self.position.x = self.position.x % (BOARD_WIDTH * 20)


    def move_to_target(self):
        self.update_target()

        up_dir    = pygame.Vector2( 0,-1)
        left_dir  = pygame.Vector2(-1, 0)
        down_dir  = pygame.Vector2( 0, 1)
        right_dir = pygame.Vector2( 1, 0)

        dirs = [up_dir, left_dir, down_dir, right_dir]

        #sacamos las distancias en todas las direcciones
        distance_up    = (self.target - self.board_position - up_dir   ).length_squared()
        distance_left  = (self.target - self.board_position - left_dir ).length_squared()
        distance_down  = (self.target - self.board_position - down_dir ).length_squared()
        distance_right = (self.target - self.board_position - right_dir).length_squared()

        #descartamos los caminos con paredes y giros de 180º
        if self.game.board[int(self.board_position.x + up_dir.x)    % BOARD_WIDTH][int(self.board_position.y + up_dir.y)   ] == 1 or self.direction == down_dir:
            distance_up    = 10000
        if self.game.board[int(self.board_position.x + left_dir.x)  % BOARD_WIDTH][int(self.board_position.y + left_dir.y) ] == 1 or self.direction == right_dir:
            distance_left  = 10000
        if self.game.board[int(self.board_position.x + down_dir.x)  % BOARD_WIDTH][int(self.board_position.y + down_dir.y) ] == 1 or self.direction == up_dir:
            distance_down  = 10000
        if self.game.board[int(self.board_position.x + right_dir.x) % BOARD_WIDTH][int(self.board_position.y + right_dir.y)] == 1 or self.direction == left_dir:
            distance_right = 10000

        #descartes por spawn de fantasmas
        if self.board_position.x > 12 and self.board_position.x < 15 and self.board_position.y == 11:
            distance_down = 10000
        #los fantasmas salen del curartito
        if self.board_position.x > 12 and self.board_position.x < 15 and self.board_position.y <= 14 and self.board_position.y > 11:
            distance_up = 0
        #descarte por spawn de pacman
        if self.board_position.x > 11 and self.board_position.x < 16 and self.board_position.y == 23:
            distance_up = 10000

        #decidimos a donde movernos, (prioridad descendente: arriba, izquierda, abajo, derecha)
        distancias = [distance_up, distance_left, distance_down, distance_right]
        indice_dir = distancias.index(min(distancias))

        self.wish_direction.update(dirs[indice_dir])


    def update_target(self):
        if self.state == "chasing":

            if self.type == "chaser":
                self.target = self.game.player.board_position

            if self.type == "fronter":
                self.target = self.game.player.board_position + (4* self.game.player.last_direction)
                if self.game.player.last_direction == pygame.Vector2(0,-1):
                    self.target += pygame.Vector2(-4,0)

            if self.type == "flanker":
                aux_target = self.game.player.board_position + (self.game.player.last_direction)
                if self.game.player.last_direction == pygame.Vector2(0,-1):
                    aux_target += pygame.Vector2(-1,0)
                self.target = -(self.game.blinky.board_position - aux_target)
                self.target += aux_target

            if self.type == "roamer":
                if (self.game.player.board_position - self.board_position).length_squared() >= 64:
                    self.target = self.game.player.board_position  
                else: self.target = pygame.Vector2(0, BOARD_HEIGHT + 1)

        if self.state == 'scatering':

            if self.type == 'chaser':
                self.target = pygame.Vector2(BOARD_WIDTH-3, -4)

            if self.type == 'fronter':
                self.target = pygame.Vector2(-4, 2)

            if self.type == 'flanker':
                self.target = pygame.Vector2(BOARD_WIDTH-1, BOARD_HEIGHT)

            if self.type == 'roamer':
                self.target = pygame.Vector2(0, BOARD_HEIGHT)


    def draw(self, screen):
        super().draw(screen)

        #debug
        '''if self.type == 'chaser':
            pygame.draw.circle(screen, 'red', self.target * 20 + (10,10), 15)

        if self.type == 'fronter':
            pygame.draw.circle(screen, 'pink', self.target * 20 + (10,10), 15)
                               
        if self.type == 'flanker':
            pygame.draw.circle(screen, (0,255,255), self.target * 20 + (10,10), 15)

        if self.type == 'roamer':
            pygame.draw.circle(screen, 'orange', self.target * 20 + (10,10), 15)'''

    def change_state(self):
        if (self.frame + 660) % 900 == 0:
            print("chasing")
            self.state = 'chasing'
            self.wish_direction *= -1
            self.direction *= -1

        if self.frame % 900 == 0:
            print("scatering")
            self.state = 'scatering'
            self.wish_direction *= -1
            self.direction *= -1