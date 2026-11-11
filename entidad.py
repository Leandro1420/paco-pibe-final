import pygame
from settings import *
from abc import ABC, abstractmethod

class Entity(ABC):

    def __init__(self):
        self.image_index = 0
        self.position = pygame.Vector2(0,0)
        self.board_position = pygame.Vector2(0,0)
        self.direction = pygame.Vector2(0,0)
        self._images = [pygame.image.load('assets/blank.png')]
        self.rect = self.images[self.image_index].get_rect()
        self.rect.topleft = (self.rect.x -self.rect.h/2, self.rect.y - self.rect.w/2)
        self.game = []
        self.speed = SPEED


    def tick(self):
        pass


    @property
    def images(self):
        return self._images


    @images.setter
    def images(self, images):
        self._images = images
        self.rect = self._images[self.image_index].get_rect()


    def draw(self, screen: pygame.surface.Surface):
        self.rect.topleft = (self.position.x -self.rect.h/2, self.position.y - self.rect.w/2)
        screen.blit(self.images[self.image_index], self.rect)


    def wall_aligned(self):
        return (self.position.x-10) % 20 == 0 and (self.position.y-10) % 20 == 0