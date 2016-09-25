import serial, pygame
from time import sleep
from pygame.locals import *
from textprint import *
from player import Player
from colours import *


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
player = Player(screen, width, height)
points = 0
ammo = 10
points_printer = TextPrint(screen, 10, 10, 25)
ammo_printer = TextPrint(screen, width - 200, 10, 25)

 

# -------- Main Program Loop -----------
while not quit_game:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
 
    # --- Game logic should go here
 
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
    
     
    # --- Drawing code should go here
    data = s.readline().decode('UTF-8')
    data_list = data.rstrip().split(' ')
    try:
        x, a, b = data_list
        # handle moving
        x = float(x)
        if x > 50:
            player.move_right()
        elif x < - 50:
            player.move_left()
        else:
            player.stay_still()

        # button presses
        if a == 'True' and b == 'True':
            quit_game = True
        if a == "True":
            points += 1
        if b == "True":
            ammo = player.shoot()

    except ValueError:
        # it is okay, might not have data coming through
        pass

    # update points and ammo
    points_printer.print('POINTS    {0:0>3}'.format(str(points)), PINK)
    if ammo > 5:
        ammo_printer.print('AMMUNITION    {0:0>3}'.format(str(ammo)), PINK)
    else:
        ammo_printer.print('AMMUNITION    {0:0>3}'.format(str(ammo)), RED)
    # update the screen 
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)

    
 
# Close the serial port connection and window to quit.
s.close()
pygame.quit()
