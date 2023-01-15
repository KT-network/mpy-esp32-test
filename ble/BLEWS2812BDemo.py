from machine import Pin
from machine import Timer
from neopixel import NeoPixel
import ubluetooth

# 创建像素序列对象
# 服务于板载WS2812B
np = NeoPixel(Pin(15), 1)
np[0] = (128, 0, 0)
np.write()


# 接收消息设置颜色的方法
def processMsg(colorStr):
    cl = colorStr.split(",")
    np[0] = (int(cl[0]), int(cl[1]), int(cl[2]))
    np.write()


class ESP32_BLE():
    def __init__(self, name):
        # 用于显示蓝牙连接状态的指示灯
        self.led = Pin(13, Pin.OUT)
        # 完成未连接状态指示灯闪烁任务的定时器
        self.timer1 = Timer(0)
        # 蓝牙设备名称
        self.name = name
        # 创建BLE类对象
        self.ble = ubluetooth.BLE()
        # 激活，使用任何其他相关操作前必须先激活
        self.ble.active(True)
        # 设置未连接状态定时器闪烁任务
        self.disconnected()
        # 设置蓝牙状态发生变化时的中断回调方法
        self.ble.irq(self.ble_irq)
        # 注册蓝牙
        self.register()
        # 广播蓝牙
        self.advertiser()
        # 接收的消息字符串
        self.bleMsg = ""

    # 状态切换为连接的方法
    def connected(self):
        # 指示灯常量
        self.led.value(1)
        # 执行指示灯闪烁的定时器关闭
        self.timer1.deinit()

    # 在未连接状态设置定时器
    # 以完成指示灯闪烁的任务
    def disconnected(self):
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    # 中断回调方法
    def ble_irq(self, event, data):
        # 连接成功事件
        if event == 1:
            # 关闭闪烁定时器
            self.connected()
        # 断开事件
        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT:
            # 广播蓝牙
            self.advertiser()
            # 指示灯闪烁
            self.disconnected()
        # 收到数据
        elif event == 3:
            # 读取数据字节序列
            buffer = self.ble.gatts_read(self.rx)
            # 转换为字符串
            self.bleMsg = buffer.decode('UTF-8').strip()
            # 打印
            print(self.bleMsg)

    # 注册服务
    def register(self):
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)

        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART,)
        ((self.tx, self.rx,),) = self.ble.gatts_register_services(SERVICES)

    # 发送数据
    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    # 广播蓝牙
    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(adv_data)
        print("\r\n")


ble = ESP32_BLE("ESP32BLE")
print("connected ....")

while True:
    if (len(ble.bleMsg) > 0):
        processMsg(ble.bleMsg)
        # 返回消息
        ble.send("from esp32\r\n")
        print("send ....")
        # 清空消息
        ble.bleMsg = ""
