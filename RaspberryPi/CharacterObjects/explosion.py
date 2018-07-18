import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.images = self.get_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def get_images(self):
        images = []
        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load('Resources/Images/explosion/{}'.format(filename)).convert()
            img.set_colorkey(pygame.Color("Black"))
            image = pygame.transform.scale(img, (50, 50))
            images.append(image)
        return images

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
