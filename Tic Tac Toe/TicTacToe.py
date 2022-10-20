from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT
from luma.led_matrix.device import max7219
import time



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
GridArray = [[2,2,2,2],[2,2,2,2],[2,2,2,2]] # 1 = X   0 = O
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
for i in range(len(GridArray)):
    for j in range(len(GridArray[i])):
        #if(GridArray[i][j] == 1):
            #a = input("enter y:")
            if(player1):
                pair_X = findempty(GridArray,GridDisplayArray,player1)
                if(pair_X == -1):
                    print("nothing found")
                    break
                with canvas(device) as draw:
                    text(draw, pair_X, "X", fill="white", font=proportional(LCD_FONT))
                    for l in range(len(GridArray)):
                        for p in range(len(GridArray[i])):
                            if(GridArray[l][p] == 1):
                                text(draw, GridDisplayArray[l][p] , "X", fill="white", font=proportional(LCD_FONT))
                            elif(GridArray[l][p] == 0):
                                text(draw, GridDisplayArray[l][p], "O", fill="white", font=proportional(LCD_FONT))
                    print(GridArray)
                time.sleep(0.5)
                player1 = False
            else:
                pair_O = findempty(GridArray,GridDisplayArray,player1)
                if(pair_O == -1):
                    print("nothing found")
                    break
                with canvas(device) as draw:
                    text(draw, pair_O, "O", fill="white", font=proportional(LCD_FONT))
                    for l in range(len(GridArray)):
                        for p in range(len(GridArray[i])):
                            if(GridArray[l][p] == 0):
                                text(draw, GridDisplayArray[l][p], "O", fill="white", font=proportional(LCD_FONT))
                            elif(GridArray[l][p] == 1):
                                text(draw, GridDisplayArray[l][p], "X", fill="white", font=proportional(LCD_FONT))

                    print(GridArray)
                time.sleep(0.5)
                player1 = True

                
#time.sleep(5)
