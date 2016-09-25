import pygame
from colours import *

class AlienBullet(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect(midtop=position)

    def update(self):
        self.rect.y += 6
