import pygame

class Player:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.ammo = 30
        self.hit = False
        self.image = pygame.image.load('Resources/Images/Player.png')
        self.rectangle = self.image.get_rect()
        self.rectangle.bottom = self.screen_height - 10

    def move_left(self):
        self.rectangle.left = self.rectangle.left - 10
        if self.rectangle.left < 5:
            self.rectangle.left = 5
        self.screen.blit(self.image, self.rectangle)

    def move_right(self):
        self.rectangle.right = self.rectangle.right + 10
        if self.rectangle.right > self.screen_width - 5:
            self.rectangle.right = self.screen_width -5
        self.screen.blit(self.image, self.rectangle)

    def stay_still(self):
        self.screen.blit(self.image, self.rectangle)
    
    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
        return self.ammo

    def is_alive(self):
        return not self.hit
        
