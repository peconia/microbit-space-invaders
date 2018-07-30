import pygame


class Ufo(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image_number = 0
        self.images = [pygame.image.load('Resources/Images/ufo_A1.png'),
                       pygame.image.load('Resources/Images/ufo_B1.png')]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.screen_width = width
        self.screen_height = height
        self.rect.top = 40
        self.rect.right = 0
        self.movement_counter = 1

    def update(self):
        self.image_number += 1
        self.image = self.images[self.image_number % 2]

    def move_right(self):
        self.rect.right += 3
