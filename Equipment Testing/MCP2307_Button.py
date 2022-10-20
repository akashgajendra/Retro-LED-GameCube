import RPi.GPIO as GPIO
import busio
import time
import digitalio
import board
from adafruit_mcp230xx.mcp23017 import MCP23017
from rpi_lcd import LCD

i2c = busio.I2C(board.SCL,board.SDA)

GPIO.setmode(GPIO.BCM)

mcp = MCP23017(i2c)

pin7 = mcp.get_pin(7)
pin6 = mcp.get_pin(6)
pin5 = mcp.get_pin(5)
pin4 = mcp.get_pin(4)

pin7.direction = digitalio.Direction.INPUT
pin7.pull = digitalio.Pull.UP

pin6.direction = digitalio.Direction.INPUT
pin6.pull = digitalio.Pull.UP

pin5.direction = digitalio.Direction.INPUT
pin5.pull = digitalio.Pull.UP

pin4.direction = digitalio.Direction.INPUT
pin4.pull = digitalio.Pull.UP

i=0
lcd = LCD()
try:
    lcd.text("SCORE: 0",1)
    lcd.text("SNAKE",2)
except:
    pass
finally:
    time.sleep(3)
    lcd.clear()

while True:
    if(pin7.value == False or pin6.value == False or pin5.value == False or  pin4.value == False):
        print("Hit " ,i)
        i+=1
        time.sleep(0.2)