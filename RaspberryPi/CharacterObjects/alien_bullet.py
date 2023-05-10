import pygame


class AlienBullet(pygame.sprite.Sprite):

    def __init__(self, position, game_level):
        super().__init__()
        self.speed = 6 + game_level

        self.image = pygame.Surface([4, 10])
        self.image.fill(pygame.Color("Red"))
        self.rect = self.image.get_rect(midtop=position)

    def update(self):
        self.rect.y += self.speed
