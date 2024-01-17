import pygame
from Button import Button
import random

class FifteenPuzzle:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.tiles = [[0] * cols for _ in range(rows)]
        self.empty_row = rows - 1
        self.empty_col = cols - 1

    def shuffle(self):
        numbers = list(range(1, self.rows * self.cols))
        random.shuffle(numbers)
        index = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if index == 15:
                    break
                self.tiles[row][col] = numbers[index]
                index += 1

    def is_solved(self):
        k = 1
        for i in range(self.rows):
            for j in range(self.cols):
                if k == 15:
                    return True
                if self.tiles[i][j] != k:
                    return False
                k += 1

    def move_tile(self, row, col):
        if (
                (abs(row - self.empty_row) == 1 and col == self.empty_col) or
                (abs(col - self.empty_col) == 1 and row == self.empty_row)
        ):
            self.tiles[self.empty_row][self.empty_col], self.tiles[row][col] = self.tiles[row][col], \
                self.tiles[self.empty_row][self.empty_col]
            self.empty_row, self.empty_col = row, col

class PuzzleRenderer:
    def __init__(self, screen, puzzle, cell_size, center_x, center_y):
        self.screen = screen
        self.puzzle = puzzle
        self.cell_size = cell_size
        self.center_x = center_x - 100
        self.center_y = center_y
        self.start_x = center_x - puzzle.cols * cell_size // 2
        self.start_y = center_y - puzzle.rows * cell_size // 2
        self.number_images = {}
        for number in range(1, puzzle.rows * puzzle.cols):
            image = pygame.image.load(f"i{number}.jpg").convert_alpha()
            image = pygame.transform.scale(image, (self.cell_size, self.cell_size))
            self.number_images[number] = image

    def draw(self):
        start_x = self.center_x - self.puzzle.cols * self.cell_size // 2
        start_y = self.center_y - self.puzzle.rows * self.cell_size // 2
        self.ramka_image = pygame.image.load("ramka.png").convert_alpha()
        self.ramka_image = pygame.transform.scale(self.ramka_image, (410, 410))
        for row in range(self.puzzle.rows):
            for col in range(self.puzzle.cols):
                x = start_x + col * self.cell_size
                y = start_y + row * self.cell_size
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size))
                number = self.puzzle.tiles[row][col]
                if number > 0:
                    image = self.number_images[number]
                    image_rect = image.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                    self.screen.blit(image, image_rect)
        self.screen.blit(self.ramka_image, (start_x - 35, start_y - 35))

    def update(self):
        pygame.display.flip()

class Game:
    def __init__(self, screen, width, height, player_name, music_on):
        self.screen = screen
        self.screen.fill((210, 200, 225))
        self.width = width
        self.height = height
        self.font = pygame.font.Font('Ubuntu-Medium.ttf', 36)
        self.music_on = music_on
        self.running = True
        self.return_to_menu = False
        self.player_name = player_name
        if len(self.player_name) == 0:
            self.player_name = 'Player'
        self.background_image = pygame.image.load("three.jpg").convert() # Изображение для фона
        self.background_image = pygame.transform.scale(self.background_image, (width, height))
        self.menu_button_image = pygame.image.load("home.png").convert_alpha() # Изображение для кнопки "В меню"
        self.menu_button_image = pygame.transform.scale(self.menu_button_image, (40, 40))
        self.menu_button = Button(screen, None, 10, 10, 50, 50, self.go_to_menu, image=self.menu_button_image)
        self.puzzle = FifteenPuzzle(4, 4)  # Размер поля 4x4
        self.puzzle.shuffle()  # Перемешиваем пятнашки
        self.renderer = PuzzleRenderer(screen, self.puzzle, 85, width // 2 - 20,
                                       height // 2 - 20)  # Размер ячейки 85x85
        self.click_sound = pygame.mixer.Sound("but_f.mp3")
        self.move_sound = pygame.mixer.Sound("move_f.mp3")
        # Изображение для кнопки "Музыка"
        self.music_button_image_on = pygame.image.load("music_on.png").convert_alpha()
        self.music_button_image_on = pygame.transform.scale(self.music_button_image_on, (40, 40))
        self.music_button_image_off = pygame.image.load("music_off.png").convert_alpha()
        self.music_button_image_off = pygame.transform.scale(self.music_button_image_off, (40, 40))
        if self.music_on:
            self.music_button = Button(screen, None, 740, 550, 790, 600, self.music, image=self.music_button_image_on)
        else:
            self.music_button = Button(screen, None, 740, 550, 790, 600, self.music, image=self.music_button_image_off)

    def music(self):
        if self.music_on:
            pygame.mixer.music.pause()
            self.music_button = Button(self.screen, None, 740, 550, 790, 600, self.music,
                                       image=self.music_button_image_off)
            self.music_on = False
        else:
            pygame.mixer.music.unpause()
            self.music_button = Button(self.screen, None, 740, 550, 790, 600, self.music,
                                       image=self.music_button_image_on)
            self.music_on = True

    def go_to_menu(self):
        self.return_to_menu = True

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.renderer.draw()  # Отрисовываем пятнашки
        self.menu_button.draw()
        self.music_button.draw()
        pygame.display.flip()

    def update(self):
        if self.return_to_menu:
            self.running = False
        self.renderer.update()
        if self.puzzle.is_solved():
            self.running = False
    def run(self):
        while self.running:
            self.update()
            self.draw()