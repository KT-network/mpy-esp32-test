def getbin(inta: int, x: int) -> int:
    return (inta & (1 << x)) >> x


def rgb565(bgr):
    return (bgr[0] & 0xf8 | (bgr[1] & 0xfc) >> 5), ((bgr[1] & 0x1C) << 3 | bgr[2] >> 3)


def chsC2enc(d):
    if 0x4e00 <= d <= 0x9fa5 or d < 128:
        return d
    if (d == 0xff0c):
        return 0x2c
    elif (d == 0x3002):
        return 0x2e
    elif (d == 0xff1a):
        return 0x3b
    elif (d == 0x201c or d == 0x201d):
        return 0x22
    elif (d == 0x2019 or d == 0x2018):
        return 0x27
    elif (d == 0x3010):
        return 0x5b
    elif (d == 0x3011):
        return 0x5d
    elif (d == 0xff08):
        return 0x28
    elif (d == 0xff09):
        return 0x29
    elif (d == 0xff1b):
        return 0x3b
    elif (d == 0x3001):
        return 0xb7
    elif (d == 0xff01):
        return 0x21
    print(d, chr(d))


class Font16:
    def __init__(self, filename) -> None:
        self.bias = 0x4e00
        self.h = 16
        self.w = 16
        # self.end = 0x9fa5
        self.f = open(filename, 'rb')
        if (self.f.read(3) != b'f16'):
            raise TypeError("!!!Font not support!!!")

    def text(self, x, y, data, display, width=2, color=[255, 255, 255], backgroundcolor=[0, 0, 0], linecount=10):
        color = bytearray(rgb565(color))
        backgroundcolor = bytearray(rgb565(backgroundcolor))
        i = 0  # 换字
        p = y  # 换行
        for d in data:
            d = ord(d)
            d = chsC2enc(d)
            if 0 < d < 128:
                self.f.seek((d) * 32 + 3)
            elif d >= 0x4e00:
                self.f.seek((d - self.bias + 128) * 32 + 3)
            fromD = x + p * 25 + i * width

            display._setwindowloc((x + i * self.w, p), (x + i * self.w + self.w - 1, p + self.h - 1))
            for charData in range(16):
                temp = self.f.read(1)[0]
                index = 7
                while index >= 0:
                    if (getbin(temp, index)):
                        display._writedata(color)
                    else:
                        display._writedata(backgroundcolor)
                    index = index - 1
                temp = self.f.read(1)[0]
                index = 7
                while index >= 0:
                    if (getbin(temp, index)):
                        display._writedata(color)
                    else:
                        display._writedata(backgroundcolor)
                    index = index - 1
            i = i + 1
            if i >= linecount:
                # print(i)
                p += 16
                i = 0

    def __del__(self):
        self.data.close()
