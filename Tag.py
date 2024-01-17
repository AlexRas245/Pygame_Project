import pygame
from Меню import MainMenu
import sys
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    menu = MainMenu(screen, 800, 600)
    clock = pygame.time.Clock()
    running = True
    while running:
        menu.update()
        menu.draw()
        clock.tick(60)
    pygame.quit()
    sys.exit()
