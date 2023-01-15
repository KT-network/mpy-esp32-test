from machine import SPI,Pin,PWM
import st7735
import time,random
from bmpdecoder import bmpData,bmpFileData

def initDisplay():
    global display,tftVdd
    tftVdd = PWM(Pin(5),freq =1000,duty = 1023)
    display = st7735.TFT(
        SPI(1,baudrate=60000000, polarity=0, phase=0,
            sck=Pin(0),mosi=Pin(1),miso=Pin(9)),
        10,2,3)#spi, aDC, aReset, aCS,ScreenSize = (160, 160)
    display.initr()
    display.invertcolor(True)
    display.rotation(1)
    display._offset = (1,26)#(26,1)
    display.fill(0)
    
initDisplay()

import zhFont2tft as font

tftfont = font.Font16('font1616.ebin')
tftfont.text(0,0,'中文测试，你好世界.hello world',display,color = [0,255,0],backgroundcolor = [255,0,0])