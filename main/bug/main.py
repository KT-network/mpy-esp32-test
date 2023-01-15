import json
from machine import Pin, SPI
from KsWifiConfig import open_ap, open_http, open_sta, close_ap, anew_wifi, wifi_screen_msg
from esp32 import NVS

# from st7735_old.ST7735 import TFT
# from st7735_old import ST7735
# from Tool import *
# from ui.screen import WifiConnectScreen
# from function.mqtt import *

# wifi_screen = WifiConnectScreen()

p2 = Pin(2, Pin.OUT)
config = NVS('config')


def write_config(strs):
    config.set_i32('WIFI_CONFIG_INT', len(strs))
    config.set_blob('WIFI_CONFIG_STR', strs)
    config.commit()
    print('config write succeed')


def read_config():
    buffer = config.get_i32('WIFI_CONFIG_INT')
    buf = bytearray(buffer)
    config.get_blob('WIFI_CONFIG_STR', buf)
    return buf.decode('utf-8')


def response(conn, body):
    conn.send(b'HTTP/1.1 200 OK\r\n\r\n')  # 服务器发送数据时的响应头
    conn.send(json.dumps(body))  # 服务器响应内容
    conn.close()


def cheak_config():
    try:
        num = config.get_i32("WIFI_CONFIG_INT")  # 存入wifi json信息位数
        buf = bytearray(num)
        config.get_blob("WIFI_CONFIG_STR", buf)  # 存入wifi 信息
        return True
    except:
        return False


def http_listener(server):
    while True:
        conn, addr = server.accept()
        print("\n\n connect path %s" % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print(request)

        if len(request) > 0:
            body = request[request.index("{"):request.index("}") + 1]
            if not len(body) > 0:
                response(conn, {'code': '400', 'msg': 'error', 'data': '缺少参数'})

            body_jo = json.loads(body)

            if body_jo['type'] == "0":
                write_config(body)
                if open_sta(body):

                    response(conn, {'code': 200, 'msg': 'succeed', 'data': 'wifi 配置并连接成功'})
                    close_ap()
                    # wifi_screen.close()
                    break
                else:
                    response(conn, {'code': 400, 'msg': 'error', 'data': 'wifi 连接失败，请重新配置'})

            else:
                if open_sta(body):
                    response(conn, {'code': 200, 'msg': 'succeed', 'data': 'wifi 连接成功'})
                    close_ap()
                    break
        else:
            response(conn, {'code': '400', 'msg': 'error', 'data': '缺少参数'})


if __name__ == '__main__':

    #     wifi_screen.start()
    #     wifi_screen_msg(wifi_screen)

    if not cheak_config():  # 判断wifi配置信息存在？

        print('wifi no config')
        open_ap()
        http_listener(open_http())

    else:
        if open_sta(read_config()):

            print('wifi connect succeed')
        else:
            if not anew_wifi(read_config()):
                print("wifi anew error. await anew config")

                open_ap()
                http_listener(open_http())

    print("main state")
#     timeCalibration()

# mqttConnect()

#     while True:
#         mqttWaitMsg()


# SCL   SDA    RST  DC  CS  BLK
# 13    12     14   27  26  25



