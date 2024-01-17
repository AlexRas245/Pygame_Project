import pygame
import sys
from Button import Button


class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font('Ubuntu-Medium.ttf', 28)
        pygame.display.set_caption("Пятнашки")
        self.background_image = pygame.image.load("three_menu.png").convert_alpha()  # изображение для фона
        self.background_image = pygame.transform.scale(self.background_image, (width, height))

    def update(self):
        self.handle_events()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



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
