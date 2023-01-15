from st7735 import TFTColor
import time
def bmpDecoder(filename,display,drawPos = [0,0]):
    f=open(filename, 'rb')
    if f.read(2) == b'BM':  #header
        dummy = f.read(8) #file size(4), creator bytes(4)
        offset = int.from_bytes(f.read(4), 'little')
        hdrsize = int.from_bytes(f.read(4), 'little')
        width = int.from_bytes(f.read(4), 'little')
        height = int.from_bytes(f.read(4), 'little')
        if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
            depth = int.from_bytes(f.read(2), 'little')
            if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
                #print("Image size:", width, "x", height)
                rowsize = (width * 3 + 3) & ~3
                if height < 0:
                    height = -height
                    flip = False
                else:
                    flip = True
                w, h = width, height
                if w > display._size[0]: w = display._size[0]
                if h > display._size[1]: h = display._size[1]
                if(drawPos[0]+width > display._size[0]):drawPos[0] = display._size[0] -width
                if(drawPos[1]+height > display._size[1]):drawPos[1] = display._size[1] -height
                #print(drawPos)
                display._setwindowloc(drawPos,(drawPos[0]+w - 1,drawPos[1]+h - 1))
                row = 0
                while row < h:
                    buff = bytearray()
                    if flip:
                        pos = offset + (height - 1 - row) * rowsize
                    else:
                        pos = offset + row * rowsize
                    if f.tell() != pos:
                        dummy = f.seek(pos)
                    col = 0
                    while col < w:
                        bgr = f.read(3)
                        temp = TFTColor(bgr[2],bgr[1],bgr[0])
                        buff.append(temp>>8)
                        buff.append(temp)
                        #display._pushcolor(TFTColor(bgr[2],bgr[1],bgr[0]))
                        col += 1
                    display._writedata(buff)
                    row += 1
