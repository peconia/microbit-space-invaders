import pygame

class Alien(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image_number = 0
        self.images = [pygame.image.load('Resources/Images/alien_1A.png'),
                       pygame.image.load('Resources/Images/alien_1B.png')]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self):
        self.image_number += 1
        self.image = self.images[self.image_number % 2]
