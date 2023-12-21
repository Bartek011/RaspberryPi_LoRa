

import RPi.GPIO as GPIO
from gpiozero import Button
from time import sleep
import subprocess

button = Button(26)
print("Start the program")


def command():
    print("Pressed")
    subprocess.run(['sudo', 'bash', 'setup_tx.sh'])

try:
    button.when_pressed = command
finally:
    pass
