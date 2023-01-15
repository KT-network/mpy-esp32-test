import time
import network
from neopixel import NeoPixel
import onewire
import ds18x20
import socket
from uQR import QRCode
from machine import Pin, SPI
from st7735 import ST7735
from machine import Timer

spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(13), mosi=Pin(12))
ds18b20 = ds18x20.DS18X20(onewire.OneWire(Pin(32)))
ssid = "123"
password = "123456789"
led1 = Pin(2, Pin.OUT, Pin.PULL_DOWN)
lcd = ST7735(50, 50, spi, dc=Pin(27), cs=Pin(26), rst=Pin(14), rot=2, bgr=1)
led2 = 13
rgb_num = 35
rgb_led = NeoPixel(Pin(led2, Pin.OUT), rgb_num)
DS18B20 = 0
# 定义RGB颜色
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (138, 43, 226)
COLORS = (RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET)


def DISPLAY():
    qr = QRCode(border=2)
    qr.add_data("http://n44259438f.wicp.vip:43455")  # 这里是要生成的二维码，被扫码之后的得到的内容
    matrix = qr.get_matrix()

    row_len = len(matrix)
    col_len = len(matrix[0])
    # 放大倍数
    # 默认情况下输出的二维码太小，可以按照你实际屏幕的大小进行缩放，当前我的240x240屏幕缩放8倍正合适
    scale_rate = 2

    for row in range(row_len * scale_rate):
        for col in range(col_len * scale_rate):
            if matrix[row // scale_rate][col // scale_rate]:
                lcd.pixel(row, col, ST7735.rgb(0, 255, 255, 255))
            else:
                lcd.pixel(row, col, ST7735.rgb(0, 0, 0, 0))
            col += 1
        row += 1
        lcd.show()  # 显示出来   


def RGB():
    for color in COLORS:
        for i in range(rgb_num):
            rgb_led[i] = (color[0], color[1], color[2])
            rgb_led.write()
            time.sleep_ms(100)
        time.sleep_ms(1000)


def wifi_connect():
    wlan = network.WLAN(network.STA_IF)  # STA模式
    wlan.active(True)  # 激活

    if not wlan.isconnected():
        print("连接到网络conneting to network...")
        wlan.connect(ssid, password)  # 输入账号和密码】

        while not wlan.isconnected():
            led1.value(1)
            time.sleep_ms(300)
            led1.value(0)
            time.sleep_ms(300)
        led1.value(0)
        return False


    else:
        led1.value(0)
        print("连接到网络", wlan.ifconfig())
        return True


def web_page():
    dht11 = str(DS18B20)
    if led1.value() == 0:
        gpio_state = "off"

    else:
        gpio_state = "no"

    html = """<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset ="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>柳木枫网站</title>>
        <style>
            body {
                margin: 0;
            }
        </style>
    </head>
    <body>
       <div style="
         background-color:#f1f1f1;
         text-align: center;
         padding:4px
       ">
         <img src='http://phototj.photo.store.qq.com/psc?/V12omYFl17X79A/bqQfVz5yrrGYSXMvKr.cqdT8NdAMOu.wozqbDXbhJL4To19jNT.wPWge.5BM5LeUJb5bdY3jKG1Atb5AQ60h3nniKlchumcN.ZzbmDVSbJk!/b&bo=VQhABlUIQAYBByA!&rf=viewer_4'alt="刘一泽" width="40px"height="40px"center >


       </div>
         
        <div>

           <style>
              html{font-family: Helvetica; display: inline-block; margin: Opx auto; text-align: center;}
              h1{color: #0F3376; padding: 2vh;}
              p{font-size: 10,1px;}.button{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 40px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}.button2{background-color:#0f4498; border: none; border-radius: 40px;}.button3{background-color:#0f4498; border: none; border-radius: 40px;}
              



            </style>
           <body> 
               <h1>庞贵友的RGB灯</h1>
               <p>
                 <big><b>是否开灯；</b></big><strong>""" + gpio_state + """</strong>
               </p>
               <p>

                <big><b>温   度；</b></big><strong>""" + dht11 + """</strong>
              </p>
               <P>
                   <a href="/?led=on"> <button class= "button ">  no </button> </a>
               </p>
                <p>
                    <a href="/?led=off"> <button class= "button button2"> off </button> </a>
                </p>
           </body> 


        </div>




        
       <div style= 
       background-color:#f1f1f1;
       text-align: center;
       padding:40px
       font-size: 12px;
     ”>
       <p>庞贵友</p>
       <a  href="https://www.bilibili.com/video/BV1n24y1Z7UU?p=119&vd_source=4161588e56fa43e682c8848fe589cef9">ESP32</a>
    </div>
   
       
    </body> 
</html>"""
    return html


def callback(t):
    global DS18B20
    ds18b20.convert_temp()
    time.sleep(1)
    for rom in roms:
        ABC = ds18b20.read_temp(rom)
        print("DS18B20检测温度是：%2f°C" % ABC)
        DS18B20 = ABC
    client, addr = my_socket.accept()
    print('Got a connection from %s' % str(addr))
    request = client.recv(1024)  # 接收数据
    request = str(request)
    print('content= %s' % request)
    response = web_page()
    client.send('HTTP/1.1 200 OK\n')
    client.send('Content-Type: text/html\n')
    client.send('Connection:close\n\n')
    client.sendall(response)
    client.close()


if __name__ == "__main__":
    lcd.fill(10)
#     roms = ds18b20.scan()  # 扫描设备
#     print("初始化成功")
# 
#     lcd.font_load('./GB2312-12.fon')  # 加载字体 
# 
#     if wifi_connect():
#         my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         my_socket.bind(('', 80))
#         my_socket.listen(5)
#         DISPLAY()
#         tim0 = Timer(0)
#         tim0.init(period=500, mode=Timer.PERIODIC, callback=callback)
# 
#         while True:
# 
#             client, addr = my_socket.accept()
#             print('Got a connection from %s' % str(addr))
#             request = client.recv(1024)  # 接收数据
#             request = str(request)
#             print('content= %s' % request)
#             led_on = request.find('/?led=on')
#             led_off = request.find('/?led=off')
#             if led_on == 6:
#                 print('led=on')
#                 led1.value(1)
# 
#             if led_off == 6:
#                 print('led=off')
#                 led1.value(0)
# 
#             response = web_page()
#             client.send('HTTP/1.1 200 OK\n')
#             client.send('Content-Type: text/html\n')
#             client.send('Connection:close\n\n')
#             client.sendall(response)
#             client.close()
