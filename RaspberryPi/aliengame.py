import serial, pygame
from time import sleep
from pygame.locals import *
from textprint import *
from player import Player
from colours import *
from alien import Alien
from bullet import Bullet
from alien_bullet import AlienBullet

MOVEALIENEVENT = pygame.USEREVENT+1

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
        # make aliens move down every 4 secs
        pygame.time.set_timer(MOVEALIENEVENT, 4000)
        self.game_over = False
        self.game_won = False
        self.player = Player(self.width, self.height)
        self.points = 0
        self.ammo = 60
        self.all_sprites_list = pygame.sprite.Group()
        self.bullet_sprite_list = pygame.sprite.Group()
        self.alien_sprite_list = pygame.sprite.Group()
        self.alien_bullet_sprite_list = pygame.sprite.Group()
        self.s.write(str.encode("1"))

        self.all_sprites_list.add(self.player)

        # add some aliens!
        alien_type = 0
        for y in range(50, 380, 60):
            for x in range (45, 870, 85):
                alien = Alien(x, y, alien_type % 3)
                self.all_sprites_list.add(alien)
                self.alien_sprite_list.add(alien)
            alien_type += 1

    def end_game(self):
        self.game_over = True
        self.all_sprites_list = pygame.sprite.Group()
        self.s.write(str.encode("2"))

    def play(self):
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == MOVEALIENEVENT:
                    for alien in self.alien_sprite_list:
                        alien.move_down()
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
                    bullet.kill()  # removes sprite from all sprite lists
                    self.points += 1
                    self.s.write(str.encode("4"))
                    

                # check if hit alien bullet
                alien_bullet_hit_list = pygame.sprite.spritecollide(bullet, self.alien_bullet_sprite_list, True)

                for alien_bullet in alien_bullet_hit_list:
                    bullet.kill()
                    self.points += 1
                    self.s.write(str.encode("4"))

                # clean up bullet if it is outside of screen
                if bullet.rect.y < -10:
                    bullet.kill()

            # handle alien bullets
            for bullet in self.alien_bullet_sprite_list:
                if bullet.rect.colliderect(self.player.rect):
                    self.s.write(str.encode("3"))
                    self.end_game()
                
                # clean up bullet if it is outside of screen
                if bullet.rect.y > self.height + 10:
                    bullet.kill()

            # check if aliens touch player or get out of screen
            for alien in self.alien_sprite_list:
                if alien.rect.colliderect(self.player.rect) or alien.rect.bottom > self.height:
                    self.s.write(str.encode("3"))
                    self.end_game()
                    
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

            if len(self.alien_sprite_list) == 0:
                self.end_game()
                self.game_won = True

            if self.game_over and not self.game_won:
                self.centre_printer.print('GAME OVER', GREEN)
                self.centre_printer_small.print('Press  A  to  start  a  new  game', GREEN)

            if self.game_won:
                self.centre_printer.print('OMG YOU WON!', BLUE)
                self.centre_printer_small.print('Press  A  to  start  a  new  game', GREEN)
            
            pygame.display.flip()
         
            # Limit to 60 frames per second
            self.clock.tick(60)
            
