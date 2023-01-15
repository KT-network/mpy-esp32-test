
from sprite import AnimatePics,BinloaderFile,SpriteFont16
from Driver.sh1106 import SH1106_I2C
from machine import Pin,I2C,freq

freq(240000000)
display = SH1106_I2C(128,64,I2C(0,scl = Pin(13),sda = Pin(12),freq=1100000),rotate=180)
f16 = SpriteFont16('font1616.bin')
f16.text(0,0,'中国汉字测试',display)
display.show()