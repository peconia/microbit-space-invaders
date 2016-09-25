import serial, pygame
from time import sleep
from pygame.locals import *
from textprint import *
from player import Player
from colours import *
from alien import Alien
from bullet import Bullet


def open_serial_port():
    PORT = "/dev/ttyACM0"
    BAUD = 115200
    s = serial.Serial(PORT)
    s.baudrate = BAUD
    s.parity   = serial.PARITY_NONE
    s.databits = serial.EIGHTBITS
    s.stopbits = serial.STOPBITS_ONE
    return s
 
pygame.init()
s = open_serial_port()
 
# Set up the game window and starting point
size = width, height = 900, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SPACE INVADERS <3")
clock = pygame.time.Clock()
quit_game = False
player = Player(width, height)
points = 0
ammo = 30
points_printer = TextPrint(screen, 10, 10, 25)
ammo_printer = TextPrint(screen, width - 200, 10, 25)

all_sprites_list = pygame.sprite.Group()
bullet_sprite_list = pygame.sprite.Group()
alien_sprite_list = pygame.sprite.Group()

alien = Alien()

all_sprites_list.add(player)
all_sprites_list.add(alien)
alien_sprite_list.add(alien)
 

# -------- Main Program Loop -----------
while not quit_game:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
 
    all_sprites_list.update()

    # read data from microbit 
    data = s.readline().decode('UTF-8')
    data_list = data.rstrip().split(' ')
    try:
        x, a, b = data_list
        # handle player moving
        x = float(x)
        if x > 50:
            player.move_right()
        elif x < - 50:
            player.move_left()

        # handle button presses
        if a == 'True' and b == 'True':
            quit_game = True
        if a == "True":
            points += 1
        if b == "True":
            bullet = player.shoot(ammo)
            if bullet:
                bullet_sprite_list.add(bullet)
                all_sprites_list.add(bullet)
                ammo -= 1

    except ValueError:
        # it is okay, might not have data coming through
        pass

    # handle all bullets
    for bullet in bullet_sprite_list:
        # check if hit alien
        alien_hit_list = pygame.sprite.spritecollide(bullet, alien_sprite_list, True)

        for alien in alien_hit_list:
            bullet_sprite_list.remove(bullet)
            all_sprites_list.remove(bullet)

        # clean up bullet if it is outside of screen
        if bullet.rect.y < -10:
            bullet_sprite_list.remove(bullet)
            all_sprites_list.remove(bullet)
            
    # clear screen
    screen.fill(BLACK)

    # update points and ammo
    points_printer.print('POINTS    {0:0>3}'.format(str(points)), PINK)
    if ammo > 5:
        ammo_printer.print('AMMUNITION    {0:0>3}'.format(str(ammo)), PINK)
    else:
        ammo_printer.print('AMMUNITION    {0:0>3}'.format(str(ammo)), RED)

    # update the screen
    all_sprites_list.draw(screen)
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)

    
 
# Close the serial port connection and window to quit.
s.close()
pygame.quit()
