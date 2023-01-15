import network
import socket
import json
import time

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

wifi_screen = None


def wifi_screen_msg(wifi_screen_object):
    global wifi_screen
    wifi_screen = wifi_screen_object


def open_ap():
    close_sta()
    wlan_ap.active()
    wlan_ap.config(essid="aKun")
    wlan_ap.active(True)


def close_ap():
    wlan_ap.active(False)
    open_http().close()


def open_http():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((wlan_ap.ifconfig()[0], 80))
    server.listen(5)
    return server
    # http_listener(server)


def http_listener(server):
    while True:
        conn, addr = server.accept()
        print("\n\n connect path %s" % str(addr))
        request = conn.recv(1024)
        request = str(request)

        if len(request) > 0:
            body = request[request.index("{"):request.index("}") + 1]
            body_jo = json.loads(body)

            if body_jo['type'] == "0":
                config = {}
                config['ssid'] = body_jo['ssid']
                config['passwd'] = body_jo['passwd']
                break
            else:
                pass


def open_sta(strs):
    print("open_sta...")
    jo = json.loads(strs)
    if wlan_sta.active():
        wlan_sta.active(False)
    wlan_sta.active(True)
    wlan_sta.config(dhcp_hostname="kun-esp32")
#     wifi_screen.setMsg("wifi connect...")
    wlan_sta.connect(jo['ssid'], jo['passwd'])
    # 判断其他信息是否存在，如果存在配置静态
    if jo['ip'] != '' and jo['mask'] != '' and jo['gateway'] != '':
        ifconfig = (jo['ip'], jo['mask'], jo['gateway'], jo['gateway'] if jo['dns'] == '' else jo['dns'])
        wlan_sta.ifconfig(config=ifconfig)

    time_out = 10 if jo['timeout'] == '' else int(jo['timeout'])
    print('open_sta timeout ...' + str(time_out))
    time.sleep(time_out)

    print('open_sta isconnected ...')
    if wlan_sta.isconnected():
#         wifi_screen.setMsg("wifi connect succeed")
#         wifi_screen.close()
        return True
        # return {'code': 200, 'msg': 'succeed', 'data': 'wifi 配置并连接成功'}
    else:
#         wifi_screen.setMsg("wifi connect error")
        close_sta()
        return False
        # return {'code': 400, 'msg': 'error', 'data': 'wifi 连接失败，请重新配置'}


def close_sta():
    wlan_sta.active(False)


def anew_wifi(strs):
    anew_num = 3
    while anew_num > 0:
        print("wifi anew ...")
        if open_sta(strs):
            time.sleep_ms(1000)
            print("wifi anew succeed")
            return True
        anew_num -= 1
    return False



