import pygame
from Resources.colours import BLUE


class Bullet(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(midbottom=position)

    def update(self):
        self.rect.y -= 6
