# 请先解码
from sprite import AnimatePics,BinloaderFile
from sh1106 import SH1106_I2C
from machine import Pin,I2C,freq

freq(240000000)
display = SH1106_I2C(128,64,I2C(0,scl = Pin(13),sda = Pin(12),freq=1100000),rotate=180)

ani = AnimatePics([],dt = 50)
for i in range(21):
    ani.framList.append(BinloaderFile('NiceAni/nice'+str(i+1)+'.bin'))
for i in range(1000):
    display.fill(0)
    ani.draw(display)
    display.show()