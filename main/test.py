from config import *
from config import lcd,lcdFont,lcdTexture
from Tool import *
from framebuf import FrameBuffer, RGB565
from libs.st7735 import Texture
WHITE = lcd.rgb(255, 255, 255)


# aa = loadPics1("res/simple.bnbapic")


# idd = randomPass(8)+"-"+str(time.time())
# print(idd)
# erase_config(mqttConfigNVS, "INT", "STR")
# erase_config(deviceIdConfigNVS,"INT","STR")
# erase_config(wifiConfigNVS,"INT","STR")
# erase_config(weatherConfigNVS, "INT", "STR")

# a = cheak_config(mqttConfigNVS, "INT", "STR")
# b = cheak_config(deviceIdConfigNVS,"INT","STR")
# c = cheak_config(wifiConfigNVS,"INT", "STR")
# d = cheak_config(weatherConfigNVS, "INT", "STR")


# a = read_config(mqttConfigNVS, "INT", "STR")
# b = read_config(deviceIdConfigNVS,"INT","STR")
# c = read_config(wifiConfigNVS,"INT", "STR")
# d = read_config(weatherConfigNVS, "INT", "STR")



lcd.blit(loadPics("res/weather/7.kspic").buf,80,0)
# # lcdFont.text(display=lcd,string="户县",x=0,y=0,color=WHITE)
# # # lcdFont.text(display=lcd,string="阴",x=28,y=0,color=WHITE)
# #
# # print(gc.mem_free())
lcd.show()
# print(gc.mem_free())
# print(len(loadPics("res/weather/7.kspic").buf))


