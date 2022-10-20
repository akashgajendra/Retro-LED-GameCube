from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT,TINY_FONT,ATARI_FONT
from luma.led_matrix.device import max7219
import random
import time
import RPi.GPIO as GPIO
import busio
import time
import digitalio
import board
from rpi_lcd import LCD


#banner
lcd = LCD()
lcd.text("SNAKE",1)
#buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)#left
GPIO.setup(25, GPIO.IN)#up
GPIO.setup(17, GPIO.IN)#down
GPIO.setup(12, GPIO.IN)#right
#joystick
GPIO.setup(5, GPIO.IN)#up
GPIO.setup(19, GPIO.IN)#left
GPIO.setup(13, GPIO.IN)#right
GPIO.setup(6, GPIO.IN)#down

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=24, block_orientation=-90)
device.clear()
time.sleep(1)


snake_length=3

snake="..."
x1=0
y1=1
x2=x1+snake_length
y2=1
y3=y2
x3=x2  

init=[[8,5],[8,6],[8,7]]
'''
with canvas(device) as draw:
            for x in init:
                #for y in range(device.width):
                        draw.point((x[0],x[1]),fill="white")
time.sleep(0.5)
'''

loss=False

def bound_check(init):
    if init[-1][0]<1 or init[-1][0]>31 or init[-1][1]<1 or init[-1][1]>23:
        print("YOU LOST LOSERSS!")
        return True
    for snake in init[0:len(init)-1]:
        if init[-1][0]==snake[0] and init[-1][1]==snake[1]:
            return True
    return False

def down(init):
    init.append([init[len(init)-1][0],init[len(init)-1][1]+1])
    #print(init)
    init=init[1:]
    #print(init)
    return (init)

def up(init):
    init.append([init[len(init)-1][0],init[len(init)-1][1]-1])
    #print(init)
    init=init[1:]
    #print(init)
    return (init)


def left(init):
    init.append([init[len(init)-1][0]-1,init[len(init)-1][1]])
    #print(init)
    init=init[1:]
    #print(init)
    return (init)


def right(init):
    init.append([init[len(init)-1][0]+1,init[len(init)-1][1]])
    #print(init)
    init=init[1:]
    #print(init)
    return (init)

def display_points(init):
    for x in init:
            draw.point((x[0],x[1]),fill="white")
            
moves=['D']
button_click=False


# INCREASE LENGTH OF SNAKE
def resize(init, moves):
    print("RESIZING STARTS")
    if moves[-1]=="R":
        init.insert(0,[init[0][0]-1,init[0][1]])
    if moves[-1]=="L":
        init.insert(0,[init[0][0]+1,init[0][1]])
    if moves[-1]=="U":
        init.insert(0,[init[0][0],init[0][1]+1])
    if moves[-1]=="D":
        init.insert(0,[init[0][0],init[0][1]-1])
    print(init)
    return init
    

# Food Array
food=[]
food_x=random.randrange(2,28)
food_y=random.randrange(2,20)
food+=[[food_x,food_y]]
found_food=False


def did_snake_eat(init, food_x, food_y):
    #print("MAYBE OFF",init)
    if ((init[-1][0]==food_x and init[-1][1]==food_y) or (init[0][0]==food_x and init[0][1]==food_y)):
        print("SNAKE ATE")
        print(init)
        print(food_x,food_y)
        return True
    return False

speed=0.3
while not loss:
    loss=bound_check(init)
    with canvas(device) as draw:
                #print(init)
        #FOOD PART
        found_food=did_snake_eat(init,food_x,food_y)
        if found_food:
            init=resize(init, moves)
            print("GET FOOD")
            food_x=random.randrange(2,28)
            food_y=random.randrange(2,20)
            found_food=False
            speed -= 0.03
            lcd.text("SCORE: "+str(len(init)-3), 2)
        draw.point((food_x,food_y),fill="white")
        
        if moves==[]:
            display_points(init)
                
        elif moves[-1]=="L":
            if not button_click:
                init=left(init)
            display_points(init)
            time.sleep(max(speed,0.04))
            button_click=False

        elif moves[-1]=="R":
            if not button_click:
                init=right(init)
            #init=right(init)
            display_points(init)
            time.sleep(max(speed,0.04))
            button_click=False
            
        elif moves[-1]=="U":
            if not button_click:
                init=up(init)
            display_points(init)
            time.sleep(max(speed,0.04))
            button_click=False
            
        elif moves[-1]=="D":
            if not button_click:
                init=down(init)
            display_points(init)
            time.sleep(max(speed,0.04))
            button_click=False
    
    #Direction Checks
    if(GPIO.input(16) == GPIO.LOW or GPIO.input(19) == GPIO.LOW):
        #print("left")
        if moves[-1]!="R":
            init = left(init)
            moves+=["L"]
            time.sleep(0.2)
            button_click=True
        
    if(GPIO.input(12) == GPIO.LOW or GPIO.input(13) == GPIO.LOW):
        #print("right")
        if moves[-1]!="L":
            init = right(init)
            moves+=["R"]
            time.sleep(0.2)
            button_click=True

    if(GPIO.input(17) == GPIO.LOW or GPIO.input(6) == GPIO.LOW):
        #print("down")
        if moves[-1]!="U":
            init = down(init)
            moves+=["D"]
            time.sleep(0.2)
            button_click=True

    if(GPIO.input(25) == GPIO.LOW or GPIO.input(5) == GPIO.LOW):
        #print("up")
        if moves[-1]!="D":
            init = up(init)
            moves+=["U"]
            time.sleep(0.2)
            button_click=True
    #time.sleep(0.2)

print("GAME OVER!")
print("SCORE: ", len(init)-3)

lcd.text("SCORE: "+str(len(init)-3), 2)

with canvas(device) as draw:
    text(draw, (2, 1), "GAME", fill="white", font=proportional(LCD_FONT))
    text(draw, (2, 8), "OVER", fill="white", font=proportional(LCD_FONT))
    text(draw, (2, 16), "Score:"+str(len(init)-3), fill="white", font=proportional(ATARI_FONT))

time.sleep(5)
device.clear()
GPIO.cleanup()
lcd.clear()
'''
for y in range(5):
        with canvas(device) as draw:
            for x in init:
                #for y in range(device.width):
                        draw.point((x[0]+y,x[1]),fill="white")
        time.sleep(0.5)

        
for y in range(5):
        with canvas(device) as draw:
            for x in init:
                #for y in range(device.width):
                        draw.point((x[0]+y,x[1]-y),fill="white")
        time.sleep(0.5)
'''

#Move point across
'''with canvas(device) as draw:
        #draw.line((x1,y1,x2,y2),fill="white")
        draw.line((x1,y1,x3,y3),fill="white")
        draw.line((x3,y3,x2,y2+4),fill="white")

        

for x in range(device.width):
    #for y in range(device.width):
        with canvas(device) as draw:
            draw.point((x,y),fill="white")
        time.sleep(0.5)
        

with canvas(device) as draw:
        draw.line((x,y,device.width,0),fill="white")
'''

#draw.point((point_x,point_y)
#draw.line((start_x,start_y,end_x,end_y))

'''
for i in range(device.width-snake_length):
    with canvas(device) as draw:
        draw.line((x1+i,y1,x2+i,y2),fill="white")
        snake_length+=1
        x2=x1+snake_length
        #Generate food (HARD CODING AVOID COLLISIONS FOR NOW (Gotta dynamically check)
        food_x=random.randrange(0,31)
        food_y=random.randrange(3,24)
        draw.point((food_x,food_y),fill="white")
    time.sleep(0.5)
print("EXITED")
time.sleep(1)
with canvas(device) as draw:
    text(draw, (2, 1), "HAHA!", fill="white", font=proportional(TINY_FONT))
    text(draw, (2, 8), "You lose", fill="white", font=proportional(TINY_FONT))
    text(draw, (2, 16), "Score: "+str(snake_length), fill="white", font=proportional(TINY_FONT))
    '''



    





