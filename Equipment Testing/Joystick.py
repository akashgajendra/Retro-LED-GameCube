import RPi.GPIO as GPIO
import busio
import time
import board
from adafruit_mcp230xx.mcp23017 import MCP23017

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN) #left
GPIO.setup(6, GPIO.IN) # right
GPIO.setup(13, GPIO.IN) # up
GPIO.setup(19, GPIO.IN) # down

while True:
    if(GPIO.input(5) == GPIO.LOW):
        print("left")
        #GPIO.cleanup()
        time.sleep(1)
    if(GPIO.input(6) == GPIO.LOW):
        print("right")
        #GPIO.cleanup()
        time.sleep(1)
    if(GPIO.input(13) == GPIO.LOW):
        print("up")
        #GPIO.cleanup()
        time.sleep(1)
    if(GPIO.input(19) == GPIO.LOW):
        print("down")
        #GPIO.cleanup()
        time.sleep(1)



