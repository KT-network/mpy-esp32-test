from ST7735 import TFT
from machine import SPI, Pin
from framebuf import FrameBuffer, RGB565
import time
from math import sqrt
import FileUtil as fu

# 屏幕原始方向尺寸（旋转前）
ScreenSize = (128, 160)
# 旋转后的偏移量
offset = bytearray([0, 24])


def BNColor(r, g, b):
    r = int(r * 31 / 255)
    g = int(g * 63 / 255)
    b = int(b * 31 / 255)
    color = (r << 11) | (g << 5) | (b)
    # 注意调换字节顺序 ST7735像素数据 高字节的在低地址
    high = 0xFF00 & color
    low = 0x00FF & color
    return (low << 8) | (high >> 8)


def BNClamp(aValue, aMin, aMax):
    return max(aMin, min(aMax, aValue))


# 带缓冲的屏幕驱动
class BNST7735Driver:
    def __init__(self, scl, sda, res, dc, cs=0):
        self.bufData = bytearray(ScreenSize[0] * ScreenSize[1] * 2)
        self.buf = FrameBuffer(self.bufData, ScreenSize[1], ScreenSize[0], RGB565)
        self.spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(scl), mosi=Pin(sda), miso=Pin(0))
        self.tft = TFT(self.spi, dc, res, cs, ScreenSize, offset)
        self.tft.initr()
        self.tft.rgb(False)
        self.tft.rotation(1)

    def clear(self, color):
        self.buf.fill(color)

    def drawText(self, msg, color, x, y):
        self.buf.text(msg, x, y, color)

    def drawTextString(self):
        self.buf.text()

    def drawRect(self, x, y, w, h, color, isFill):
        if (not isFill):
            self.buf.rect(x, y, w, h, color)
        else:
            self.buf.fill_rect(x, y, w, h, color)

    def drawLine(self, x1, y1, x2, y2, color):
        self.buf.line(x1, y1, x2, y2, color)

    def drawCircleInner(self, aPos, aRadius, aColor):
        xend = int(0.7071 * aRadius) + 1
        rsq = aRadius * aRadius
        for x in range(xend):
            y = int(sqrt(rsq - x * x))
            xp = aPos[0] + x
            yp = aPos[1] + y
            xn = aPos[0] - x
            yn = aPos[1] - y
            xyp = aPos[0] + y
            yxp = aPos[1] + x
            xyn = aPos[0] - y
            yxn = aPos[1] - x
            self.buf.pixel(xp, yp, aColor)
            self.buf.pixel(xp, yn, aColor)
            self.buf.pixel(xn, yp, aColor)
            self.buf.pixel(xn, yn, aColor)
            self.buf.pixel(xyp, yxp, aColor)
            self.buf.pixel(xyp, yxn, aColor)
            self.buf.pixel(xyn, yxp, aColor)
            self.buf.pixel(xyn, yxn, aColor)

    def fillcircleInner(self, aPos, aRadius, aColor):
        rsq = aRadius * aRadius
        for x in range(aRadius):
            y = int(sqrt(rsq - x * x))
            y0 = aPos[1] - y
            ey = y0 + y * 2
            y0 = BNClamp(y0, 0, ScreenSize[1])
            ln = abs(ey - y0) + 1
            self.buf.vline(aPos[0] + x, y0, ln, aColor)
            self.buf.vline(aPos[0] - x, y0, ln, aColor)

    def drawCircle(self, x, y, r, color, isFill):
        if (not isFill):
            self.drawCircleInner((x, y), r, color)
        else:
            self.fillcircleInner((x, y), r, color)

    def drawPic(self, x, y, tex):
        if (tex.hasTM):
            self.buf.blit(tex.buf, x, y, tex.maskColor)
        else:
            self.buf.blit(tex.buf, x, y)

    def drawString(self, msg, x, y):
        for i in range(len(msg)):
            self.drawPic(x + i * 16, y, msg[i])

    def show(self):
        self.tft._setwindowloc((0, 0), (ScreenSize[1] - 1, ScreenSize[0] - 1))
        self.tft._writedata(self.bufData)
