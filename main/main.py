import json
from machine import Pin, SPI,RTC,WDT
from WiFiConfig import WiFiConfig
from Tool import write_config,read_config,cheak_config,timeCalibration,randomPass,gc
from config import wifiConfigNVS,time,getID,lcdFont
from ui.screen import WifiConnectScreen,screen_time,screen_test
from function.mqtt import KsMqtt
from ui.default import UI_display,dh
from function.network_request import get_weather


idd = getID()


# if not cheak_config(deviceIdConfigNVS,"INT","STR"):
#     idd = randomPass(10)
#     write_config(deviceIdConfigNVS,"INT","STR",idd)

# wdt = WDT(timeout=30000)

wifi_screen = WifiConnectScreen()

p2 = Pin(2, Pin.OUT)
ksWifi = WiFiConfig(wifi_screen)
ksWifi.setWifiConfigNVS(wifiConfigNVS)
# ksWifi.setWdt(wdt)

ksMqtt = KsMqtt()
rtc = RTC()

tick = 61  # 每秒刷新标志位
weather = None


if __name__ == '__main__':
    wifi_screen.start()
    

    if not cheak_config(wifiConfigNVS,"INT","STR"):  # 判断wifi配置信息存在？

        print('wifi no config')
        ksWifi.open_ap()
        ksWifi.http_listener()

    else:
        if ksWifi.open_sta(read_config(wifiConfigNVS,"INT","STR")):

            print('wifi connect succeed')
        else:
            if not ksWifi.anew_wifi(read_config(wifiConfigNVS,"INT","STR")):
                print("wifi anew error. await anew config")

                ksWifi.open_ap()
                ksWifi.http_listener()
#                 http_listener(ksWifi.open_http())

    print("main state")
    timeCalibration()
    
    
    ksMqtt.mqttConnect()
#     wdt.feed()
    
    weather = get_weather()
    
    
    while True:
        
        
        datetime = rtc.datetime()
        
        
        if datetime[5] % 30 == 0 and datetime[6] == 0:
            
            weather = get_weather()
            
        
        if tick != datetime[6]:
            tick = datetime[6]
#             wdt.feed()
            UI_display(weather,datetime)
            
        if gc.mem_free() < 30000:
            gc.collect()
        dh()
        
        time.sleep_ms(50)
        
    




# SCL   SDA    RST  DC  CS  BLK
# 13    12     14   27  26  25




