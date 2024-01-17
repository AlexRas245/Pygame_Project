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
            "music_on.png").convert_alpha()  # Изображение когда музыка играет
        self.music_button_image_on = pygame.transform.scale(self.music_button_image_on, (40, 40))
        self.music_button_image_off = pygame.image.load(
            "music_off.png").convert_alpha()  # Изображение когда музыка не играет
        self.music_button_image_off = pygame.transform.scale(self.music_button_image_off, (40, 40))
        # Создаем кнопку "Музыка" с изображением
        self.music_button = Button(screen, None, 740, 550, 790, 600, self.music, image=self.music_button_image_on)
        # Загружаем изображение для кнопки "Начать"
        self.start_button_image = pygame.image.load("start.png").convert_alpha()
        self.start_button_image = pygame.transform.scale(self.start_button_image, (150, 40))
        self.start_button_image_active = pygame.image.load("start_active.png").convert_alpha()
        self.start_button_image_active = pygame.transform.scale(self.start_button_image_active, (150, 40))
        # Загружаем изображение для кнопки "Рейтинг"
        self.rating_button_image = pygame.image.load("ratin.png").convert_alpha()
        self.rating_button_image = pygame.transform.scale(self.rating_button_image, (150, 40))
        self.rating_button_image_active = pygame.image.load("rating_active.png").convert_alpha()
        self.rating_button_image_active = pygame.transform.scale(self.rating_button_image_active, (150, 40))
        # Загружаем изображение для кнопки "Выйти"
        self.exit_button_image = pygame.image.load("exitt.png").convert_alpha()
        self.exit_button_image = pygame.transform.scale(self.exit_button_image, (150, 40))
        self.exit_button_image_active = pygame.image.load("exit_active.png").convert_alpha()
        self.exit_button_image_active = pygame.transform.scale(self.exit_button_image_active, (150, 40))
        # Создаем кнопку "Начать"
        self.start_button = Button(screen, None, 325, 250, 150, 35, self.start_game, image=self.start_button_image)
        # Создаем кнопку "Рейтинг"
        self.rating_button = Button(screen, None, 325, 300, 150, 35, self.show_rating, image=self.rating_button_image)
        # Создаем кнопку "Выйти"
        self.exit_button = Button(screen, None, 325, 350, 150, 35, self.exit_menu, image=self.exit_button_image)

    def update(self):
        self.handle_events()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.music_button.draw()
        self.start_button.draw()
        self.rating_button.draw()
        self.exit_button.draw()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем нажатие на кнопку
                pos = pygame.mouse.get_pos()
                if self.music_button.check_click(pos):# Кнопка Музыка
                    self.music_button.command()
                elif self.start_button.check_click(pos): # Кнопка Начать
                    self.click_sound.play()
                    self.start_button.command()
                elif self.rating_button.check_click(pos):# Кнопка Рейтинг
                    self.click_sound.play()
                    self.rating_button.command()
                elif self.exit_button.check_click(pos):# Кнопка Выйти
                    self.exit_button.command()
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if self.start_button.check_click(pos):
                    self.start_button_active(True)
                else:
                    self.start_button_active(False)
                if self.rating_button.check_click(pos):
                    self.rating_button_active(True)
                else:
                    self.rating_button_active(False)
                if self.exit_button.check_click(pos):
                    self.exit_button_active(True)
                else:
                    self.exit_button_active(False)

    def music(self):
        if self.music_on:
            pygame.mixer.music.pause()
            self.music_button = Button(screen, None, 740, 550, 790, 600, self.music, image=self.music_button_image_off)
            self.music_on = False
        else:
            pygame.mixer.music.unpause()
            self.music_button = Button(screen, None, 740, 550, 790, 600, self.music, image=self.music_button_image_on)
            self.music_on = True

    def start_button_active(self, flag):
        if flag:
            self.start_button = Button(screen, None, 325, 250, 150, 35, self.start_game,
                                       image=self.start_button_image_active)
        else:
            self.start_button = Button(screen, None, 325, 250, 150, 35, self.start_game,
                                       image=self.start_button_image)

    def rating_button_active(self, flag):
        if flag:
            self.rating_button = Button(screen, None, 325, 300, 150, 35, self.show_rating,
                                        image=self.rating_button_image_active)
        else:
            self.rating_button = Button(screen, None, 325, 300, 150, 35, self.show_rating,
                                        image=self.rating_button_image)

    def exit_button_active(self, flag):
        if flag:
            self.exit_button = Button(screen, None, 325, 350, 150, 35, self.exit_menu,
                                      image=self.exit_button_image_active)
        else:
            self.exit_button = Button(screen, None, 325, 350, 150, 35, self.exit_menu, image=self.exit_button_image)

    def start_game(self):
        pass

    def show_rating(self):
        pass

    def exit_menu(self):
        pygame.mixer.quit()
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
