from Tool import cheak_config,write_config,read_config,request,json,gc
from config import weatherConfigNVS,weatherUrlTest


def get_weather():
    if not cheak_config(weatherConfigNVS, "INT", "STR"):
        write_config(weatherConfigNVS, "INT", "STR", json.dumps(weatherConfig))

    params = read_config(weatherConfigNVS, "INT", "STR")
    jo = json.loads(params)
    
    try:
        data = request.post(weatherUrlTest, json=jo).json()
    except:
        data = None
        
    gc.collect()

    return data
