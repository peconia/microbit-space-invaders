import pygame

'''
Helper class to write text on screen.
'''
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, text, color):
        bitmap = self.font.render(text, True, color)
        screen.blit(bitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
