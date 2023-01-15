from machine import Pin
from config import mqttConfigNVS,weatherConfigNVS,wifiConfigNVS
from Tool import write_config,read_config,cheak_config,json


def ctrl_led(action):
#     jo = json.loads(action)
    pin = action['pin']
    value = action['value']
    
    for i in range(len(pin)):
        Pin(pin[i], Pin.OUT, value=value[i])
    
    print("完成")
    


def config_nvs(action):
    nvs = action['NVS']
    
    if nvs == "wifi":
        pass
    elif nvs == "weather":
        pass
    elif nvs == "mqtt":
        pass
    
    
    pass



