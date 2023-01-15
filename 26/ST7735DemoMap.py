from BNST7735Driver import BNST7735Driver,BNColor,ScreenSize
from MoveBall import MoveBall
from Texture import Texture
import FileUtil as fu
import time

#创建屏幕驱动对象
bnsd=BNST7735Driver(4,13,32,2)

#加载游戏图集
pics=fu.loadPics("base.bnbapic")
#东周末年 文字图列表
msg1=fu.getSentence("ST7735.bnbapic",[7,4,6,1],BNColor(8,8,2),BNColor(0,0,0))
#列国纷争 文字图列表 
msg2=fu.getSentence("ST7735.bnbapic",[2,9,3,5],BNColor(133,81,6),BNColor(0,0,0))

#获取当前毫秒数(辅助FPS计算)
ts=time.ticks_ms()
#每多少帧计算一次
MAX_FRAME=500
#计数器(辅助FPS计算)
FPSCount=0
#FPS信息字符串
FPSStr="FPS:N/A"

#地图数据
gameMap=[
         [3,0,5,4,2],
         [0,1,1,1,1],
         [0,0,0,0,0]
        ]

#不断循环执行绘制
while True:
    #根据地图数据绘制每一个图块
    for i in range(len(gameMap)):
        for j in range(len(gameMap[0])):
            bnsd.drawPic(32*j,32*i,pics[gameMap[i][j]]) 
    #绘制地图上面包含透明部分的铁匠铺建筑
    bnsd.drawPic(0,0,pics[6])
    #绘制文字边框
    bnsd.drawPic(90,40,pics[7])
    #绘制右下角的中文“东周末年 列国纷争”        
    bnsd.drawString(msg1,94,43)
    bnsd.drawString(msg2,94,60)
    #执行显示
    bnsd.show()
    
    #更新FPS计数器
    FPSCount=FPSCount+1
    #若到达了100帧
    if(FPSCount==MAX_FRAME):
        #计数器归0
        FPSCount=0
        #计算时间跨度(ms)
        timeSpan=time.ticks_ms()-ts
        #更新当前毫秒数
        ts=time.ticks_ms()
        #打印FPS数据
        FPSStr="FPS:"+str(round(1000*MAX_FRAME/timeSpan,2))
        print(FPSStr)