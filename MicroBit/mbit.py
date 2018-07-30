from microbit import *

def send_sensor_data():
    x = accelerometer.get_x()
    a, b = button_a.was_pressed(), button_b.was_pressed()
    print(x, a, b)

def show_hearts():
    hearts = [Image.HEART_SMALL, Image.HEART]
    display.clear()
    display.show(hearts, wait=False, delay=200)

def vibrate_angrily():
    for x in range(14):
        pin1.write_digital(1)
        sleep(70)
        pin1.write_digital(0)
        sleep(50)

def vibrate_happily():
    for x in range(4):
        pin1.write_digital(1)
        sleep(150)
        pin1.write_digital(0)
        sleep(50)
        pin1.write_digital(1)
        sleep(90)
        pin1.write_digital(0)
        sleep(40)

uart.init(115200)

motor_on = False
motor_counter = 0
while True:
    sleep(100)
    send_sensor_data()
    if uart.any():
        data = uart.read(1)
        if data == b'1':
            display.show(Image.ARROW_E, wait=False)
        elif data == b'2':
            # game lost
            vibrate_angrily()
            display.show(Image.ARROW_W, wait=False)
        elif data == b'3':
            # the player was hit
            pin1.write_digital(1)
            display.show(Image.CONFUSED, wait=False)
            motor_on = True
            motor_counter = 0
        elif data == b'4':
            # player scored a point
            show_hearts()
        elif data == b'5':
            # game won
            display.show(Image.HAPPY, wait=False)
            vibrate_happily()
            display.show(Image.ARROW_W, wait=False)
    if motor_on:
        motor_counter += 1
        if motor_counter > 5:
            pin1.write_digital(0)
            display.clear()
            motor_on = False
    else:
        pin1.write_digital(0)
