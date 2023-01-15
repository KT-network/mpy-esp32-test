from BNST7735Driver import BNST7735Driver, BNColor, ScreenSize
from MoveBall import MoveBall
from Texture import Texture
import FileUtil as fu
import time

# 创建屏幕驱动对象
bnsd = BNST7735Driver(4, 13, 32, 2)

# 加载图集
pics = fu.loadPics("simple.bnbapic")
# 创建Logo小球移动计算辅助类对象
mb = MoveBall(20, 20, 28, ScreenSize[1], ScreenSize[0])
# 东周末年 文字图列表
msg1 = fu.getSentence("ST7735.bnbapic", [7, 4, 6, 1], BNColor(157, 250, 128), BNColor(0, 0, 0))
# 列国纷争 文字图列表
msg2 = fu.getSentence("ST7735.bnbapic", [2, 9, 3, 5], BNColor(249, 210, 127), BNColor(0, 0, 0))

# 获取当前毫秒数(辅助FPS计算)
ts = time.ticks_ms()
# 每多少帧计算一次
MAX_FRAME = 500
# 计数器(辅助FPS计算)
FPSCount = 0
# FPS信息字符串
FPSStr = "FPS:N/A"

# 不断循环执行绘制及计算
while True:
    # 用黑色清屏
    bnsd.clear(BNColor(0, 0, 0));
    # 绘制一行文字(仅限英文)
    bnsd.drawText("ESP32!", BNColor(255, 255, 255), 20, 50)
    # 绘制红绿蓝边框矩形
    bnsd.drawRect(2, 2, 156, 76, BNColor(255, 0, 0), False)
    bnsd.drawRect(5, 5, 150, 70, BNColor(0, 255, 0), False)
    bnsd.drawRect(8, 8, 144, 64, BNColor(0, 0, 255), False)
    # 绘制画面右上部分的矩形、填充圆形、非填充圆形
    bnsd.drawRect(100, 24, 20, 14, BNColor(240, 182, 69), True)
    bnsd.drawCircle(83, 23, 10, BNColor(0, 0, 255), True)
    bnsd.drawCircle(96, 31, 16, BNColor(255, 0, 0), False)
    bnsd.drawCircle(96, 31, 15, BNColor(255, 0, 0), False)
    # 绘制右下角的小鸟图(不含透明部分)
    bnsd.drawPic(115, 42, pics[0])
    # 绘制左上角的中文“东周末年 列国纷争”
    bnsd.drawString(msg1, 10, 11)
    bnsd.drawString(msg2, 10, 28)
    # 计算Logo小球的新位置
    mb.nextStep()
    # 绘制Logo小球
    bnsd.drawPic(mb.cx, mb.cy, pics[1])
    # 绘制左下位置的FPS信息
    bnsd.drawText(FPSStr, BNColor(255, 255, 255), 20, 60)
    # 执行显示
    bnsd.show()

    # 更新FPS计数器
    FPSCount = FPSCount + 1
    # 若到达了100帧
    if (FPSCount == MAX_FRAME):
        # 计数器归0
        FPSCount = 0
        # 计算时间跨度(ms)
        timeSpan = time.ticks_ms() - ts
        # 更新当前毫秒数
        ts = time.ticks_ms()
        # 打印FPS数据
        FPSStr = "FPS:" + str(round(1000 * MAX_FRAME / timeSpan, 2))
