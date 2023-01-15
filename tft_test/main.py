from machine import SPI,Pin
from sysfont import sysfont
import st7735
import time
from st7735 import TFTColor
from bmpdecoder import bmpDecoder
displayOn = Pin(10,Pin.OUT,value = 1)
spi = SPI(1,baudrate=60000000, polarity=0, phase=0)
display = st7735.TFT(spi,5,3,2)#a0
display._size = (128,160)
display.initg()
display.fill(0)
display.text((5,100),"ESP32 C3",TFTColor(255,255,255),sysfont)
t = time.ticks_us()
bmpDecoder("2233_3.bmp",display,[100,50])
print((time.ticks_us()-t)/1000000)
#bmpDecoder("2233_2.bmp",display)
#print((time.ticks_us()-t)/1000000)