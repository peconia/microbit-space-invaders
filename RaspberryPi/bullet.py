import pygame
from colours import *

class Bullet(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 6
