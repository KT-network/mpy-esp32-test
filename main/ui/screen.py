from config import lcd,lcdFont
import _thread
import time
import gc

WHITE = lcd.rgb(255, 255, 255)

def clear():
    lcd.clear(0)
    lcd.show()
    gc.collect() 

class WifiConnectScreen:

    def __init__(self):
        self.__state = False
        self.__msg = "loading..."

    def setMsg(self, msg):
        self.__msg = msg

    def getState(self):
        return self.__state

    def start(self):
        if not self.__state:
            self.__state = True
            _thread.start_new_thread(self.__wifi_connect_screen,())

    def close(self):
        self.__state = False
        time.sleep(1)
        clear()
        

    def __wifi_connect_screen(self):
        numX = 16  # 小方块的初始位置
        numW = 20  # 小方块的长度
        while self.__state:
            lcd.clear(0)
            lcd.drawRect(14, 50, 100, 10, WHITE, False)
            # lcdFont.text(display=lcd,string=self.__msg,x=0,y=70)
            lcd.text(self.__msg, 0, 80,WHITE)

            if numX > 92:
                # 8            100
                numWE = 112 - numX

                # 12            8
                numWS = 20 - numWE
                lcd.drawRect(numX, 52, numWE, 6, WHITE, True)
                lcd.drawRect(16, 52, numWS, 6, WHITE, True)
            else:
                lcd.drawRect(numX, 52, numW, 6, WHITE, True)

            if numX > 112:
                numX = 16

            lcd.show()
            numX += 1



def screen_time(datetime):
    
    year = datetime[0]
    month = datetime[1]
    day = datetime[2]
    week = datetime[3]
    
    second = datetime[6]
    minute = datetime[5]
    hour = datetime[4]
    
    times = "/"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
    print(times)
    lcd.clear(0)
    lcdFont.text(display=lcd,string=times,x=0,y=70,color=WHITE)
    
    
    # lcd.drawText(times, WHITE, 0, 70)
    lcd.show()
    
def screen_test(strs,size):
    
    
    lcd.clear(0)
    lcdFont.text(display=lcd,string=strs,x=0,y=70,color=WHITE,font_size=size)
    
    
    # lcd.drawText(times, WHITE, 0, 70)
    lcd.show()

    
    
    
    

