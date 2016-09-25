import serial, pygame
from time import sleep
from pygame.locals import *
from textprint import *
from player import Player
from colours import *
from alien import Alien
from bullet import Bullet
from alien_bullet import AlienBullet

class AlienGame:
    def __init__(self, serialport, screen, width, height):
        self.s = serialport
        self.screen = screen
        self.width = width
        self.height = height
        self.points_printer = TextPrint(screen, 10, 10, 25)
        self.ammo_printer = TextPrint(screen, width - 200, 10, 25)
        self.centre_printer = TextPrint(screen, 255, height/2 - 50, 100)
        self.centre_printer_small = TextPrint(screen, 65, height/2 + 50, 60)
        self.clock = pygame.time.Clock()
        self.start_new_game()
        self.play()

    def start_new_game(self):
        self.game_over = False
        self.player = Player(self.width, self.height)
        self.points = 0
        self.ammo = 100
        self.all_sprites_list = pygame.sprite.Group()
        self.bullet_sprite_list = pygame.sprite.Group()
        self.alien_sprite_list = pygame.sprite.Group()
        self.alien_bullet_sprite_list = pygame.sprite.Group()

        self.all_sprites_list.add(self.player)

        # add some aliens!
        for y in range(50, 380, 60):
            for x in range (60, 860, 100):
                alien = Alien(x, y)
                self.all_sprites_list.add(alien)
                self.alien_sprite_list.add(alien)

    def end_game(self):
        self.game_over = True
        self.all_sprites_list = pygame.sprite.Group()

    def play(self):
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.all_sprites_list.update()

            # read data from microbit 
            data = self.s.readline().decode('UTF-8')
            data_list = data.rstrip().split(' ')
            try:
                x, a, b = data_list
                # handle player moving
                x = float(x)
                if x > 50:
                    self.player.move_right()
                elif x < - 50:
                    self.player.move_left()

                # handle button presses
                if a == 'True' and b == 'True':
                    self.end_game()
                if a == "True":
                    if self.game_over:
                        self.start_new_game()
                if b == "True":
                    if not self.game_over:
                        bullet = self.player.shoot(self.ammo)
                        if bullet:
                            self.bullet_sprite_list.add(bullet)
                            self.all_sprites_list.add(bullet)
                            self.ammo -= 1

            except (ValueError, UnicodeDecodeError):
                # it is okay, might not have data coming through
                pass

            for alien in self.alien_sprite_list:
                if not self.game_over:
                    bullet = alien.shoot()
                    if bullet:
                        self.alien_bullet_sprite_list.add(bullet)
                        self.all_sprites_list.add(bullet)

            # handle all bullets
            for bullet in self.bullet_sprite_list:
                # check if hit alien
                alien_hit_list = pygame.sprite.spritecollide(bullet, self.alien_sprite_list, True)

                for alien in alien_hit_list:
                    self.bullet_sprite_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)
                    self.points += 1

                alien_bullet_hit_list = pygame.sprite.spritecollide(bullet, self.alien_bullet_sprite_list, True)

                for alien_bullet in alien_bullet_hit_list:
                    self.alien_bullet_sprite_list.remove(alien_bullet)
                    self.all_sprites_list.remove(alien_bullet)
                    self.points += 1

                # clean up bullet if it is outside of screen
                if bullet.rect.y < -10:
                    self.bullet_sprite_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)

            # handle alien bullets
            for bullet in self.alien_bullet_sprite_list:
                if bullet.rect.colliderect(self.player.rect):
                    self.end_game()
                
                # clean up bullet if it is outside of screen
                if bullet.rect.y > self.height + 10:
                    self.bullet_sprite_list.remove(bullet)
                    self.all_sprites_list.remove(bullet)
                    
            # clear screen
            self.screen.fill(BLACK)

            # update points and ammo
            self.points_printer.print('POINTS    {0:0>3}'.format(str(self.points)), PINK)
            if self.ammo > 5:
                self.ammo_printer.print('AMMUNITION    {0:0>3}'.format(str(self.ammo)), PINK)
            else:
                self.ammo_printer.print('AMMUNITION    {0:0>3}'.format(str(self.ammo)), RED)

            # update the screen
            self.all_sprites_list.draw(self.screen)

            if self.game_over:
                self.centre_printer.print('GAME OVER', GREEN)
                self.centre_printer_small.print('Press  A  to  start  a  new  game', GREEN)
            pygame.display.flip()
         
            # Limit to 60 frames per second
            self.clock.tick(60)
            
