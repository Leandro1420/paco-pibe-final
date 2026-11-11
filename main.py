import pygame, menu, game
from settings import *

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
text_input = ''

game = game.Game()
menu = menu.Menu()

game.menu = menu
menu.game = game

def draw() -> None:
    screen.fill((50,50,50))
    
    game.draw(screen)
    menu.draw(screen)


def tick() -> None:
    if menu.start_signal:
        menu.start_signal = False
        game.paused = not game.paused
        if game.paused:
            game.reset()
        
    game.tick(pygame.key.get_pressed())
    menu.update(text_input)

game.reset()

running = True
while running:
    text_input = ''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            text_input = event.unicode

    tick()
    draw()

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()