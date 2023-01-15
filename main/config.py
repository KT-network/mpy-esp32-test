from esp32 import NVS
from machine import Timer, Pin, SPI
import random
import time
from libs.st7735 import st7735, Texture, ufont

# from libs.st7735_old.BNST7735Driver import BNST7735Driver, BNColor, ScreenSize
# import libs.st7735_old.FileUtil as fu
#
# bnsd = BNST7735Driver(13, 12, 14, 27, 26, 25)


# 初始化屏幕
lcdSpi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(13), mosi=Pin(12))
lcd = st7735.ST7735(128, 160, lcdSpi, dc=Pin(27), cs=Pin(26), rst=Pin(14), rot=2, bgr=1)
lcdTexture = Texture.Texture
# 加载字体
lcdFont = ufont.BMFont("res/font/tft-unifont-15.bmf")

# 随机
def randomPass(n):
    strs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
            'w', 'x', 'y', 'z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    s = ''
    for i in range(n):
        s += str(strs[random.randint(0, len(strs) - 1)])
    return s


def read_configs(config, key1, key2):
    buffer = config.get_i32(key1)
    buf = bytearray(buffer)
    config.get_blob(key2, buf)
    return buf.decode('utf-8')


# NVS 配置初始化
wifiConfigNVS = NVS('wifiConfig')  # wifi配置信息
weatherConfigNVS = NVS('weatherConfig')  # 天气配置信息
mqttConfigNVS = NVS('mqttConfig')  # mqtt配置信息
deviceIdConfigNVS = NVS('deviceIdConfig')  # 设备id信息 （重新烧录代码会改变）


def getID():
    try:
        num = deviceIdConfigNVS.get_i32("INT")  # 存入wifi json信息位数
        buf = bytearray(num)
        deviceIdConfigNVS.get_blob("STR", buf)  # 存入wifi 信息
        return buf.decode('utf-8')

    except:
        idd = randomPass(10)
        deviceIdConfigNVS.set_i32("INT", len(idd))
        deviceIdConfigNVS.set_blob("STR", idd)
        deviceIdConfigNVS.commit()

        return idd


# 天气配置
weatherUrl = "https://devapi.qweather.com/v7/weather/now"
weatherUrlTest = "http://124.70.108.79:2511/get/weather"
weatherConfig = {
    "key": "",
    "location": "101110106",
    "lang": "",
    "unit": "",
    "time": "60",
    "path":[25143,21439]
}


# mqtt配置

def getMqttConfig():
    try:
        num = deviceIdConfigNVS.get_i32("INT")  # 存入wifi json信息位数
        buf = bytearray(num)
        deviceIdConfigNVS.get_blob("STR", buf)  # 存入wifi 信息
        mqttConfig = {
            "client_id": "Ks-MicroPython-esp32-mqtt-client_id-" + getID(),
            "server": "124.70.108.79",
            "port": 1883,
            "user": "admin",
            "passwd": "123456",
            "keepalive": 10,
            "subscribeTopic": "Ks/MicroPython/esp32/mqtt/subscribe/" + getID()
        }

        return mqttConfig
    except:
        return None


mqttTimer = Timer(0)
