import pygame
import sys
from Button import Button


class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font('Ubuntu-Medium.ttf', 28)
        self.music_on = True
        pygame.display.set_caption("Пятнашки")
        self.background_image = pygame.image.load("three_menu.png").convert_alpha()  # изображение для фона
        self.background_image = pygame.transform.scale(self.background_image, (width, height))
        pygame.mixer.init()  # Музыка
        pygame.mixer.set_num_channels(8)
        pygame.mixer.music.load("music_f.mp3")  # Музыка на фоне
        pygame.mixer.music.play(-1)
        self.click_sound = pygame.mixer.Sound("but_f.mp3")  # Музыка для клика на кнопки
        # Загружаем изображение для кнопки "Музыка"
        self.music_button_image_on = pygame.image.load(
            "music_on.png").convert_alpha()  # изображение когда музыка играет
        self.music_button_image_on = pygame.transform.scale(self.music_button_image_on, (40, 40))
        self.music_button_image_off = pygame.image.load(
            "music_off.png").convert_alpha()  # изображение когда музыка не играет
        self.music_button_image_off = pygame.transform.scale(self.music_button_image_off, (40, 40))
        # Создаем кнопку "Музыка" с изображением
        self.music_button = Button(screen, None, 740, 550, 790, 600, self.music, image=self.music_button_image_on)

    def update(self):
        self.handle_events()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.music_button.draw()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем нажатие на кнопку
                pos = pygame.mouse.get_pos()
                if self.music_button.check_click(pos):
                    self.music_button.command()

    def music(self):
        if self.music_on:
            pygame.mixer.music.pause()
            self.music_button = Button(screen, None, 740, 550, 790, 600, self.music, image=self.music_button_image_off)
            self.music_on = False
        else:
            pygame.mixer.music.unpause()
            self.music_button = Button(screen, None, 740, 550, 790, 600, self.music, image=self.music_button_image_on)
            self.music_on = True


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
