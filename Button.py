import pygame


class Button:
    def __init__(self, screen, text, x, y, width, height, command, image=None):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.command = command
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = pygame.Color('lightskyblue3')
        self.active = False

    def draw(self):
        if self.image:
            self.screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
            self.draw_text(self.text, (0, 0, 0), self.x + self.width // 2, self.y + self.height // 2)

    def draw_text(self, text, color, x, y):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def check_click(self, pos):
        return self.rect.collidepoint(pos)

    def highlight(self):
        self.color = pygame.Color('yellow')

    def unhighlight(self):
        self.color = pygame.Color('lightskyblue3')
