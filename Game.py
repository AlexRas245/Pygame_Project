import pygame
from Button import Button
import random
import time
from рейтинг import RatingMenu
from random import randint

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
        self.background_image = pygame.image.load("three.jpg").convert()  # Изображение для фона
        self.background_image = pygame.transform.scale(self.background_image, (width, height))
        self.menu_button_image = pygame.image.load("home.png").convert_alpha()  # Изображение для кнопки "В меню"
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
        self.start_time = time.time()
        self.moves = 0
        self.db = RatingMenu(self.screen, self.width, self.height, self.music_on)

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

    def record_victory(self):
        # Записываем информацию о победе в базу данных
        self.db.record_victory(self.player_name, self.moves, round(time.time() - self.start_time, 2))

    def handle_mouse_click(self, pos):
        # Пересчитываем координаты в индексы пятнашки
        row = (pos[1] - self.renderer.start_y) // self.renderer.cell_size
        col = (pos[0] - self.renderer.start_x + 100) // self.renderer.cell_size
        # Проверяем, можно ли переместить пятнашку
        if 0 <= row < self.puzzle.rows and 0 <= col < self.puzzle.cols:
            if self.is_valid_move(row, col):
                # Перемещаем пятнашку
                self.move_sound.play()
                self.puzzle.move_tile(row, col)
                self.moves += 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Обработка левого клика мыши
                # Получаем координаты мыши
                pos = pygame.mouse.get_pos()
                self.handle_mouse_click(pos)
                # Проверка, было ли нажатие на кнопку "В меню"
                if self.menu_button.rect.collidepoint(pos):
                    self.click_sound.play()
                    self.return_to_menu = True
                if self.music_button.rect.collidepoint(pos):
                    self.music()

    def is_valid_move(self, row, col):
        # Проверка, можно ли переместить пятнашку в указанную позицию
        return (
                (abs(row - self.puzzle.empty_row) == 1 and col == self.puzzle.empty_col) or
                (abs(col - self.puzzle.empty_col) == 1 and row == self.puzzle.empty_row)
        )

    def display_victory_message(self):
        self.record_victory()
        victory_font = pygame.font.Font('Ubuntu-Medium.ttf', 60)
        victory_text = victory_font.render(f"Вы победили!", True, (0, 0, 0))
        text_rect = victory_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(victory_text, text_rect)
        # Добавляем информацию о времени и ходах
        elapsed_time = round(time.time() - self.start_time, 2)
        info_text = f"Время: {elapsed_time} сек., Ходы: {self.moves}"
        info_font = pygame.font.Font('Ubuntu-Medium.ttf', 36)
        info_render = info_font.render(info_text, True, (0, 0, 0))
        info_rect = info_render.get_rect(center=(self.width // 2, self.height // 2 + 60))
        self.screen.blit(info_render, info_rect)
        pygame.display.flip()
        # Анимация салюта
        fireworks_particles = self.generate_fireworks_particles()
        fireworks_start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - fireworks_start_time < 3000:  # Ожидание 3 секунды
            self.update_fireworks_particles(fireworks_particles)
            self.draw_fireworks_particles(fireworks_particles)
            pygame.display.flip()
            pygame.time.delay(45)

    def run_fireworks_animation(self):
        fireworks_particles = self.generate_fireworks_particles()
        for _ in range(100):  # Количество частиц салюта
            self.update_fireworks_particles(fireworks_particles)
            self.draw_fireworks_particles(fireworks_particles)
            pygame.display.flip()
            pygame.time.delay(45)  # Задержка между кадрами анимации
    def generate_fireworks_particles(self):
        particles = []
        for _ in range(200):  # Количество частиц салюта
            particle = {
                'x': randint(0, self.width),
                'y': randint(0, self.height),
                'color': (randint(0, 255), randint(0, 255), randint(0, 255)),
                'speed_x': randint(-5, 5),
                'speed_y': randint(-5, 5)
            }
            particles.append(particle)
        return particles
    def update_fireworks_particles(self, particles):
        for particle in particles:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['speed_y'] += 0.1
            particle['color'] = tuple(max(0, min(255, c + randint(-10, 10))) for c in particle['color'])

    def draw_fireworks_particles(self, particles):
        for particle in particles:
            pygame.draw.circle(self.screen, particle['color'], (int(particle['x']), int(particle['y'])), 2)
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.renderer.draw()  # Отрисовываем пятнашки
        self.menu_button.draw()
        self.music_button.draw()
        # Преобразование секунд в формат MM:SS
        elapsed_time = time.strftime("%M:%S", time.gmtime(round(time.time() - self.start_time)))
        # Отображение информации о времени, ходах и игроке
        info_text = f"Игрок: {self.player_name}\nХоды: {self.moves}\nВремя: {elapsed_time}"
        info_font = pygame.font.Font('Ubuntu-Medium.ttf', 32)
        left_padding = 500
        max_lines = 5  # Максимальное количество строк для отображения
        info_rect = pygame.Rect(0, 0, 0, 0)
        for i, line in enumerate(info_text.splitlines()):
            if i < max_lines:
                if len(line) > 17:
                    line = line[:15] + '...'
                line_render = info_font.render(line, True, (255, 255, 255))
                line_rect = line_render.get_rect(topleft=(left_padding, 50 + i * 40))
                self.screen.blit(line_render, line_rect)
                info_rect.width = max(info_rect.width, line_rect.width)
                info_rect.height += line_rect.height
        pygame.display.flip()

    def update(self):
        self.handle_events()
        if self.return_to_menu:
            self.running = False
        self.renderer.update()
        if self.puzzle.is_solved():
            self.running = False
            self.display_victory_message()

    def run(self):
        while self.running:
            self.update()
            self.draw()
