from framebuf import FrameBuffer, RGB565


# 纹理贴图类
# 所有像素全部不透明的使用缓冲拷贝，快速贴图
class Texture:
    def __init__(self, w, h, data, maskColor=None):
        self.w = w
        self.h = h
        self.hasTM = not (maskColor is None)
        if self.hasTM:
            self.maskColor = maskColor
        self.buf = FrameBuffer(bytearray(data), w, h, RGB565)
