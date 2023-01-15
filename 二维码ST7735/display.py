from uQR import QRCode
from machine import Pin, SPI
from st7735 import ST7735
spi=SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))
lcd= ST7735 (70, 60, spi,dc=Pin(21),cs=Pin(16),rst=Pin(22),rot=4,bgr=2)






def DISPLAY():
       

       qr = QRCode(border=2)
       qr.add_data("192.168.248.2")  # 这里是要生成的二维码，被扫码之后的得到的内容
       matrix = qr.get_matrix()

       row_len = len(matrix)
       col_len = len(matrix[0])
# 放大倍数
# 默认情况下输出的二维码太小，可以按照你实际屏幕的大小进行缩放，当前我的240x240屏幕缩放8倍正合适
       scale_rate = 2

       for row in range(row_len * scale_rate):
            for col in range(col_len * scale_rate):
                if matrix[row//scale_rate][col//scale_rate]:
                    lcd.pixel(row, col, ST7735.rgb(0,255, 255, 255))
                else:
                    lcd.pixel(row, col, ST7735.rgb(0,0, 0, 0))
                col += 1
            row += 1
            lcd.show() # 显示出来 
