from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT, CP437_FONT, TINY_FONT, ATARI_FONT
from luma.led_matrix.device import max7219
import time

import RPi.GPIO as GPIO
import busio
import digitalio
import board
from adafruit_mcp230xx.mcp23017 import MCP23017
from rpi_lcd import LCD
import random

# defining button entries

i2c = busio.I2C(board.SCL,board.SDA)

#buttons
GPIO.setmode(GPIO.BCM)

#COIN
GPIO.setup(23, GPIO.IN)#QUIT


GPIO.setup(16, GPIO.IN)#left
GPIO.setup(25, GPIO.IN)#up
GPIO.setup(17, GPIO.IN)#down
GPIO.setup(12, GPIO.IN)#right
#joystick
GPIO.setup(5, GPIO.IN)#up
GPIO.setup(19, GPIO.IN)#left
GPIO.setup(13, GPIO.IN)#right
GPIO.setup(6, GPIO.IN)#down


#pin3 = mcp.get_pin(3)

'''
pin7.direction = digitalio.Direction.INPUT
pin7.pull = digitalio.Pull.UP
'''


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

#LCD check
lcd = LCD()
lcd.text("Tic Tac Toe",1)
lcd.text("Turn: Player 1",2)

player1 = True
player2 = False

device.clear()
time.sleep(3)
global GridArray
GridArray = [[2,2,2,2],
             [2,2,2,2],
             [2,2,2,2]] # 1 = X   0 = O
GridDisplayArray = [[GRID_1,GRID_2,GRID_3,GRID_4],[GRID_5,GRID_6,GRID_7,GRID_8], [GRID_9,GRID_10,GRID_11,GRID_12]]

def check_locked(GridArray):
    print("Grid: ", GridArray)
    if (GridArray[0][0]!=2 and GridArray[1][0]!=2 and GridArray[0][2]!=2 and GridArray[1][2]!=2 and GridArray[2][1]!=2):
        return True
    if (GridArray[1][0]!=2 and GridArray[1][1]!=2 and GridArray[2][2]!=2 and GridArray[0][3]!=2 and GridArray[1][3]!=2):
        return True
    
    return False


def findempty(GridArray, GridDisplayArray,player):
    # Sequential
    for i in range(len(GridArray)):
        for j in range(len(GridArray[i])):
            if(GridArray[i][j] == 2):
                if(player):
                    GridArray[i][j] = 1
                else:
                    GridArray[i][j] = 0
                return GridDisplayArray[i][j]
    return -1


def finndlast(GridArray, GridDisplayArray,player):
    n = 0
    for i in range(len(GridArray)):
        for j in range(len(GridArray[i])):
            if(GridArray[i][j] == 2):
                n += 1
    if(n == 1):
        return True
    else:
        return False

def findempty_i_j(GridArray, GridDisplayArray,player, x,y):
    # Random
    if check_locked(GridArray):
        while True:
            x=random.randrange(0,3)
            y=random.randrange(0,4)
            if GridArray[x][y]==2:
                return GridDisplayArray[x][y], x, y
            
    for i in range(len(GridArray)):
        for j in range(len(GridArray[i])):
            if(GridArray[i][j] == 2 and i!=x and j!=y):
                return GridDisplayArray[i][j], i , j
    return -1

def adjust_bound(x,y):
    # out of bounds check for up - reset it to start of Griddisplayarray
        if(x <= -3): 
            x = 0
        # out of bounds check for down - reset it to end of Griddisplayarray
        if(x >= 2):
            x = -1
            
         # out of bounds check for up - reset it to start of Griddisplayarray
        if(y >= 3): 
            y = -1
        # out of bounds check for down - reset it to end of Griddisplayarray
        if(y <= -4):
            y = 0
            
        return x,y
def check_Column(GridArray):
    check_x = 0
    check_o = 0
    '''
    for i in range(len(GridArray)):
        for j in range(i,len(GridArray[i])):
            if(GridArray[j-1][i] == 1):
                check_x +=1
            if(GridArray[j-1][i] ==0):
                check_o += 1
    '''
    for i in range(len(GridArray)):
        if(GridArray[i][0] == 1):
                check_x +=1
        if(GridArray[i][0] ==0):
                check_o += 1
    if(check_x == 3):
            print(GridArray)
            print("here 7")
            return "x_won"
    elif(check_o == 3):
            print("here 8")
            return "o_won"
    check_o = 0
    check_x = 0
    
    for i in range(len(GridArray)):
        if(GridArray[i][1] == 1):
                check_x +=1
        if(GridArray[i][1] ==0):
                check_o += 1
    if(check_x == 3):
            print(GridArray)
            print("here 7")
            return "x_won"
    elif(check_o == 3):
            print("here 8")
            return "o_won"
    check_o = 0
    check_x = 0
    
    for i in range(len(GridArray)):
        if(GridArray[i][2] == 1):
                check_x +=1
        if(GridArray[i][2] ==0):
                check_o += 1
    if(check_x == 3):
            print(GridArray)
            print("here 7")
            return "x_won"
    elif(check_o == 3):
            print("here 8")
            return "o_won"
    check_o = 0
    check_x = 0
    
    for i in range(len(GridArray)):
        if(GridArray[i][3] == 1):
                check_x +=1
        if(GridArray[i][3] ==0):
                check_o += 1

        if(check_x == 3):
            print(GridArray)
            print("here 7")
            return "x_won"
        elif(check_o == 3):
            print("here 8")
            return "o_won"
    return "no one"
    
    
        
def check_Row(GridArray):
    check_x = 0
    check_o = 0
    '''
    for i in range(len(GridArray)):
        for j in range(len(GridArray[i])):
            if(GridArray[i][j] == 1):
                check_x +=1
            if(GridArray[i][j] ==0):
                check_o += 1
        if(check_x == 3):
            return "x_won"
        elif(check_o == 3):
            return "o_won"
    return "no one"
    '''
    for i in range(4):
        if(GridArray[0][i] == 1):
                check_o = 0
                check_x +=1
        if(GridArray[0][i] ==0):
                check_x =0
                check_o += 1
    if(check_x == 3):
            print(GridArray)
            print("here 7")
            return "x_won"
    elif(check_o == 3):
            print("here 8")
            return "o_won"
    check_o = 0
    check_x = 0
    
    for i in range(4):
        if(GridArray[1][i] == 1):
                check_o =0
                check_x +=1
        if(GridArray[1][i] ==0):
                check_x =0
                check_o += 1
    if(check_x == 3):
            print(GridArray)
            print("here 7")
            return "x_won"
    elif(check_o == 3):
            print("here 8")
            return "o_won"
    check_o = 0
    check_x = 0
    
    for i in range(4):
        if(GridArray[2][i] == 1):
                check_o =0
                check_x +=1
        if(GridArray[2][i] ==0):
                check_x =0
                check_o += 1

        if(check_x == 3):
            print("here4")
            print(GridArray)
            return "x_won"
        elif(check_o == 3):
            print("here 5")
            return "o_won"
    return "no one"
    

def check_Diagonal(GridArray):
    check = "no one"
    '''
    check_x = 0
    check_o = 0
    for i in range(len(GridArray)):
        # positie diagonals
        if(GridArray[i][i] == 1):
                check_x +=1
        if(GridArray[i][i] ==0):
                check_o += 1
        if(i < len(GridArray)-1):
            if(GridArray[i][i+1] ==1):
                    check_x += 1
            if(GridArray[i][i+1] ==0):
                    check_o += 1
        # negative diagonals
        if(GridArray[i][2-i] == 1):
                check_x +=1
        if(GridArray[i][2-i] ==0):
                check_o += 1
        
        if(GridArray[i][3-i] ==1):
                check_x += 1
        if(GridArray[i][3-i] ==0):
                check_o += 1
                    
        if(check_x == 3):
            return "x_won"
        elif(check_o == 3):
            return "o_won"
        '''
    if(GridArray[0][0] == GridArray[1][1] == GridArray[2][2] == 1):
        check = "x_won"
        print("here 1")
    if(GridArray[0][1] == GridArray[1][2] == GridArray[2][3] == 1):
        check = "x_won"
        print("here 2")
    if(GridArray[0][2] == GridArray[1][1] == GridArray[2][0] == 1):
        check = "x_won"
    if(GridArray[0][3] == GridArray[1][2] == GridArray[2][1] == 1):
        check = "x_won"
    
    if(GridArray[0][0] == GridArray[1][1] == GridArray[2][2] == 0):
        check = "o_won"
    if(GridArray[0][1] == GridArray[1][2] == GridArray[2][3] == 0):
        check = "o_won"
    if(GridArray[0][2] == GridArray[1][1] == GridArray[2][0] == 0):
        check = "o_won"
    if(GridArray[0][3] == GridArray[1][2] == GridArray[2][1] == 0):
        check = "o_won"
        
    return check

def check_win(GridArray):
    check_column = check_Column(GridArray)
    check_row = check_Row(GridArray)
    check_diagonal = check_Diagonal(GridArray)
    if(check_column == "x_won" or check_row == "x_won" or check_diagonal == "x_won"):
        return "x_won"
    elif(check_column == "o_won" or check_row == "o_won" or check_diagonal == "o_won"):
        return "o_won"
    else:
        return "none"
    
with canvas(device) as draw:
                text(draw, GRID_1, "X", fill="white", font=proportional(TINY_FONT))
x = 0
y = 0
player1 = True
play = True
winner = "no one"
while play:
        if(finndlast(GridArray, GridDisplayArray,player1) == True):
             with canvas(device) as draw:
                for l in range(len(GridArray)):
                            for p in range(len(GridArray[l])):
                                if(GridArray[l][p] == 0):
                                    text(draw, GridDisplayArray[l][p], "O", fill="white", font=proportional(LCD_FONT))
                                elif(GridArray[l][p] == 1):
                                    text(draw, GridDisplayArray[l][p], "X", fill="white", font=proportional(LCD_FONT))
                                    
                new_pos,x,y = findempty_i_j(GridArray, GridDisplayArray,player1,x,y)
                if(player1):
                    text(draw, new_pos, "X", fill="white", font=proportional(LCD_FONT))
                else:
                    text(draw, new_pos, "O", fill="white", font=proportional(LCD_FONT))
                    #continue
                play = False
                winner = check_win(GridArray)
                break
        
        x,y = adjust_bound(x,y)
        if(GPIO.input(25) == GPIO.LOW or GPIO.input(5) == GPIO.LOW):
            with canvas(device) as draw:
                for l in range(len(GridArray)):
                            for p in range(len(GridArray[l])):
                                if(GridArray[l][p] == 0):
                                    text(draw, GridDisplayArray[l][p], "O", fill="white", font=proportional(LCD_FONT))
                                elif(GridArray[l][p] == 1):
                                    text(draw, GridDisplayArray[l][p], "X", fill="white", font=proportional(LCD_FONT))
                                    
                x-=1
                if(player1 and GridArray[x][y] == 2):
                    text(draw, GridDisplayArray[x][y], "X", fill="white", font=proportional(TINY_FONT))
                elif(not player1 and GridArray[x][y] == 2):
                    text(draw, GridDisplayArray[x][y], "O", fill="white", font=proportional(TINY_FONT))
                else:
                    #x-=1
                    #x,y = adjust_bound(x,y)
                    
                    # CODE TO SKIP COL IN THE ROW IF FILLED AND END UP ON THE NEXT
                    next_row1=x-1
                    
                    x1,y=adjust_bound(next_row1,y)
                    if GridArray[x1][y]==2:
                        print("JUMP BLOCK: ", x1,x,y)
                        x=x-1
                        print("Modified X - Up: ", x)
                        x,y=adjust_bound(x,y)
                        new_pos=GridDisplayArray[x][y]
                    else:
                        new_pos,x,y = findempty_i_j(GridArray, GridDisplayArray,player1,x,y)
                    
                    
                    if(player1):
                        text(draw, new_pos, "X", fill="white", font=proportional(TINY_FONT))
                    else:
                        text(draw, new_pos, "O", fill="white", font=proportional(TINY_FONT))
                    #continue
                
            time.sleep(0.2)
        elif(GPIO.input(17) == GPIO.LOW or GPIO.input(6) == GPIO.LOW):
            with canvas(device) as draw:
                for l in range(len(GridArray)):
                            for p in range(len(GridArray[l])):
                                if(GridArray[l][p] == 0):
                                    text(draw, GridDisplayArray[l][p], "O", fill="white", font=proportional(LCD_FONT))
                                elif(GridArray[l][p] == 1):
                                    text(draw, GridDisplayArray[l][p], "X", fill="white", font=proportional(LCD_FONT))
                
                x+=1
                if(player1 and GridArray[x][y] == 2):
                    text(draw, GridDisplayArray[x][y], "X", fill="white", font=proportional(TINY_FONT))
                elif(not player1 and GridArray[x][y] == 2):
                    text(draw, GridDisplayArray[x][y], "O", fill="white", font=proportional(TINY_FONT))
                else:
                    #x=+1
                    #x,y = adjust_bound(x,y)
                    
                    # CODE TO SKIP COL IN THE ROW IF FILLED AND END UP ON THE NEXT
                    next_row1=x+1
                    x1,y=adjust_bound(next_row1,y)

                    if GridArray[x1][y]==2:
                        print("JUMP BLOCK: ", x1,x,y)
                        x=x+1
                        print("Modified X - Down: ", x)
                        x,y=adjust_bound(x,y)
                        new_pos=GridDisplayArray[x][y]
                    else:
                        new_pos,x,y = findempty_i_j(GridArray, GridDisplayArray,player1,x,y)
                    
                    
                    if(player1):
                        text(draw, new_pos, "X", fill="white", font=proportional(TINY_FONT))
                    else:
                        text(draw, new_pos, "O", fill="white", font=proportional(TINY_FONT))
                    #continue
                
            time.sleep(0.2)
        elif(GPIO.input(13) == GPIO.LOW or GPIO.input(12) == GPIO.LOW):
            with canvas(device) as draw:
                for l in range(len(GridArray)):
                            for p in range(len(GridArray[l])):
                                if(GridArray[l][p] == 0):
                                    text(draw, GridDisplayArray[l][p], "O", fill="white", font=proportional(LCD_FONT))
                                elif(GridArray[l][p] == 1):
                                    text(draw, GridDisplayArray[l][p], "X", fill="white", font=proportional(LCD_FONT))
                
                y+=1
                if(player1 and GridArray[x][y] == 2):
                    text(draw, GridDisplayArray[x][y], "X", fill="white", font=proportional(TINY_FONT))
                elif(not player1 and GridArray[x][y] == 2):
                    text(draw, GridDisplayArray[x][y], "O", fill="white", font=proportional(TINY_FONT))
                else:
                    #y+=1
                    #x,y = adjust_bound(x,y)
                    
                    
                    # CODE TO SKIP COL IN THE ROW IF FILLED AND END UP ON THE NEXT
                    next_col1=y+1
                    next_col2=y+2
                    
                    x,y1=adjust_bound(x,next_col1)
                    x,y2=adjust_bound(x,next_col2)

                    if GridArray[x][y1]==2:
                        print("JUMP BLOCK: ", x,y,y1)
                        y=y+1
                        print("Modified Y - Right: ", y)
                        x,y=adjust_bound(x,y)
                        new_pos=GridDisplayArray[x][y]
                    elif GridArray[x][y2]==2:
                        print("JUMP BLOCK: ", x,y,y2)
                        y=y+2
                        print("Modified Y - Right2: ", y)
                        x,y=adjust_bound(x,y)
                        new_pos=GridDisplayArray[x][y]
                    else:
                        new_pos,x,y = findempty_i_j(GridArray, GridDisplayArray,player1,x,y)
                    if(player1):
                        text(draw, new_pos, "X", fill="white", font=proportional(TINY_FONT))
                    else:
                        text(draw, new_pos, "O", fill="white", font=proportional(TINY_FONT))
                    #continue

                
            time.sleep(0.2)
        elif(GPIO.input(16) == GPIO.LOW or GPIO.input(19) == GPIO.LOW):
            with canvas(device) as draw:
                for l in range(len(GridArray)):
                            for p in range(len(GridArray[l])):
                                if(GridArray[l][p] == 0):
                                    text(draw, GridDisplayArray[l][p], "O", fill="white", font=proportional(LCD_FONT))
                                elif(GridArray[l][p] == 1):
                                    text(draw, GridDisplayArray[l][p], "X", fill="white", font=proportional(LCD_FONT))
                
                y-=1
                if(player1 and GridArray[x][y] == 2):
                    text(draw, GridDisplayArray[x][y], "X", fill="white", font=proportional(TINY_FONT))
                elif(not player1 and GridArray[x][y] == 2):
                    text(draw, GridDisplayArray[x][y], "O", fill="white", font=proportional(TINY_FONT))
                else:
                    #y-=1
                    #x,y = adjust_bound(x,y)
                    
                    # CODE TO SKIP COL IN THE ROW IF FILLED AND END UP ON THE NEXT
                    next_col1=y-1
                    next_col2=y-2
                    
                    x,y1=adjust_bound(x,next_col1)
                    x,y2=adjust_bound(x,next_col2)

                    if GridArray[x][y1]==2:
                        print("JUMP BLOCK: ", x,y,y1)
                        y=y-1
                        print("Modified Y - Left: ", y)
                        x,y=adjust_bound(x,y)
                        new_pos=GridDisplayArray[x][y]
                    elif GridArray[x][y2]==2:
                        print("JUMP BLOCK: ", x,y,y2)
                        y=y-2
                        print("Modified Y - Left2: ", y)
                        x,y=adjust_bound(x,y)
                        new_pos=GridDisplayArray[x][y]
                    else:
                        new_pos,x,y = findempty_i_j(GridArray, GridDisplayArray,player1,x,y)
                    if(player1):
                        text(draw, new_pos, "X", fill="white", font=proportional(TINY_FONT))
                    else:
                        text(draw, new_pos, "O", fill="white", font=proportional(TINY_FONT))
                    #continue
                
            time.sleep(0.2)
            
        # fixing position onto array grid
        if(GPIO.input(23) == GPIO.LOW):
            if(player1 and  GridArray[x][y] == 2):
                    lcd.text("Turn: Player 2",2)
                    GridArray[x][y] = 1
                    player1 = False
            elif(not player1 and  GridArray[x][y] == 2):
                    lcd.text("Turn: Player 1",2)
                    GridArray[x][y] = 0
                    player1 = True
            winner = check_win(GridArray)
            if(winner == "x_won"):
                play = False
            elif(winner == "o_won"):
                play = False
                
            # Move pawn automatically after position selected
            with canvas(device) as draw:
                for l in range(len(GridArray)):
                            for p in range(len(GridArray[l])):
                                if(GridArray[l][p] == 0):
                                    text(draw, GridDisplayArray[l][p], "O", fill="white", font=proportional(LCD_FONT))
                                elif(GridArray[l][p] == 1):
                                    text(draw, GridDisplayArray[l][p], "X", fill="white", font=proportional(LCD_FONT))
                
                x+=1
                if(player1 and GridArray[x][y] == 2):
                    text(draw, GridDisplayArray[x][y], "X", fill="white", font=proportional(TINY_FONT))
                elif(not player1 and GridArray[x][y] == 2):
                    text(draw, GridDisplayArray[x][y], "O", fill="white", font=proportional(TINY_FONT))
                else:
                    #x=+1
                    #x,y = adjust_bound(x,y)
                    new_pos,x,y = findempty_i_j(GridArray, GridDisplayArray,player1,x,y)
                    if(player1):
                        text(draw, new_pos, "X", fill="white", font=proportional(TINY_FONT))
                    else:
                        text(draw, new_pos, "O", fill="white", font=proportional(TINY_FONT))
                    #continue
            
                time.sleep(0.2)
                
                
                
if(winner == "x_won"):
        with canvas(device) as draw:
                text(draw, (2, 1), "GAME", fill="white", font=proportional(LCD_FONT))
                text(draw, (2, 8), "OVER", fill="white", font=proportional(LCD_FONT))
                text(draw, (2, 16), "P1 Won", fill="white", font=proportional(ATARI_FONT))
                lcd.text("Tic Tac Toe",1)
                lcd.text("Player 1 Won",2)
        time.sleep(2)
elif(winner == "o_won"):
        with canvas(device) as draw:
                text(draw, (2, 1), "GAME", fill="white", font=proportional(LCD_FONT))
                text(draw, (2, 8), "OVER", fill="white", font=proportional(LCD_FONT))
                text(draw, (2, 16), "P2 Won", fill="white", font=proportional(ATARI_FONT))
                lcd.text("Tic Tac Toe",1)
                lcd.text("Player 2 Won:",2)
        time.sleep(2)
else:
    with canvas(device) as draw:
                text(draw, (2, 1), "GAME", fill="white", font=proportional(LCD_FONT))
                text(draw, (2, 8), "OVER", fill="white", font=proportional(LCD_FONT))
                text(draw, (2, 16), "No Winner", fill="white", font=proportional(ATARI_FONT))
                lcd.text("Tic Tac Toe",1)
                lcd.text("No Winner",2)
    time.sleep(2)
lcd.clear()
device.clear()
GPIO.cleanup()