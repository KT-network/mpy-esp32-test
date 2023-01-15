from umqtt.simple import MQTTClient
import _thread

from Tool import write_config, read_config, cheak_config, json
from config import mqttConfigNVS, getMqttConfig, mqttTimer, time
from function.controller import *


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
        if not cheak_config(mqttConfigNVS, "INT", "STR"):
            write_config(mqttConfigNVS, "INT", "STR", json.dumps(getMqttConfig()))

        params = read_config(mqttConfigNVS, "INT", "STR")
        jo = json.loads(params)

        self.mqttServer = MQTTClient(client_id=jo['client_id'], server=jo['server'], port=int(jo['port']),
                                     user=jo['user'], password=jo['passwd'], keepalive=int(jo['keepalive']))

        try:
            self.state = self.mqttServer.connect()
            print("mqttServer连接状态：", self.state)

        except:
            self.mqttAnew("connect")

        # mqtt 连接成功后启动所有功能
        if self.state == 0:
            self.state_wait_msg = True
            self.mqttServer.set_callback(self.mqttCallback)  # 消息接收回调
            self.mqttServer.subscribe(jo['subscribeTopic'])  # 订阅消息
            self.mqttMaintain()  # 心跳包
            self.mqttWaitMsgThreadStart()  # 消息接收堵塞线程
            print("成功")

    # 关闭mqtt
    def mqttClose(self):
        if self.state == 0:
            self.state = -1
            mqttTimer.deinit()
            self.state_wait_msg = False
            # time.sleep(10)

            try:
                self.mqttServer.disconnect()
            except:
                self.mqttServer = None

    # 消息接收函数
    def mqttCallback(self, topic, msg):
        #         print("消息接收函数")
        print(topic, msg)
        try:
            jo = json.loads(msg)
            print(jo)
            if jo["behavior"] == 0:
                ctrl_led(jo["action"])
            elif jo["behavior"] == 1:
                pass
        except:
            pass

    # 发布消息
    def mqttPublish(self, topic, msg):
        if self.state == 0:
            try:
                self.mqttServer.publish(topic, msg.encode('utf-8'))
            except:
                self.mqttAnew("mqttPublish")

    # 发布心跳包
    def mqttPublishTimer(self, t):
        #         print("mqttPublishTimer:",self.state)
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
        # print(threadTag)
        # print(threadTag.get_ident())

    # mqtt断开连接时
    def mqttAnew(self, msg):
        if not self.anewLock:
            print("mqttAnew", msg)  # logi 在哪里断开 调用的
            self.anewLock = True
            self.mqttClose()

            time.sleep(10)

            self.mqttConnect()
