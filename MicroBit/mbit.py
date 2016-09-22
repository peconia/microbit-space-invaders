from microbit import *

def get_sensor_data():
    x = accelerometer.get_x()
    a, b = button_a.was_pressed(), button_b.was_pressed()
    print(x, a, b)

while True:
    sleep(100)
    get_sensor_data()
