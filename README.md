# Space Invaders with BBC Micro:Bit controller

Work in progress.

This project is a space invader game that you can run on a Raspberry Pi (or on some other linux system), and use
a BBC Micro:bit as a game controller. The Micro:bit should be attached to the Pi via USB.

### Micro:Bit

You can use Mu editor to flash the python code in Microbit. Change into the MicroBit directory and create/activate a
virtualenv with python 3.6. Install all the requirements with
    pip install -r requirements.txt

You can then run Mu editor with command "mu-editor". If you have any issues with the mu editor, please check
their website and github for help.

Copy and paste the mbit.py file contents into Mu and then flash the code on to the microbit.

### Running the game

I suggest installing and running this in a virtualenv. Change into the RaspberryPi directory and create virtualenv with
python 3.6. Activate the venv and then install all the requirements with
    pip install -r requirements.txt

For the serial communication to work, you need to have rights to read and write to the serial /dev/ttyACM0 (if the
microbit is using a different port, you should amend the code).
On Ubuntu 16.06, you can achieve this by adding yourself to the dialout group
    sudo usermod -a -G dialout $USER

Note that you must logout and back in for the serial to work.

Make sure the microbit is connected via USB and has been flashed with the code in mbit.py.

Start the game by running "python3 main_game.py"

Stop the game with Ctrl+C



