from rpi_lcd import LCD
import time
lcd = LCD()


try:
    lcd.text("SCORE: 0",1)
    lcd.text("SNAKE",2)
except:
    pass
finally:
    time.sleep(3)
    lcd.clear()