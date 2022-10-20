from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT, CP437_FONT, TINY_FONT
from luma.led_matrix.device import max7219
import time

import RPi.GPIO as GPIO
import busio
import digitalio
import board
from adafruit_mcp230xx.mcp23017 import MCP23017
from rpi_lcd import LCD

# defining button entries

i2c = busio.I2C(board.SCL,board.SDA)

GPIO.setmode(GPIO.BCM)

mcp = MCP23017(i2c)

pin7 = mcp.get_pin(2)
pin6 = mcp.get_pin(6)
pin5 = mcp.get_pin(0)
pin4 = mcp.get_pin(4)
#pin3 = mcp.get_pin(3)


pin7.direction = digitalio.Direction.INPUT
pin7.pull = digitalio.Pull.UP

pin6.direction = digitalio.Direction.INPUT
pin6.pull = digitalio.Pull.UP

pin5.direction = digitalio.Direction.INPUT
pin5.pull = digitalio.Pull.UP

pin4.direction = digitalio.Direction.INPUT
pin4.pull = digitalio.Pull.UP

#pin3.direction = digitalio.Direction.INPUT
#pin3.pull = digitalio.Pull.UP


serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=24, block_orientation=-90)

# (x,y) pairs to determine the boxes
GRID_1 = (2,0)  # 0 -> start of row 1
GRID_2 = (10,0)
GRID_3 = (18,0)
GRID_4 = (26,0)
GRID_5 = (2,8)
GRID_6 = (10,8) # 8 -> start of row 2
GRID_7 = (18,8)
GRID_8 = (26,8)
GRID_9 = (2,16) # 16 -> start of row3
GRID_10 = (10,16)
GRID_11 = (18,16)
GRID_12 = (26,16)

player1 = True
player2 = False

device.clear()
time.sleep(3)
global GridArray
GridArray = [[1,2,2,2],[2,2,2,2],[2,2,2,2]] # 1 = X   0 = O
GridDisplayArray = [[GRID_1,GRID_2,GRID_3,GRID_4],[GRID_5,GRID_6,GRID_7,GRID_8], [GRID_9,GRID_10,GRID_11,GRID_12]]

def findempty(GridArray, GridDisplayArray,player):
    for i in range(len(GridArray)):
        for j in range(len(GridArray[i])):
            if(GridArray[i][j] == 2):
                if(player):
                    GridArray[i][j] = 1
                else:
                    GridArray[i][j] = 0
                return GridDisplayArray[i][j]
    return -1


'''for i in range(len(GridArray)):
    for j in range(len(GridArray[i])):'''

with canvas(device) as draw:
                text(draw, GRID_1, "X", fill="white", font=proportional(LCD_FONT))
x = 0
y = 0
player1 = True
while True:
        # out of bounds check for up - reset it to start of Griddisplayarray
        if(x == -3): 
            x = 0
        # out of bounds check for down - reset it to end of Griddisplayarray
        if(x == 2):
            x = -1
            
         # out of bounds check for up - reset it to start of Griddisplayarray
        if(y == 3): 
            y = -1
        # out of bounds check for down - reset it to end of Griddisplayarray
        if(y == -4):
            y = 0
        if(pin7.value == False):
            with canvas(device) as draw:
                x-=1
                text(draw, GridDisplayArray[x][y], "X", fill="white", font=proportional(TINY_FONT))
            time.sleep(0.2)
        elif(pin6.value == False):
            with canvas(device) as draw:
                x+=1
                text(draw, GridDisplayArray[x][y], "O", fill="white", font=proportional(TINY_FONT))
            time.sleep(0.2)
        elif(pin5.value == False):
            with canvas(device) as draw:
                y+=1
                text(draw, GridDisplayArray[x][y], "R", fill="white", font=proportional(TINY_FONT))
            time.sleep(0.2)
        elif(pin4.value == False):
            with canvas(device) as draw:
                y-=1
                text(draw, GridDisplayArray[x][y], "L", fill="white", font=proportional(TINY_FONT))
            time.sleep(0.2)
        '''elif(pin3.value == False):
            if(player1):
                GridArray[x][y] = 1
                with canvas(device) as draw:
                    for l in range(len(GridArray)):
                            for p in range(len(GridArray[l])):
                                if(GridArray[l][p] == 0):
                                    text(draw, GridDisplayArray[l][p], "O", fill="white", font=proportional(LCD_FONT))
                                elif(GridArray[l][p] == 1):
                                    text(draw, GridDisplayArray[l][p], "X", fill="white", font=proportional(LCD_FONT))
                player1 = False
            else:
                GridArray[x][y] = 0
                with canvas(device) as draw:
                    for l in range(len(GridArray)):
                            for p in range(len(GridArray[l])):
                                if(GridArray[l][p] == 0):
                                    text(draw, GridDisplayArray[l][p], "O", fill="white", font=proportional(LCD_FONT))
                                elif(GridArray[l][p] == 1):
                                    text(draw, GridDisplayArray[l][p], "X", fill="white", font=proportional(LCD_FONT))
                player1 = False
'''
