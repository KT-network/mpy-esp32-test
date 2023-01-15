import libs.ksrequests as request
import time, ntptime
import json
from machine import Timer
from config import lcdTexture
import random
import gc

# 删除/擦除NVS中的某个Key
def erase_config(config, key1, key2):
    config.erase_key(key1)
    config.erase_key(key2)
    config.commit()


# 写入数据到NVS的指定key
def write_config(config, key1, key2, strs):
    config.set_i32(key1, len(strs))
    config.set_blob(key2, strs)
    config.commit()
    # print("write succer")


# 读取NVS中的key数据
def read_config(config, key1, key2):
    buffer = config.get_i32(key1)
    buf = bytearray(buffer)
    config.get_blob(key2, buf)
    return buf.decode('utf-8')


# 校验NVS是否存在某个Key
def cheak_config(config, key1, key2):
    try:
        num = config.get_i32(key1)  # 存入信息位数
        buf = bytearray(num)
        config.get_blob(key2, buf)  # 存入信息
        return True
    except:
        return False


# 拼接表单数据（弃用）
def params_joint(params):
    data = ''

    for i in params.keys():
        data = data + i + '=' + params[i] + "&"

    return data[:-1:]


# def get_weather():
#     if not cheak_config(weatherConfig, "weather_int", "weather_str"):
#         
#         write_config(weatherConfig, "weather_int", "weather_str", json.dumps(weatherConfig))
# 
#     params = read_config(weatherConfig, "weather_int", "weather_str")
#     jo = json.loads(params)
# 
#     date = int(jo['time'])
# 
#     return request.post(weatherUrlTest,json=jo).json()


# 获取ntp服务器的时间
def timeCalibration():
    ntptime.NTP_DELTA = 3155644800
    ntptime.host = 'ntp1.aliyun.com'
    anew_num = 3

    while anew_num > 0:
        try:
            ntptime.settime()
            break
        except:
            time.sleep_ms(500)
            anew_num -= 1

    mytime = time.localtime()
    mytime = '%d-%d-%d %d:%d:%d' % (mytime[0], mytime[1], mytime[2], mytime[3], mytime[4], mytime[5])
    print(mytime)


# 生成随机的字符串
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


# 读取文件指定位置的内容
def readInt(bytesArray, start):
    result = bytesArray[start] + (bytesArray[start + 1] << 8) + (bytesArray[start + 2] << 16) + (
            bytesArray[start + 3] << 24)
    return result


# 加载kspic文件
def loadPics(fname):
#     gc.collect()
    # 结果列表
    # 读取文件字节数据
    dataFile = open(fname, "rb")
    # 读取文件中的所有数据字节
    bytesData = dataFile.read()

    if bytesData[0:2] != b'KS':
        print('文件格式不正确')
        return

    # 字节计数器
    bcount = 2
    # 首先读出四个字节组装为图集中图的数量
    count = readInt(bytesData, bcount)
    bcount = bcount + 4

    w = readInt(bytesData, int(bcount))
    bcount = bcount + 4
    h = readInt(bytesData, int(bcount))
    bcount = bcount + 4
    # 提取此图片像素数据字节序列
    gc.collect()
    dataCurr = bytesData[int(bcount):int(bcount + w * h * 2)]
    
    
    return lcdTexture(w, h, dataCurr)

# 生成md5字符串
# def getMd5(txt):
#   hash_md5 = hashlib.md5()
#    txt = txt + '-ks' + str(defTime().TIMEINT)
#   data = txt.encode('utf-8')
#    hash_md5.update(data)
#    return hash_md5.hexdigest()
