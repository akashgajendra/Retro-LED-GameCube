import RPi.GPIO as GPIO
import busio
import time
import board
from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL,board.SDA)

GPIO.setmode(GPIO.BCM)

mcp = MCP23017(i2c)

pin7 = mcp.get_pin(7)

print("LOW_MCP")
pin7.switch_to_output(value=False)
time.sleep(3)
print("HIGH_MCP")
pin7.switch_to_output(value=True)
time.sleep(3)
print("chip end")

time.sleep(5)

# light
#GPIO.setup(18, GPIO.OUT)

print("LOW")
#GPIO.output(18,GPIO.LOW)
time.sleep(3)
#print("HIGH")
#GPIO.output(18,GPIO.HIGH)
#time.sleep(3)
print("Cleanup")

GPIO.cleanup()