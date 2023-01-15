from umqtt.simple import MQTTClient
import _thread
from machine import Timer
import time

mqttTimer = Timer(0)

'''
该库基于 umqtt 进行了二次功能封装
函数功能介绍:
    1.mqttConnect      -> 建立与服务器的连接
    2.mqttClose        -> 关闭与服务器的连接
    3.mqttCallback     -> 消息接收回调函数
    4.mqttPublish      -> 发布消息
    5.mqttPublishTimer -> 与服务器建立心跳包的消息发布函数。与 mqttPublish 函数相同，指定了话题与消息内容
    6.mqttMaintain     -> 启动心跳包功能。使用 Timer 功能
    7.__mqttWaitMsg    -> 原函数 wait_msg 接收消息会堵塞主线程，并且调用一次接收一次消息。现用 while 不间断接收消息，并放在一个新线程中
    8.mqttWaitMsgThreadStart -> 创建一个新线程，用于 __mqttWaitMsg 函数的运行
    9.mqttAnew         -> mqtt 断开连接时进行重连操作（有bug）。发布函数与消息接收函数出现异常时，即可代表 mqtt断开连接或wifi断开连接
                            （如果wifi断开连接，在短时间内重新连接上wifi后，此函数可以使mqtt重新连接上。反之，开发板会因内存溢出重启）
                            
    —— by. 坤少(QQ:841369846)
'''


class KsMqtt:

    def __init__(self):
        self.mqttServer = None  # mqtt 对象
        self.state = -1  # 全局mqtt 连接状态
        self.state_wait_msg = False  # 消息接收线程结束
        self.anewLock = False  # mqtt断开后重新连接锁

    def mqttConnect(self):
        self.anewLock = False
        if self.state == 0:
            pass

        self.mqttServer = MQTTClient(client_id='', server='', port=int('port'),
                                     user='user', password='passwd', keepalive=int('keepalive'))

        try:
            self.state = self.mqttServer.connect()
            print("mqttServer连接状态：", self.state)

        except:
            self.mqttAnew("connect")

        # mqtt 连接成功后启动所有功能
        if self.state == 0:
            self.state_wait_msg = True
            self.mqttServer.set_callback(self.mqttCallback)  # 消息接收回调
            self.mqttServer.subscribe('topic')  # 订阅话题
            self.mqttMaintain()  # 心跳包
            self.mqttWaitMsgThreadStart()  # 消息接收堵塞线程

    # 关闭mqtt
    def mqttClose(self):
        if self.state == 0:
            self.state = -1
            mqttTimer.deinit()
            self.state_wait_msg = False
            try:
                self.mqttServer.disconnect()
            except:
                self.mqttServer = None

    # 消息接收函数
    def mqttCallback(self, topic, msg):
        '''
        :param topic: 话题
        :param msg: 消息
        可自定义消息内容 控制引脚
        msg = {"behavior": 0,"action": {"pin": [12, 14,27,26,25,33],"value": [1,1,1,1,1,1]}}
        import json
        from machine import Pin
        jo = json.loads(msg)
        action = jo['action']

        pin = action['pin']
        value = action['value']
        for i in range(len(pin)):
            Pin(pin[i], Pin.OUT, value=value[i])


        '''
        print(topic, msg)

    # 发布消息
    def mqttPublish(self, topic, msg):
        if self.state == 0:
            try:
                self.mqttServer.publish(topic, msg.encode('utf-8'))
            except:
                self.mqttAnew("mqttPublish")

    # 发布心跳包
    def mqttPublishTimer(self, t):

        if self.state == 0:
            try:
                self.mqttServer.publish("esp32MqttMaintain", "1".encode('utf-8'))
            except:
                self.mqttAnew("mqttPublishTimer")

    # 心跳包发送 使用定时器 每5秒发送一次
    def mqttMaintain(self):
        # mode = Timer.PERIODIC --> 1
        mqttTimer.init(period=5000, mode=1, callback=self.mqttPublishTimer)

    # 使用堵塞接收消息
    def __mqttWaitMsg(self):

        while self.state_wait_msg:
            #             print("mqttWaitMsg:",self.state)
            if self.state == 0:
                try:
                    if self.state == 0:
                        self.mqttServer.wait_msg()
                except:
                    if self.state == 0:
                        self.mqttAnew("__mqttWaitMsg")
                time.sleep_ms(100)

    # 消息监听 创建线程
    def mqttWaitMsgThreadStart(self):
        _thread.start_new_thread(self.__mqttWaitMsg, ())


    # mqtt断开连接时
    def mqttAnew(self, msg):
        if not self.anewLock:
            print("mqttAnew", msg)  # log 在哪里断开 调用的
            self.anewLock = True
            self.mqttClose()

            time.sleep(10)

            self.mqttConnect()
