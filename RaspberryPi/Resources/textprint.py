import pygame


class TextPrint:
    """
    Helper class to write text on screen.
    """
    def __init__(self, screen, x, y, text_size):
        self.x = x
        self.y = y
        self.font = pygame.font.Font('Resources/Fonts/ARCADECLASSIC.TTF', text_size)
        self.screen = screen

    def print(self, text, color):
        bitmap = self.font.render(text, True, color)
        self.screen.blit(bitmap, [self.x, self.y])

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15



