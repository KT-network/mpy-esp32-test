import os
from Texture import Texture


# 将四个字节组装为整数的方法
def readInt(bytesArray, start):
    result = bytesArray[start] + (bytesArray[start + 1] << 8) + (bytesArray[start + 2] << 16) + (
                bytesArray[start + 3] << 24)
    return result


# 将一幅文字图的bit数据转换为Texture
def fromBitDataToTexture(width, height, pdata, fColor, bgColor):
    # 文字颜色字节拆出
    fColorH = (fColor & 0xFF00) >> 8
    fColorL = (fColor & 0x00FF)
    bgColorH = (bgColor & 0xFF00) >> 8
    bgColorL = (bgColor & 0x00FF)

    # 结果像素数据
    imgData = bytearray(width * height * 2)
    # 当前字节
    currByte = pdata[0]
    # 当前字节计数器
    byteCount = 0
    # 当前比特计数器
    bitCount = 0
    # 当前比特掩码
    bitMask = 0b10000000
    # 遍历每一行
    for i in range(height):
        # 此行当前像素位置
        currX = 0
        # 遍历每一列
        for j in range(width):
            # 计算当前像素值
            color = (currByte & bitMask) >> (7 - bitCount)
            tempIndex = i * width + j
            if (color == 0):
                imgData[tempIndex * 2] = fColorL
                imgData[tempIndex * 2 + 1] = fColorH
            else:
                imgData[tempIndex * 2] = bgColorL
                imgData[tempIndex * 2 + 1] = bgColorH
            # X坐标右移一格
            currX = currX + 1
            # 比特掩码右移1位
            bitMask = bitMask >> 1
            # 比特计数器加1
            bitCount = bitCount + 1
            # 如果比特计数器等于7且还有下一个字节，则换字节
            if bitCount == 8 and byteCount < len(pdata) - 1:
                bitCount = 0
                byteCount = byteCount + 1
                currByte = pdata[byteCount]
                bitMask = 0b10000000
    return Texture(width, height, imgData, bgColor)


# 加载指定编号文字对应二值图的方法
def getSpecCharBNBinPic(fname, code, fColor, bgColor):
    # 读取文件字节数据
    dataFile = open(fname, "rb")
    # 图像计数器
    pCount = 0
    # 字节计数器
    bcount = 0
    # 首先读出四个字节组装为图集中图的数量
    buf4 = dataFile.read(4)
    count = readInt(buf4, 0)
    bcount = bcount + 4
    # 遍历图集中的每一幅图
    for i in range(int(count)):
        # 读取当前图片的宽度、高度
        dataFile.seek(int(bcount))
        buf4 = dataFile.read(4)
        w = readInt(buf4, 0)
        bcount = bcount + 4
        dataFile.seek(int(bcount))
        buf4 = dataFile.read(4)
        h = readInt(buf4, 0)
        bcount = bcount + 4
        if pCount == code:
            # 提取此图片像素数据字节序列
            dataFile.seek(int(bcount))
            bufPD = dataFile.read(int(w * h / 8))
            return fromBitDataToTexture(w, h, bufPD, fColor, bgColor)
        bcount = bcount + w * h / 8
        pCount = pCount + 1


# 加载句子中各个字图列表的方法
def getSentence(fname, codes, fColor, bgColor):
    result = []
    for code in codes:
        result.append(getSpecCharBNBinPic(fname, code, fColor, bgColor))
    return result


# ==============================================================================
# 将两个个字节组装为RGB565的方法
def readRGB565(bytesArray, start):
    result = bytesArray[start] + (bytesArray[start + 1] << 8)
    return result


def loadPics(fname):
    # 结果列表
    pics = []
    # 读取文件字节数据
    dataFile = open(fname, "rb")
    # 读取文件中的所有数据字节
    bytesData = dataFile.read()
    # 字节计数器
    bcount = 0
    # 首先读出四个字节组装为图集中图的数量
    count = readInt(bytesData, bcount)
    bcount = bcount + 4
    # 遍历图集中的每一幅图
    for i in range(int(count)):
        # 读取当前图片的宽度、高度
        w = readInt(bytesData, int(bcount))
        bcount = bcount + 4
        h = readInt(bytesData, int(bcount))
        bcount = bcount + 4
        # 读取是否透明
        isTM = bytesData[bcount]
        bcount = bcount + 1
        # 读取透明色
        TMColor = readRGB565(bytesData, int(bcount))
        bcount = bcount + 2
        # 提取此图片像素数据字节序列
        dataCurr = bytesData[int(bcount):int(bcount + w * h * 2)]
        bcount = bcount + w * h * 2
        if (isTM == 1):
            pics.append(Texture(w, h, dataCurr, TMColor))
        else:
            pics.append(Texture(w, h, dataCurr))
    return pics
