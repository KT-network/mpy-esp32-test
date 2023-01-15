import network
import time
import mqttLib

wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_sta.connect('ssid', 'passwd')

print("正在连接WiFi", end="")
while not wlan_sta.isconnected():
    print(".", end="")
    time.sleep_ms(800)

mqtt = mqttLib.KsMqtt()
mqtt.mqttConnect()


