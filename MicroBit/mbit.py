from microbit import *

def send_sensor_data():
    x = accelerometer.get_x()
    a, b = button_a.was_pressed(), button_b.was_pressed()
    print(x, a, b)
    
def show_hearts():
    hearts = [Image.HEART_SMALL, Image.HEART]
    display.clear()
    display.show(hearts, wait=False, delay=200)

uart.init(115200)

while True:
    sleep(100)
    send_sensor_data()
    if uart.any():
        data = uart.read(1)
        if data == b'1':
            display.show(Image.ARROW_E, wait=False)
        elif data == b'2':
            display.show(Image.ARROW_W, wait=False)
        elif data == b'3':
            # ammo hit the player
            #TODO: add haptic feedback???
            pass
        elif data == b'4':
            show_hearts()
