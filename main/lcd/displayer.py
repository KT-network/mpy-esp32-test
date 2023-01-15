
from LcdTest import *

from machine import Pin, I2C, SPI
import time
def color565(r, g=0, b=0):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3
# def display(type = '0.96'):
#   if type == '2.8':
#     spi = SPI(
#         2,
#         baudrate=60000000,
#         miso=Pin(19),
#         mosi=Pin(23),
#         sck=Pin(18))
#     display = ILI9341(
#         spi,
#         cs=Pin(1),
#         dc=Pin(5),
#         rst=Pin(3),
#         r=0)
#   elif type == '0.96':
#     spi = SPI(
#         2,
#         baudrate=60000000,#600000001.8
#         miso=Pin(19),
#         mosi=Pin(23),
#         sck=Pin(18))
#
#     display = ST7735(
#         spi,
#         cs = Pin(1),
#         dc = Pin(5),
#         rst = Pin(3),
#         r=3,
#         type = '0.96')
#   elif type == '1.8':
#     spi = SPI(
#         2,
#         baudrate=60000000,#600000001.8
#         miso=Pin(19),
#         mosi=Pin(23),
#         sck=Pin(18))
#
#     display = ST7735(spi,
#         cs = Pin(1),
#         dc = Pin(5),
#         rst = Pin(3),
#         r=0,
#         type = '1.8')
#   elif type == '1.4':
#     spi = SPI(
#         2,
#         baudrate=60000000,#600000001.8
#         miso=Pin(19),
#         mosi=Pin(23),
#         sck=Pin(18), polarity=1)
#     display = ST7789(
#         spi,
#         cs= Pin(1, Pin.OUT),#
#         dc=Pin(5, Pin.OUT),
#         rst=Pin(3, Pin.OUT),#
#         r = 0)
#   return display



if __name__ == '__main__':

    spi = SPI(
        2,
        baudrate=60000000,#600000001.8
        miso=Pin(19),
        mosi=Pin(23),
        sck=Pin(18))

    display = ST7735(spi,
        cs = Pin(1),
        dc = Pin(5),
        rst = Pin(3),
        r=0,
        type = '1.8')

    display.init()
    display.fill(0,0,100,100)