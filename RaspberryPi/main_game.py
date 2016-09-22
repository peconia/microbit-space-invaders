import serial, pygame
from time import sleep
from pygame.locals import *
from textprint import *


def open_serial_port():
    PORT = "/dev/ttyACM0"
    BAUD = 115200
    s = serial.Serial(PORT)
    s.baudrate = BAUD
    s.parity   = serial.PARITY_NONE
    s.databits = serial.EIGHTBITS
    s.stopbits = serial.STOPBITS_ONE
    return s

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()
s = open_serial_port()
 
# Set up the game window and starting point
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SPACE INVADERS <3")
clock = pygame.time.Clock()
current_position = 0
quit_game = False
 

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

    printer = TextPrint()
    printer.print(screen, "Hello", GREEN)
    
     
    # --- Drawing code should go here
    data = s.readline().decode('UTF-8')
    data_list = data.rstrip().split(' ')
    try:
        x, a, b = data_list
        # handle moving
        x = float(x)
        if x > current_position + 20:
            printer.print(screen, "RIGHT", RED)
        elif x< current_position - 20:
            printer.print(screen, "LEFT", WHITE)
        else:
            printer.print(screen, "STILL", GREEN)
        current_position = x

        # button presses
        if a == 'True' and b == 'True':
            quit_game = True
        if a == "True":
            printer.print(screen, "A pressed", WHITE)

        if b == "True":
            printer.print(screen, "B pressed", WHITE)

    except ValueError:
        # it is okay, might not have data coming through
        pass
 
    # update the screen 
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)

    
 
# Close the serial port connection and window to quit.
s.close()
pygame.quit()
