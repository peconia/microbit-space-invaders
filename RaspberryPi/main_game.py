import serial, pygame
from pygame.locals import *
from aliengame import AlienGame

def open_serial_port():
    PORT = "/dev/ttyACM0"
    BAUD = 115200
    s = serial.Serial(PORT)
    s.baudrate = BAUD
    s.parity   = serial.PARITY_NONE
    s.databits = serial.EIGHTBITS
    s.stopbits = serial.STOPBITS_ONE
    return s

def main():
    pygame.init()
    s = open_serial_port()
    quit_game = False
    # Set up the game window and starting point
    size = width, height = 900, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("SPACE INVADERS <3")

    # start game loop
    game = AlienGame(s, screen, width, height)
     
    # Close the serial port connection and window to quit.
    s.close()
    pygame.quit()


if __name__ == '__main__':
    main()
