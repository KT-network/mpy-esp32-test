from time import sleep_ms
import struct
import framebuf
from micropython import const


class LCDDRIVE():
    # -----------------------------------实现FrameBuffer类方法----------------------------------------#
    # 这些方法之前必须要先获取buffer在他们是buffer上操作的，即把屏幕的一块单独拿出来操作#
    def pixel(self, x, y, c=0xffff):
        w, h = self.limit(x, y, 1, 1)  # 高宽限制
        self.getbuffer(x, y, 1, 1)
        self.fb.pixel(0, 0, c)
        self.show()

    def fill(self, x, y, w, h, c=0xffff):
        w, h = self.limit(x, y, w, h)  # 高宽限制
        self.getbuffer(x, y, w, h)
        self.fb.fill_rect(0, 0, w, h, c)
        self.show()

    def rect(self, x, y, w, h, c=0xffff):
        w, h = self.limit(x, y, w, h)  # 高宽限制
        self.getbuffer(x, y, w, h)
        self.fb.rect(0, 0, w, h, c)
        self.show()

    def line(self, x, y, w, h, c=0xffff):
        w, h = self.limit(x, y, w, h)  # 高宽限制
        self.getbuffer(x, y, w, h)
        self.fb.line(0, 0, w, h, c)
        self.show()

    def hline(self, x, y, w, c=0xffff):
        w = w
        h = 1
        width, height = self.limit(x, y, w, h)  # 高宽限制
        self.getbuffer(x, y, width, height)
        self.fb.hline(0, 0, width, c)
        self.show()

    def vline(self, x, y, h, c=0xffff):
        w = 1
        h = h
        w, h = self.limit(x, y, w, h)  # 高宽限制
        self.getbuffer(x, y, w, h)
        self.fb.vline(0, 0, h, c)
        self.show()

    def text(self, str, x, y, fc=0xffff, bc=0x0000, size=8):
        w = size * len(str)
        h = size

        m = (self.width - x) // size
        for i in range(len(str) // m + 1):
            w, h = self.limit(x, y, w, h)  # 高宽限制
            self.getbuffer(x, y, w, h)
            self.fb.fill_rect(x, y, w, h, bc)  # 背景色
            self.fb.text(str[i * m:(i + 1) * m], 0, 0)
            y = y + size
            self.show()

    def limit(self, x, y, w, h):
        xmax = x + w
        ymax = y + h
        if xmax >= self.width:
            xmax = self.width
        if ymax >= self.height:
            ymax = self.height
        return xmax - x, ymax - y

    # ---------------------------------------------------------------------------------------------#

    def printf(self, str, x0, y0, font_path="/sd/font/utf16_hb.lzk", size=(16, 16), alignment=True):
        charbytes = int(size[0] * size[1] * 2)  # 一个字符的所占的字节数，是跳转字库指针的最小单位
        n = 0
        pos_y = y0
        with open(font_path, 'rb') as f:  # 打开字库
            for c in str:  # 分割字符串为字符
                pos_x = x0 + size[0] * n  # y的位置为起始值加上n个字符size
                self.writeblock(pos_x, pos_y, pos_x + size[0] - 1, pos_y + size[1] - 1)
                # self.getbuffer(pos_x,pos_y,size[0],size[1])#每次显示一行字符
                f.seek(ord(c) * charbytes)  # 跳转到字符c的位置
                self.data(f.read(charbytes))  # 读取字符c,返回此字符对应的点阵数据
                # self.buf = f.read(charbytes)
                # self.show()#显示一个字符
                n = n + 1
                if pos_x >= self.width - 1 * size[0]:  # 如果当前位置超出屏幕
                    pos_y = pos_y + size[1]  # 向下偏移一个size<换行>
                    if alignment == False:
                        x0 = 0
                    n = 0
                    if pos_y > self.height - 1 * size[1]:
                        break

    # ---------------------------------------------------------------------------------------------#
    def bitmap(self, x, y, pic_w, pic_h, file_name, lines=100):
        lines = 240
        block = pic_w * lines * 2
        nums = (pic_w * pic_h * 2) // block
        with open(file_name, 'rb') as fio:
            for v in range(nums + 1):
                self.writeblock(x, y + v * lines, x + pic_w - 1, y + v * lines + lines - 1)
                self.data(fio.read(block))

    # ----------------------------------------其它方法-----------------------------------------------#

    def show(self):
        self.data(self.buf)

    def erase(self, c):
        height = int(self.height / 20) + 1
        width = self.width
        for x in range(height):
            self.fill(0, 20 * x, width, 20, c)

    def getbuffer(self, x, y, w, h):
        self.writeblock(x, y, x + w - 1, y + h - 1)
        self.buf = bytearray(w * h * 2)
        self.fb = framebuf.FrameBuffer(self.buf, w, h, framebuf.RGB565)


# ---------------------------------------------------------------------------------------------#


class ST7735(LCDDRIVE):
    # command definitions
    ST7735_NOP = const(0x00)  # No Operation
    ST7735_SWRESET = const(0x01)  # Software reset
    ST7735_RDDID = const(0x04)  # Read Display ID
    ST7735_RDDST = const(0x09)  # Read Display Status
    ST7735_SLPIN = const(0x10)  # Sleep in & booster off
    ST7735_SLPOUT = const(0x11)  # Sleep out & booster on
    ST7735_PTLON = const(0x12)  # Partial mode on
    ST7735_NORON = const(0x13)  # Partial off (Normal)
    ST7735_INVOFF = const(0x20)  # Display inversion off
    ST7735_INVON = const(0x21)  # Display inversion on
    ST7735_DISPOFF = const(0x28)  # Display off
    ST7735_DISPON = const(0x29)  # Display on
    ST7735_CASET = const(0x2A)  # Column address set
    ST7735_RASET = const(0x2B)  # Row address set
    ST7735_RAMWR = const(0x2C)  # Memory write
    ST7735_RAMRD = const(0x2E)  # Memory read
    ST7735_PTLAR = const(0x30)  # Partial start/end address set
    ST7735_COLMOD = const(0x3A)  # Interface pixel format
    ST7735_MADCTL = const(0x36)  # Memory data access control
    ST7735_FRMCTR1 = const(0xB1)  # In normal mode (Full colors)
    ST7735_FRMCTR2 = const(0xB2)  # In Idle mode (8-colors)
    ST7735_FRMCTR3 = const(0xB3)  # In partial mode + Full colors
    ST7735_INVCTR = const(0xB4)  # Display inversion control
    ST7735_PWCTR1 = const(0xC0)  # Power control settings
    ST7735_PWCTR2 = const(0xC1)  # Power control settings
    ST7735_PWCTR3 = const(0xC2)  # In normal mode (Full colors)
    ST7735_PWCTR4 = const(0xC3)  # In Idle mode (8-colors)
    ST7735_PWCTR5 = const(0xC4)  # In partial mode + Full colors
    ST7735_VMCTR1 = const(0xC5)  # VCOM control
    ST7735_GMCTRP1 = const(0xE0)
    ST7735_GMCTRN1 = const(0xE1)

    # ------------------------------------------初始化方法--------------------------------------------#
    def __init__(self, spi, cs, dc, rst, r=0, type='1.8'):
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.spi = spi
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=1)
        self.rst.init(self.rst.OUT, value=1)
        self.r = r
        if type == '0.96':
            # r = 0为正常方向
            self.w_offset = 0x01
            self.h_offset = 0x1a
            self.w = 160
            self.h = 80
        elif type == '1.8':
            # r = 1为正常方向
            self.w_offset = 0x00
            self.h_offset = 0x00
            self.w = 160
            self.h = 128
        self.init()

    def reset(self):
        self.rst.on()
        sleep_ms(5)
        self.rst.off()
        sleep_ms(20)
        self.rst.on()
        sleep_ms(150)

    def rotation(self, r):
        if r == 0:
            self.command(self.ST7735_MADCTL)
            self.data(b'\xc0')
            self.width = self.h
            self.height = self.w
            self.width_offset = self.h_offset
            self.height_offset = self.w_offset
        elif r == 1:
            self.command(self.ST7735_MADCTL)
            self.data(b'\xa0')
            self.width = self.w
            self.height = self.h
            self.width_offset = self.w_offset
            self.height_offset = self.h_offset
        elif r == 2:
            self.command(self.ST7735_MADCTL)
            self.data(b'\x00')
            self.width = self.h
            self.height = self.w
            self.width_offset = self.h_offset
            self.height_offset = self.w_offset
        elif r == 3:
            self.command(self.ST7735_MADCTL)
            self.data(b'\x60')
            self.width = self.w
            self.height = self.h
            self.width_offset = self.w_offset
            self.height_offset = self.h_offset

    def init(self):
        self.reset()
        self.rotation(self.r)
        for cmd, data, delay in [
            (self.ST7735_SWRESET, None, 150),
            (self.ST7735_SLPOUT, None, 500),
            (self.ST7735_FRMCTR1, b'\x01\x2c\x2d', None),
            (self.ST7735_FRMCTR2, b'\x01\x2c\x2d', None),
            (self.ST7735_FRMCTR3, b'\x01\x2c\x2d\x01\x2c\x2d', None),
            (self.ST7735_INVCTR, b'\x07', None),
            (self.ST7735_PWCTR1, b'\xa2\x02\x84', None),
            (self.ST7735_PWCTR2, b'\xc5', None),
            (self.ST7735_PWCTR3, b'\x0a\x00', None),
            (self.ST7735_PWCTR4, b'\x8a\x2a', None),
            (self.ST7735_PWCTR5, b'\x8a\xee', None),
            (self.ST7735_VMCTR1, b'\x0e', None),
            (self.ST7735_COLMOD, b'\x05', None),
            (self.ST7735_GMCTRP1, b'\x02\x1c\x07\x12\x37\x32\x29\x2d\x29\x25\x2b\x39\x00\x01\x03\x10', None),
            (self.ST7735_GMCTRN1, b'\x03\x1d\x07\x06\x2e\x2c\x29\x2d\x2e\x2e\x37\x3f\x00\x00\x02\x10', None),
            (self.ST7735_NORON, None, 10),
            (self.ST7735_DISPON, None, 100), ]:
            self.command(cmd)
            if data:
                self.data(data)
            if delay:
                sleep_ms(delay)

        self.erase(0xffff)

    def writeblock(self, x0, y0, x1, y1):
        x0 = x0 + self.width_offset
        x1 = x1 + self.width_offset
        y0 = y0 + self.height_offset
        y1 = y1 + self.height_offset
        self.command(self.ST7735_CASET)  # 列地址设置
        self.data(struct.pack(">HH", x0, x1))
        self.command(self.ST7735_RASET)  # 页地址设置
        self.data(struct.pack(">HH", y0, y1))
        self.command(self.ST7735_RAMWR)  # 内存写入

    def command(self, cmd):
        self.dc.off()
        self.cs.off()
        self.spi.write(bytes([cmd]))
        self.cs.on()

    def data(self, buf):
        self.dc.on()
        self.cs.off()
        self.spi.write(buf)
        self.cs.on()

    # ------------------------------------------------------------------------------------------------#

    # ----------------------------------------其它方法-------------------------------------------------#
    # 0 关 1 开
    def swith(self, mode):
        if mode == 0:
            self.command(self.ST7735_SLPIN)
        else:
            self.command(self.ST7735_SLPOUT)

    def inversion(self, mode):
        if mode == 0:
            self.command(self.ST7735_INVON)
        else:
            self.command(self.ST7735_INVOFF)


# ----------------------------------------------------------------------------------------------#

class ILI9341(LCDDRIVE):
    PWRONCTRL = const(0xed)
    VSCRSADD = const(0x37)
    PGAMCTRL = const(0xe0)
    NGAMCTRL = const(0xe1)
    DISPOFF = const(0x28)
    PWCTRLA = const(0xcb)
    PWCRTLB = const(0xcf)
    DTCTRLA = const(0xe8)
    DTCTRLB = const(0xea)
    PWCTRL1 = const(0xc0)
    PWCTRL2 = const(0xc1)
    VMCTRL1 = const(0xc5)
    VMCTRL2 = const(0xc7)
    FRMCTR1 = const(0xb1)
    DISCTRL = const(0xb6)
    RDDSDR = const(0x0f)
    SLPOUT = const(0x11)
    SLPIN = const(0x10)
    INVOFF = const(0x20)
    INVON = const(0x21)
    GAMSET = const(0x26)
    DISPON = const(0x29)
    MADCTL = const(0x36)
    PIXSET = const(0x3a)
    PRCTRL = const(0xf7)
    CASET = const(0x2a)
    PASET = const(0x2b)
    RAMWR = const(0x2c)
    RAMRD = const(0x2e)
    ENA3G = const(0xf2)

    # --------------------------------初始化即底层代码-----------------------------------------------#

    def __init__(self, spi, cs, dc, rst, r=0, type='3.5'):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        if type == '3.5':
            self.w = 240
            self.h = 320
            self.w_offset = 0x00
            self.h_offset = 0x00
        self.r = r
        self.init()

    def reset(self):
        self.rst(0)
        sleep_ms(50)
        self.rst(1)
        sleep_ms(50)

    def rotation(self, r):
        if r == 0:  # 0 deg
            self.command(self.MADCTL)
            self.data(b"\x48")
            self.width = self.w
            self.height = self.h
            self.width_offset = self.w_offset
            self.height_offset = self.h_offset
        elif r == 1:  # 90 deg
            self.command(self.MADCTL)
            self.data(b"\x28")
            self.width = self.h
            self.height = self.w
            self.width_offset = self.h_offset
            self.height_offset = self.w_offset
        elif r == 2:  # 180 deg
            self.command(self.MADCTL)
            self.data(b"\x88")
            self.width = self.w
            self.height = self.h
            self.width_offset = self.w_offset
            self.height_offset = self.h_offset
        elif r == 3:  # 270 deg
            self.command(self.MADCTL)
            self.data(b"\xE8")
            self.width = self.h
            self.height = self.w
            self.width_offset = self.h_offset
            self.height_offset = self.w_offset
        else:
            pass

    def init(self):
        self.reset()
        self.rotation(self.r)
        for command, data in (
                (self.RDDSDR, b"\x03\x80\x02"),
                (self.PWCRTLB, b"\x00\xc1\x30"),
                (self.PWRONCTRL, b"\x64\x03\x12\x81"),
                (self.DTCTRLA, b"\x85\x00\x78"),
                (self.PWCTRLA, b"\x39\x2c\x00\x34\x02"),
                (self.PRCTRL, b"\x20"),
                (self.DTCTRLB, b"\x00\x00"),
                (self.PWCTRL1, b"\x23"),
                (self.PWCTRL2, b"\x10"),
                (self.VMCTRL1, b"\x3e\x28"),
                (self.VMCTRL2, b"\x86")):
            self.command(command)
            self.data(data)
        for command, data in (
                (self.PIXSET, b"\x55"),
                (self.FRMCTR1, b"\x00\x18"),
                (self.DISCTRL, b"\x08\x82\x27"),
                (self.ENA3G, b"\x00"),
                (self.GAMSET, b"\x01"),
                (self.PGAMCTRL, b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00"),
                (self.NGAMCTRL, b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f")):
            self.command(command)
            self.data(data)
        self.command(self.SLPOUT)
        sleep_ms(120)
        self.command(self.DISPON)
        self.erase(0xffff)

    def command(self, command):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytes([command]))
        self.cs(1)

    def data(self, data):
        self.cs(0)
        self.dc(1)
        self.spi.write(data)
        self.cs(1)

    # 写入块
    def writeblock(self, x0, y0, x1, y1):
        self.command(self.CASET)  # 列地址设置
        self.data(struct.pack(">HH", x0, x1))
        self.command(self.PASET)  # 页地址设置
        self.data(struct.pack(">HH", y0, y1))
        self.command(self.RAMWR)  # 内存写入

    # 读取块，返回
    def readblock(self, x0, y0, x1, y1):
        self.command(self.CASET)  # 列地址设置
        self.data(struct.pack(">HH", x0, x1))
        self.command(self.PASET)  # 页地址设置
        self.data(struct.pack(">HH", y0, y1))
        self.command(self.RAMRD)  # 内存读出
        data = self.spi.read((x1 - x0 + 1) * (y1 - y0 + 1) * 3)
        return data

    # ---------------------------------------------------------------------------------------------#

    # ----------------------------------------其它方法-------------------------------------------------#
    # 0 关 1 开
    def swith(self, mode):
        if mode == 0:
            self.command(self.SLPIN)
        else:
            self.command(self.SLPOUT)

    def inversion(self, mode):
        if mode == 0:
            self.command(self.INVON)
        else:
            self.command(self.INVOFF)


# ---------------------------------------------------------------------------------------------#


class ST7789(LCDDRIVE):
    # commands
    ST7789_NOP = const(0x00)
    ST7789_SWRESET = const(0x01)
    ST7789_RDDID = const(0x04)
    ST7789_RDDST = const(0x09)
    ST7789_SLPIN = const(0x10)
    ST7789_SLPOUT = const(0x11)
    ST7789_PTLON = const(0x12)
    ST7789_NORON = const(0x13)
    ST7789_INVOFF = const(0x20)
    ST7789_INVON = const(0x21)
    ST7789_DISPOFF = const(0x28)
    ST7789_DISPON = const(0x29)
    ST7789_CASET = const(0x2A)
    ST7789_RASET = const(0x2B)
    ST7789_RAMWR = const(0x2C)
    ST7789_RAMRD = const(0x2E)
    ST7789_PTLAR = const(0x30)
    ST7789_COLMOD = const(0x3A)
    ST7789_MADCTL = const(0x36)

    def __init__(self, spi, cs, dc, rst, r=0, type='1.3'):
        self.spi = spi
        self.rst = rst
        self.dc = dc
        self.cs = cs
        if self.cs != None: self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=1)
        self.rst.init(self.rst.OUT, value=1)
        self.r = r
        if type == '1.3':
            # r = 0为正常方向
            self.w_offset = 0x00
            self.h_offset = 0x00
            self.w = 240
            self.h = 240
        else:
            pass
        self.init()

    def rotation(self, r):
        if r == 0:
            self.command(self.ST7789_MADCTL)
            self.data(b'\x00')
            self.width = self.w
            self.height = self.h
            self.width_offset = self.w_offset
            self.height_offset = self.h_offset
        elif r == 1:
            self.command(self.ST7789_MADCTL)
            self.data(b'\x60')
            self.width = self.h
            self.height = self.w
            self.width_offset = self.h_offset
            self.height_offset = self.w_offset
        elif r == 2:
            self.command(self.ST7789_MADCTL)
            self.data(b'\x10')
            self.width = self.w
            self.height = self.h
            self.width_offset = self.w_offset
            self.height_offset = self.h_offset
        elif r == 3:
            self.command(self.ST7789_MADCTL)
            self.data(b'\x70')
            self.width = self.h
            self.height = self.w
            self.width_offset = self.h_offset
            self.height_offset = self.w_offset
        else:
            pass

    def init(self):
        self.reset()

        self.rotation(self.r)
        for cmd, data, delay in [
            (self.ST7789_SWRESET, None, 150),
            (self.ST7789_SLPOUT, None, None),
            (self.ST7789_COLMOD, b'\x05', 50),
            (self.ST7789_NOP, None, 10),
            (self.ST7789_DISPON, None, 500),
            (self.ST7789_INVON, None, None),
        ]:
            self.command(cmd)
            if data:
                self.data(data)
            if delay:
                sleep_ms(delay)
        self.erase(0xffff)

    def command(self, command):
        if self.cs != None: self.cs.off()
        self.dc.off()
        self.spi.write(bytes([command]))
        if self.cs != None: self.cs.on()

    def data(self, data):
        if self.cs != None: self.cs.off()
        self.dc.on()
        self.spi.write(data)
        if self.cs != None: self.cs.on()

    def reset(self):
        if self.cs != None: self.cs.off()
        self.rst.on()
        sleep_ms(50)
        self.rst.off()
        sleep_ms(50)
        self.rst.on()
        sleep_ms(150)
        if self.cs != None: self.cs.on()

    def writeblock(self, x0, y0, x1, y1):
        x0 = x0 + self.width_offset
        x1 = x1 + self.width_offset
        y0 = y0 + self.height_offset
        y1 = y1 + self.height_offset
        self.command(self.ST7789_CASET)  # 列地址设置
        self.data(struct.pack(">HH", x0, x1))
        self.command(self.ST7789_RASET)  # 页地址设置
        self.data(struct.pack(">HH", y0, y1))
        self.command(self.ST7789_RAMWR)  # 内存写入

    # 0 关 1 开
    def swith(self, mode):
        if mode == 0:
            self.command(self.ST7789_SLPIN)
        else:
            self.command(self.ST7789_SLPOUT)

    def inversion(self, mode):
        if mode == 0:
            self.command(self.ST7789_INVON)
        else:
            self.command(self.ST7789_INVOFF)
