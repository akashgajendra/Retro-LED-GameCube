from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT, TINY_FONT, ATARI_FONT
from luma.led_matrix.device import max7219
import random
import time
import RPi.GPIO as GPIO
import busio
import time
import digitalio
import board
from math import ceil
from rpi_lcd import LCD



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


serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=24, block_orientation=-90)
device.clear()

device.clear()
time.sleep(2)
# draw hang man shape

node = [[]]
u_ast_x=14
u_ast_y=9

## LCD Array
lcd = LCD()
lcd.text("Galaxia",1)
lcd.text("Score: 0",2)

#asteroid_array = [[u_ast_x, u_ast_y],[u_ast_x+random.randrange(3,7),u_ast_y+random.randrange(4,10)],[u_ast_x+random.randrange(4,15),u_ast_y+random.randrange(4,10)],[u_ast_x+random.randrange(4,15),u_ast_y-random.randrange(4,10)]]
asteroid_array = [[u_ast_x, u_ast_y],[random.randrange(12,18),  random.randrange(0,2)],[random.randrange(15,32),random.randrange(0,20)],[random.randrange(15,32),random.randrange(0,20)]]

def add_asteroid(asteroid_array):
    while(len(asteroid_array)<10):
        test_x = random.randrange(0,15)
        test_y = random.randrange(-24,16)
        #if(test_x + u_ast_x <= 28 and test_y + u_ast_y <= 17 and test_x + u_ast_x >= u_ast_x+3 and test_y + u_ast_y >= u_ast_y):
        asteroid_array.append([random.randrange(15,32),random.randrange(0,20)])

GRID_3 = (18,0)
GRID_4 = (26,0)



def asteroids(device,asteroid_array):
    x,y=asteroid_array[-1][0],asteroid_array[-1][1]
    draw.line((x-1,y,x+1,y),fill="white")

def fire(device,node, x, y, asteroid_array):
    # fire point
    for i in range(30):
        with canvas(device) as draw:
            node = make_rocket(draw, x, y, node)
            #asteroids(device, asteroid_array)
            draw.point((node[-1][0]+i+2,node[-1][1]),fill="white")
        time.sleep(.02)

def make_rocket(draw, x, y, node):
    draw.point((x,y), fill='white')
    draw.line((x-1,y-1,x-1,y+1),fill="white")
    draw.line((x-2,y-2,x-2,y+2),fill="white")
    draw.point((x-3,y+1), fill="white")
    draw.point((x-3,y-1),fill="white")
    node.append([x,y])
    return node

score = 0
x=4
y=21

fire_x = []
fire_y = []

def up(x,y):
    return x,y-1

def down(x,y):
    return x,y+1

fire = 0
QUIT = False
while not QUIT:
    add_asteroid(asteroid_array)
    if(GPIO.input(23) == GPIO.LOW):
        QUIT = True
    for i in range(30):
        with canvas(device) as draw:
                #Make Rocket
                if(y < 2):
                    y = 2
                elif(y > 21):
                    y = 21
                draw.point((x,y), fill='white')
                draw.line((x-1,y-1,x-1,y+1),fill="white")
                draw.line((x-2,y-2,x-2,y+2),fill="white")
                draw.point((x-3,y+1), fill="white")
                draw.point((x-3,y-1),fill="white")
                node.append([x,y])
                
                
                #for i in range(30):
                if(GPIO.input(12) == GPIO.LOW):
                    draw.point((node[-1][0]+i+2,node[-1][1]),fill="white")
                    time.sleep(0.01)
                    fire_x.append(node[-1][0]+i+2)
                    fire_y.append(node[-1][1])
                    fire+=1
                
                if(GPIO.input(25) == GPIO.LOW or GPIO.input(5) == GPIO.LOW):
                    x,y=up(x,y)
                    time.sleep(0.05)
                
                if(GPIO.input(17) == GPIO.LOW or GPIO.input(6) == GPIO.LOW):
                    x,y = down(x,y)
                    time.sleep(0.05)
            
                #device.clear()
                #fire(device,node, x, y+i, asteroid_array)
                for k in range(len(asteroid_array)-1):
                    c_x,c_y=asteroid_array[k][0],asteroid_array[k][1]
                    text(draw,(c_x,c_y),"*",fill="white", font=TINY_FONT)
                    
                if(fire > 0 and len(fire_x)!=0 and len(fire_y)!=0):
                    for n in range(len(asteroid_array)-1):
                        if(fire_x[-1] == asteroid_array[n][0] + 1  and (fire_y[-1] == asteroid_array[n][1] + 3 or fire_y[-1] == asteroid_array[n][1] + 2 or fire_y[-1] == asteroid_array[n][1] + 4)):
                            print("Start   ", asteroid_array)
                            print("hit")
                            print(fire_x[-1], "   x")
                            print(fire_y[-1] ,"  y")
                            del asteroid_array[n]
                            print(asteroid_array)
                            score += 1
                            add_asteroid(asteroid_array)
                            time.sleep(0.05)
                            lcd.text("Score: " + str(ceil(score)),2)
    
                
print("GAME OVER!")
print("SCORE: ", ceil(score))


with canvas(device) as draw:
    text(draw, (2, 1), "GAME", fill="white", font=proportional(LCD_FONT))
    text(draw, (2, 8), "OVER", fill="white", font=proportional(LCD_FONT))
    text(draw, (2, 16), "Score:"+str(ceil(score)), fill="white", font=proportional(TINY_FONT))
    lcd.text("Galaxia",1)
    lcd.text("Game Over!",2)

time.sleep(5)
lcd.clear()
device.clear()
GPIO.cleanup()
    

'''
time.sleep(1.5)
with canvas(device) as draw:
        for i in range(3):
            #Left line
            draw.point((i+1,i+1),fill="white")
            # rigth line
            draw.point((3-i,3+i),fill="white")
            # base
            draw.line((1,1,1,4),fill="white")
            #point in middle
            j = i
        draw.point((j,j+1),fill="white")
            
            #draw.point((1,1),fill="white")
'''
        
time.sleep(3)
#device.clear()

#ijklmnopqrstwxyz