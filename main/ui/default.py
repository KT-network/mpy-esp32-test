from config import lcd,lcdFont,lcdTexture
from Tool import loadPics,gc
from function.network_request import get_weather


weather_tick = None
WHITE = lcd.rgb(255, 255, 255)
BLACK = lcd.rgb(0,0,0)

TIME = [61,61,61,61,61,61]

UI_Change = True
def datetime_display(datetime):
    global TIME
    
    year = datetime[0]  # 年
    month = datetime[1]  # 月
    day = datetime[2]  # 天
    week = datetime[3]  # 周
    
    second = "0" + str(datetime[6]) if len(str(datetime[6])) == 1 else str(datetime[6]) # 秒
    minute = "0" + str(datetime[5]) if len(str(datetime[5])) == 1 else str(datetime[5])  # 分
    hour = "0" + str(datetime[4]) if len(str(datetime[4])) == 1 else str(datetime[4])  # 时
    
    if TIME[0] != hour[0]:
        print("time0")
        TIME[0] = hour[0]
        lcd.blit(loadPics("res/num/"+hour[0]+".kspic").buf,0,55)
    
    if TIME[1] != hour[1]:
        print("time1")
        TIME[1] = hour[1]
        lcd.blit(loadPics("res/num/"+hour[1]+".kspic").buf,30,55)
        
    if TIME[2] != minute[0]:
        print("time2")
        TIME[2] = minute[0]
        lcd.blit(loadPics("res/num/"+minute[0]+".kspic").buf,70,55)
        
    if TIME[3] != minute[1]:
        print("time3")
        TIME[3] = minute[1]
        lcd.blit(loadPics("res/num/"+minute[1]+".kspic").buf,100,55)
        
#     if TIME[4] != second[0]:
#         TIME[4] = second[0]
#         lcd.blit(loadPics("res/num/"+second[0]+".kspic").buf,30,100)
#         
#     if TIME[5] != second[1]:
#         TIME[5] = second[1]
#         lcd.blit(loadPics("res/num/"+second[1]+".kspic").buf,70,100)
    
    
def weather_display(weather):
    
    if weather == None:
        return
    

    location = weather['location']  # 位置
    temp = weather["temp"]  # 温度
    text = weather["text"]
    icon = weather['icon']
    feelsLike = weather['feelsLike']  # 体感温度
    hum = weather['hum']  # 湿度
    air_grade = weather['air_grade']  # 空气质量指数级别
    air_aqi = weather['air_aqi']  # 空气质量指数
    
    if weather_tick == weather:
        return

    if air_grade == "N/A":
        air_grade = "N"
    else:
        if len(air_grade) != 1:
            air_grade = air_grade[0:2]
    
    
    if len(location) + len(air_grade) > 4:
        if len(location) > 4:
            texts = location[0:4] + "..."
            lcdFont.text(display=lcd,string=texts,x=0,y=0,color=WHITE)
        else:
            x = (80 - len(location)*15) / 2
            lcdFont.text(display=lcd,string=location,x=int(x),y=0,color=WHITE)
    else:
        
        
        if len(air_grade) == 2:
            x = 50
        else:
            x = 65
    
    lcdFont.text(display=lcd,string=location,x=0,y=5,color=WHITE)    
    lcdFont.text(display=lcd,string=air_grade,x=x,y=5,color=lcd.rgb(255,150,0))
    lcdFont.text(display=lcd,string="今天 "+text,x=0,y=25,color=WHITE)
    #print(gc.mem_free(),"weather_display")
    lcd.blit(loadPics("res/weather32/"+str(icon)+".kspic").buf,90,10)
    
    lcdFont.text(display=lcd,string="温度: "+str(temp)+"/"+str(feelsLike),x=0,y=115,color=WHITE)
    lcdFont.text(display=lcd,string="湿度: "+str(hum),x=0,y=135,color=WHITE)
    
#         if len(air_grade) == 2:
#             x = 50
#             if air_grade == "轻度":
#                 color = lcd.rgb(255,140,0)
#             elif air_grade == "中度":
#                 color = lcd.rgb(255,67,54)
#             elif air_grade == "重度":
#                 color = lcd.rgb(103,58,183)
#             else:
#                 color = lcd.rgb(128,0,0)
# 
#         else:
#             print(air_grade)
#             x = 65
#             if air_grade == "优":
#                 print(1)
#                 color = lcd.rgb(76,175,80)
#             elif air_grade == "良":
#                 print(2)
#                 color = lcd.rgb(255,200,7)
#             else:
#                 print(3)
#                 color = lcd.rgb(102,102,102)
                
    
    
second2 = 0

def dh():
    global second2
    if second2 > 17:
        second2 = 0
#     print(second2)
        
#         print(datetime[6]%18)
    if gc.mem_free() < 30000: #内存不足
        gc.collect() #回收内存
    lcd.blit(loadPics("res/dh/"+str(second2)+".kspic").buf,98,110)
    second2 += 1
    lcd.show()


DATE = [13,32,8]
def date_display(datetime):
    global DATE
    if DATE[0] != datetime[1] or DATE[1] != datetime[2] or DATE[2] != datetime[3]+1 :
        DATE[0] = datetime[1]
        DATE[1] = datetime[2]
        DATE[2] = datetime[3] + 1
        
        zhou = ""
        if DATE[2] == 1:
            zhou = "一"
        elif DATE[2] == 2:
            zhou = "二"
        elif DATE[2] == 3:
            zhou = "三"
        elif DATE[2] == 4:
            zhou = "四"
        elif DATE[2] == 5:
            zhou = "五"
        elif DATE[2] == 6:
            zhou = "六"
        elif DATE[2] == 7:
            zhou = "七"
        
        lcdFont.text(display=lcd,string=str(datetime[1])+"月"+str(datetime[2])+"日 周"+zhou,x=0,y=95,color=WHITE)
    
    
#     if DATE[0] != datetime[1]:
#         DATE[0] = datetime[1]
#         
#         if len(str(datetime[1])) == 1:
#             lcdFont.text(display=lcd,string=" "+str(datetime[1]),x=2,y=95,color=WHITE)
#         else:
#             lcdFont.text(display=lcd,string=str(datetime[1]),x=2,y=95,color=WHITE)
#             
#         lcdFont.text(display=lcd,string="月",x=16,y=95,color=WHITE)
#     
#     if DATE[1] != datetime[2]:
#         DATE[1] = datetime[2]
#         
#         if len(str(datetime[2])) == 1:
#             lcdFont.text(display=lcd,string=" "+str(datetime[2]),x=32,y=95,color=WHITE)
#         else:
#             lcdFont.text(display=lcd,string=str(datetime[2]),x=32,y=95,color=WHITE)        
#         lcdFont.text(display=lcd,string="日",x=46,y=95,color=WHITE)
#     
#     lcdFont.text(display=lcd,string=str(datetime[1])+"月"+str(datetime[2])+"日",x=0,y=110,color=WHITE)


def UI_display(weather,datetime):
    global UI_Change
#     if gc.mem_free() < 15000:
#         gc.collect()
        
#     print(gc.mem_free())
    if UI_Change:
        
        UI_Change = False
        
        lcd.fill(BLACK)
        
        weather_display(weather)
    
    datetime_display(datetime)
    
    date_display(datetime)
    
    if datetime[5]%10 == 0 and datetime[6]==0:
        weather_display(weather)
    lcd.show()
    
# a = get_weather()
# print(a)
# weather_display(a)

# lcdFont.text(display=lcd,string="N",x=0,y=20,color=WHITE)
# lcd.blit(loadPics("res/num/8.kspic").buf,0,60)
# lcd.blit(loadPics("res/num/8.kspic").buf,30,60)
# lcd.blit(loadPics("res/num/8.kspic").buf,70,60)
# lcd.blit(loadPics("res/num/8.kspic").buf,100,60)
# # lcd.blit(loadPics("res/num/8.kspic").buf,100,60)
# # lcd.blit(loadPics("res/num-little/0.kspic").buf,117,60)
# lcd.show()
