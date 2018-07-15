import random

import pygame
from CharacterObjects.alien_bullet import AlienBullet


class Alien(pygame.sprite.Sprite):

    def __init__(self, x, y, alien_type=1):
        super().__init__()
        self.image_number = 0
        self.get_images_for_type(alien_type)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.movement_counter = 1

    def update(self):
        self.image_number += 1
        self.image = self.images[self.image_number % 2]

    def shoot(self):
        if not random.randrange(700):
            bullet = AlienBullet(self.rect.midbottom)
            return bullet
        return None

    def get_images_for_type(self, alien_type):
        if alien_type == 1:
            self.images = [pygame.image.load('Resources/Images/alien_2A.png'),
                   pygame.image.load('Resources/Images/alien_2B.png')]
        elif alien_type == 2:
            self.images = [pygame.image.load('Resources/Images/alien_3A.png'),
                   pygame.image.load('Resources/Images/alien_3B.png')]
        else:
            self.images = [pygame.image.load('Resources/Images/alien_1A.png'),
                   pygame.image.load('Resources/Images/alien_1B.png')]

    def move_down(self):
        self.rect.top += 10
        if self.movement_counter % 2 == 0:
            self.rect.left += 30
        else:
            self.rect.left -= 30
        self.movement_counter += 1
