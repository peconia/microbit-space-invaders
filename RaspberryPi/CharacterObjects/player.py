import pygame
from CharacterObjects.bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.screen_width = width
        self.screen_height = height
        self.image = pygame.image.load('Resources/Images/Player.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = self.screen_height - 10

    def move_left(self):
        self.rect.left -= 10
        if self.rect.left < 5:
            self.rect.left = 5

    def move_right(self):
        self.rect.right += 10
        if self.rect.right > self.screen_width - 5:
            self.rect.right = self.screen_width - 5
    
    def shoot(self, ammo):
        if ammo > 0:
            bullet = Bullet(self.rect.midtop)
            return bullet
        return None
