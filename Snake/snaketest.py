from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT,ATARI_FONT
from luma.led_matrix.device import max7219
import time

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=24, block_orientation=-90)
device.clear()

with canvas(device) as draw:
   draw.rectangle(device.bounding_box, outline="white")
   text(draw, (5, 1), "HOWDY", fill="white", font=proportional(ATARI_FONT))
   text(draw, (5, 8), "Dr Liu", fill="white", font=proportional(ATARI_FONT))
   