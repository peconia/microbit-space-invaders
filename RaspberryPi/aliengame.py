import pygame
from pygame.locals import *
from CharacterObjects.explosion import Explosion
from CharacterObjects.ufo import Ufo
from Resources.textprint import TextPrint
from CharacterObjects.alien import Alien
from CharacterObjects.player import Player
from Resources.colours import BLUE, PINK

MOVEALIENEVENT = pygame.USEREVENT+1
MOVEUFOEVENT = pygame.USEREVENT+2


class AlienGame:
    def __init__(self, serialport, screen, width, height):
        self.s = serialport
        self.screen = screen
        self.width = width
        self.height = height
        self.points_printer = TextPrint(screen, 10, 10, 25)
        self.ammo_printer = TextPrint(screen, width - 200, 10, 25)
        self.lives_printer = TextPrint(screen, width - 500, 10, 25)
        self.centre_printer = TextPrint(screen, 255, height/2 - 50, 100)
        self.centre_printer_small = TextPrint(screen, 65, height/2 + 50, 60)
        self.move_down_timer = 4000
        self.game_ending_message_sent = False
        self.clock = pygame.time.Clock()
        self.start_new_game()
        self.play()

    def start_new_game(self):
        # make aliens move down every 4 secs
        pygame.time.set_timer(MOVEALIENEVENT, self.move_down_timer)
        pygame.time.set_timer(MOVEUFOEVENT, 50)
        self.game_over = False
        self.game_won = False
        self.player = Player(self.width, self.height)
        self.points = 0
        self.ammo = 100
        self.all_sprites_list = pygame.sprite.Group()
        self.ufo_sprites_list = pygame.sprite.Group()
        self.player_bullet_sprite_list = pygame.sprite.Group()
        self.alien_sprite_list = pygame.sprite.Group()
        self.alien_bullet_sprite_list = pygame.sprite.Group()
        self.game_ending_message_sent = False
        self.alien_move_down_counter = 0
        self.s.write(str.encode("1"))

        self.all_sprites_list.add(self.player)

        # add some aliens!
        alien_type = 0
        for y in range(50, 380, 60):
            for x in range(45, 870, 85):
                alien = Alien(x, y, alien_type % 3)
                self.all_sprites_list.add(alien)
                self.alien_sprite_list.add(alien)
            alien_type += 1

    def end_game(self):
        self.game_over = True
        self.all_sprites_list = pygame.sprite.Group()

    def play(self):
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == MOVEALIENEVENT:
                    self.alien_move_down_counter += 1
                    for alien in self.alien_sprite_list:
                        alien.move_down()
                    if self.alien_move_down_counter % 7 == 0 and len(self.ufo_sprites_list) < 1:
                        # create an ufo for extra points
                        ufo = Ufo(self.width, self.height)
                        self.ufo_sprites_list.add(ufo)
                        self.all_sprites_list.add(ufo)
                elif event.type == MOVEUFOEVENT:
                    for ufo in self.ufo_sprites_list:
                        ufo.move_right()
            self.all_sprites_list.update()

            # read data from microbit
            self.handle_microbit_data()
            # all the aliens have a chance to shoot
            self.aliens_shoot()

            # handle all the collisions between sprites
            self.handle_player_bullets()
            self.handle_alien_bullets()

            # check if aliens touch player or get out of screen
            self.check_alien_positions()

            self.update_screen()

            self.check_if_game_over()
            
            pygame.display.flip()
         
            # Limit to 60 frames per second
            self.clock.tick(60)

    def handle_microbit_data(self):
        """
        Read any data sent by the microbit controller and take actions based on it
        """
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
                        self.player_bullet_sprite_list.add(bullet)
                        self.all_sprites_list.add(bullet)
                        self.ammo -= 1
        except (ValueError, UnicodeDecodeError):
            # it is okay, might not have data coming through
            pass

    def aliens_shoot(self):
        """
        Handle the aliens shooting at the player
        """
        for alien in self.alien_sprite_list:
            if not self.game_over:
                bullet = alien.shoot()
                if bullet:
                    self.alien_bullet_sprite_list.add(bullet)
                    self.all_sprites_list.add(bullet)

    def handle_player_bullets(self):
        """
        Handle the player bullet collisions and moving off screen
        """
        for bullet in self.player_bullet_sprite_list:
            # check if hit alien
            alien_hit_list = pygame.sprite.spritecollide(bullet, self.alien_sprite_list, dokill=True)

            for alien in alien_hit_list:
                bullet.kill()  # removes sprite from all sprite lists
                explosion = Explosion(alien.rect.center)
                self.all_sprites_list.add(explosion)
                self.points += 1
                self.s.write(str.encode("4"))


            # check if hit alien bullet
            alien_bullet_hit_list = pygame.sprite.spritecollide(bullet, self.alien_bullet_sprite_list, True)

            for alien_bullet in alien_bullet_hit_list:
                bullet.kill()
                self.points += 1
                self.s.write(str.encode("4"))

            ufo_hit_list = pygame.sprite.spritecollide(bullet, self.ufo_sprites_list, True)

            for ufo in ufo_hit_list:
                bullet.kill()
                explosion = Explosion(ufo.rect.center)
                self.all_sprites_list.add(explosion)
                self.points += 500
                self.s.write(str.encode("4"))

            # clean up bullet if it is outside of screen
            if bullet.rect.y < -10:
                bullet.kill()

    def handle_alien_bullets(self):
        """
        Handle the alien bullet collisions and moving off screen
        """
        for bullet in self.alien_bullet_sprite_list:
            if bullet.rect.colliderect(self.player.rect):
                # ammo hit the player
                bullet.kill()  # remove the bullet so the same one won't collide with player again
                self.player.lives -= 1
                if self.player.lives < 1:
                    self.end_game()
                else:
                    # tell the microbit to vibrate
                    self.s.write(str.encode("3"))

            # clean up bullet if it is outside of screen
            if bullet.rect.y > self.height + 10:
                bullet.kill()

    def check_alien_positions(self):
        """
        Handle the aliens moving off screen or colliding with the player
        """
        for alien in self.alien_sprite_list:
            if alien.rect.colliderect(self.player.rect):
                # alien hit player
                self.s.write(str.encode("3"))
                self.player.lives -= 1
                if self.player.lives < 1:
                    self.end_game()
                else:
                    alien.kill()  # remove so won't collide with player again

            if alien.rect.bottom > self.height:
                # alien went off screen, end game
                self.s.write(str.encode("3"))
                self.end_game()

        for ufo in self.ufo_sprites_list:
            if ufo.rect.left > self.width:
                ufo.kill()

    def update_screen(self):
        """
        Helper to update the text and sprites on screen
        """
        # clear screen
        self.screen.fill(pygame.Color("Black"))
        # update points, lives  and ammo
        self.points_printer.print('POINTS    {0:0>3}'.format(str(self.points)), PINK)
        if self.ammo > 5:
            self.ammo_printer.print('AMMUNITION    {0:0>3}'.format(str(self.ammo)), PINK)
        else:
            self.ammo_printer.print('AMMUNITION    {0:0>3}'.format(str(self.ammo)), pygame.Color("Red"))
        self.lives_printer.print('Lives     {0:0>3}'.format(self.player.lives), PINK)
        # update the screen
        self.all_sprites_list.draw(self.screen)

    def check_if_game_over(self):
        if len(self.alien_sprite_list) == 0:
            # all aliens have been killed!
            self.end_game()
            self.game_won = True
        if self.game_over and not self.game_won:
            if not self.game_ending_message_sent:
                self.s.write(str.encode("2"))
                self.game_ending_message_sent = True
            self.centre_printer.print('GAME OVER', pygame.Color("Green"))
            self.centre_printer_small.print('Press  A  to  start  a  new  game', pygame.Color("Green"))
        if self.game_won:
            if not self.game_ending_message_sent:
                self.s.write(str.encode("5"))
                self.game_ending_message_sent = True
            self.centre_printer.print('OMG YOU WON!', BLUE)
            self.centre_printer_small.print('Press  A  to  start  a  new  game', pygame.Color("Red"))