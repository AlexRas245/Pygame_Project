import pygame
import sqlite3
from Button import Button


class RatingMenu:
    def __init__(self, screen, width, height, music_on):
        self.screen = screen
        self.screen.fill((210, 200, 225))
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.back_to_menu = False
        self.music_on = music_on
        self.background_image = pygame.image.load("three_rating.png").convert_alpha()  # Изображение для фона
        self.background_image = pygame.transform.scale(self.background_image, (width, height))
        menu_button_image = pygame.image.load("home.png").convert_alpha()
        menu_button_image = pygame.transform.scale(menu_button_image,
                                                   (40, 40))  # Изображение для кнопки В меню
        self.menu_button = Button(screen, None, 10, 10, 50, 50, self.go_to_menu, image=menu_button_image)
        self.click_sound = pygame.mixer.Sound("but_f.mp3")
        # Загружаем изображение для кнопки "Музыка"
        self.music_button_image_on = pygame.image.load("music_on.png").convert_alpha()
        self.music_button_image_on = pygame.transform.scale(self.music_button_image_on, (40, 40))
        self.music_button_image_off = pygame.image.load("music_off.png").convert_alpha()
        self.music_button_image_off = pygame.transform.scale(self.music_button_image_off, (40, 40))
        # Музыка
        if self.music_on:
            self.music_button = Button(screen, None, 740, 550, 790, 600, self.music, image=self.music_button_image_on)
        else:
            self.music_button = Button(screen, None, 740, 550, 790, 600, self.music, image=self.music_button_image_off)
        self.conn = sqlite3.connect('rating.db')
        self.cursor = self.conn.cursor()
        # Создание таблицы игроков, если она не существует
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT UNIQUE,
                games_played INTEGER DEFAULT 0
            )
        ''')
        # Создание таблицы игр, если она не существует
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                moves INTEGER,
                time REAL,
                FOREIGN KEY(player_id) REFERENCES players(id)
            )
        ''')
        self.update_rating()
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

    def update_rating(self):
        # Получение рейтинга игроков из базы данных
        self.cursor.execute('''
               SELECT players.nickname, COUNT(games.id) as games_played
               FROM players
               LEFT JOIN games ON players.id = games.player_id
               GROUP BY players.id
               ORDER BY games_played DESC
           ''')
        self.rating_data = self.cursor.fetchall()
    def get_player_id(self, player_name):
        # Получаем id игрока по его имени
        self.cursor.execute('''
            SELECT id FROM players WHERE nickname = ?
        ''', (player_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    def get_top_games_played(self, num_players=5):
        # Получить топ игроков по количеству сыгранных игр
        self.cursor.execute('''
            SELECT players.nickname, COUNT(games.id) as games_played
            FROM players
            LEFT JOIN games ON players.id = games.player_id
            GROUP BY players.id
            ORDER BY games_played DESC
        ''')
        top_players = self.cursor.fetchmany(num_players)
        return top_players
    def get_top_speed_run(self, num_players=5):
        # Получить топ игроков по скорости прохождения
        self.cursor.execute('''
            SELECT players.nickname, AVG(games.time) as avg_time
            FROM players
            JOIN games ON players.id = games.player_id
            GROUP BY players.id
            ORDER BY avg_time ASC
        ''')
        top_players = self.cursor.fetchmany(num_players)
        return top_players
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.menu_button.draw()  # Отрисовка кнопки "В меню"
        self.music_button.draw()
        header_text = "Топ по количеству игр"  # Отрисовка заголовка таблицы
        self.draw_text(header_text, (255, 0, 0), self.width // 2, 50)
        self.draw_text("#", (230, 225, 215), self.width // 4 - 80, 100)
        self.draw_text("Никнейм", (230, 225, 215), self.width // 2, 100)
        self.draw_text("Количество игр", (230, 225, 215), self.width * 3 // 4 + 80, 100)
        self.draw_text("Топ по времени", (255, 0, 0), self.width // 2, 320)
        self.draw_text("#", (230, 225, 215), self.width // 4 - 80, 370)
        self.draw_text("Никнейм", (230, 225, 215), self.width // 2, 370)
        self.draw_text("Лучшее время", (230, 225, 215), self.width * 3 // 4 + 80, 370)
        top_games_played = self.get_top_games_played() # Получение топов
        top_speed_run = self.get_top_speed_run()
        # Отрисовка топа по количеству игр
        row_height = 30
        start_y = 140
        for i, (nickname, games_played) in enumerate(top_games_played):
            self.draw_text(str(i + 1), (0, 0, 0), self.width // 4 - 80, start_y + i * row_height)
            self.draw_text(nickname, (0, 0, 0), self.width // 2, start_y + i * row_height)
            self.draw_text(str(games_played), (0, 0, 0), self.width * 3 // 4 + 80, start_y + i * row_height)
        start_y = 410
        for i, (nickname, games_played) in enumerate(top_speed_run):
            self.draw_text(str(i + 1), (0, 0, 0), self.width // 4 - 80, start_y + i * row_height)
            self.draw_text(nickname, (0, 0, 0), self.width // 2, start_y + i * row_height)
            self.draw_text(str(round(games_played, 2)), (0, 0, 0), self.width * 3 // 4 + 80, start_y + i * row_height)
        pygame.display.flip()
    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Обработка левого клика мыши
                pos = pygame.mouse.get_pos()
                if self.menu_button.rect.collidepoint(pos):
                    self.click_sound.play()
                    self.menu_button.command()
                elif self.music_button.rect.collidepoint(pos):
                    self.music_button.command()

    def update(self):
        self.handle_events()
        if self.back_to_menu:
            self.running = False
        pygame.display.flip()
    def go_to_menu(self):
        self.back_to_menu = True
    def run(self):
        while self.running:
            self.update()
            self.draw()
