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

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.handle_events()
        if self.back_to_menu:
            self.running = False
        pygame.display.flip()

    def run(self):
        while self.running:
            self.update()
            self.draw()
