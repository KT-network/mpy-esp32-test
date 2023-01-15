import network
import socket
import json
import time
from Tool import write_config

class WiFiConfig:

    def __init__(self, screen):
        self.wlan_ap = network.WLAN(network.AP_IF)
        self.wlan_sta = network.WLAN(network.STA_IF)
        self.screen = screen
        self.server = None
        self.wdt = None
        
    
    def setWifiConfigNVS(self,wifiConfigNVS):
        self.wifiConfigNVS = wifiConfigNVS
    
    def setWdt(self,wdt):
        self.wdt = wdt
    
    def open_ap(self):
        self.close_sta()
        self.wlan_ap.active()
        #self.wlan_ap.config(essid="aKun",security=4)
        self.wlan_ap.active(True)

    def close_ap(self):
        if self.server != None:
            self.server.close()
            self.wlan_ap.active(False)
            

    def open_http(self):
        if self.server != None:
            self.server.close()
            
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.wlan_ap.ifconfig()[0], 80))
        self.server.listen(5)


    def http_listener(self):
        self.open_http()
        
        while True:
            if self.wdt != None:
                self.wdt.feed()
                
            conn, addr = self.server.accept()
            print("\n\n connect path %s" % str(addr))
            request = conn.recv(1024)
            request = str(request)
            print(request)

            if len(request) <= 0:
                continue
            
            # 请求方式 POST / GET
            reqWay = request[0:6]
            

            if reqWay == 'b\'POST':
                path = request[request.index("b'POST")+7:request.index("HTTP")-1]
                
                body = request[request.index("{"):request.index("}") + 1]
                if not len(body) > 0:
                    self.response(conn, {'code': '400', 'msg': 'error', 'data': '缺少参数'})
#                     continue
                
                body_jo = json.loads(body)
                if path == "/set/wifi":
                    if body_jo['type'] == "0":
                        write_config(self.wifiConfigNVS,"INT","STR",body)
                        if self.open_sta(body):
                            self.response(conn, {'code': 200, 'msg': 'succeed', 'data': 'wifi 配置并连接成功'})
                            time.sleep(1)
                            self.close_ap()
                            self.screen.close()
                            break
                        else:
                            self.response(conn, {'code': 400, 'msg': 'error', 'data': 'wifi 连接失败，请重新配置'})
                    else:
                        if self.open_sta(body):
                            self.response(conn, {'code': 200, 'msg': 'succeed', 'data': 'wifi 连接成功'})
                            time.sleep(1)
                            self.close_ap()
                            self.screen.close()
                            break
                    
                else:
                    self.response(conn, {'code': '400', 'msg': 'error', 'data': '请求地址错误'})
                
                

            elif reqWay == 'b\'GET ':
                print("GET")
                
    def response(self,conn, body):
        conn.send(b'HTTP/1.1 200 OK\r\n\r\n')  # 服务器发送数据时的响应头
        conn.send(json.dumps(body))  # 服务器响应内容
        conn.close()


    def open_sta(self, strs):
        print("open_sta...")
        jo = json.loads(strs)
        try:
            if self.wlan_sta.active():
                self.wlan_sta.active(False)
        except:
            pass
        #self.wlan_sta.config(dhcp_hostname="kun-esp32")
        self.wlan_sta.active(True)
        self.screen.setMsg("wifi connect...")
        self.wlan_sta.connect(jo['ssid'], jo['passwd'])
        # 判断其他信息是否存在，如果存在配置静态
        if jo['ip'] != '' and jo['mask'] != '' and jo['gateway'] != '':
            ifconfig = (jo['ip'], jo['mask'], jo['gateway'], jo['gateway'] if jo['dns'] == '' else jo['dns'])
            self.wlan_sta.ifconfig(ifconfig)

        time_out = 10 if jo['timeout'] == '' else int(jo['timeout'])
        print('open_sta timeout ...' + str(time_out))
        time.sleep(time_out)

        print('open_sta isconnected ...')
        if self.wlan_sta.isconnected() and len(self.wlan_sta.ifconfig()) == 4:
            self.screen.setMsg("wifi connect succeed")
            self.screen.close()
            return True
        else:
            self.screen.setMsg("wifi connect error")
            self.close_sta()
            return False

    def close_sta(self):
        self.wlan_sta.active(False)

    def anew_wifi(self, strs):
        jo = json.loads(strs)
        anew_num = 3 if jo['anew'] =='' else int(jo['anew'])
        while anew_num > 0:
            if self.wdt != None:
                self.wdt.feed()
            print("wifi anew ...")
            if self.open_sta(strs):
                time.sleep_ms(1000)
                print("wifi anew succeed")
                return True
            anew_num -= 1
        return False
    
        
