import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, width, height):
        super().__init__()
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.ammo = 30
        self.hit = False
        self.image = pygame.image.load('Resources/Images/Player.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = self.screen_height - 10

    def move_left(self):
        self.rect.left = self.rect.left - 10
        if self.rect.left < 5:
            self.rect.left = 5

    def move_right(self):
        self.rect.right = self.rect.right + 10
        if self.rect.right > self.screen_width - 5:
            self.rect.right = self.screen_width -5
    
    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
        return self.ammo

    def is_alive(self):
        return not self.hit
        
