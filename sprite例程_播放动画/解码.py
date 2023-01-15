# 1.把NiceAni上传
# 2.运行本程序解码（一次解码后续都可以用）
from sprite import bmpdecode
for i in range(21):
    p = bmpdecode('NiceAni/nice'+str(i+1)+'.bmp',limit=210,InvertColor=True)
