#小球斜45°四向反弹
#    3     0
#     \ | /
#     -----
#     / | \
#    2     1

#移动的小球
class MoveBall:
    def __init__(self,cx,cy,size,screenWidth,screenHeight):
        self.cx=cx
        self.cy=cy
        self.direction=0
        self.step=[[1,-1],[1,1],[-1,1],[-1,-1]]
        self.size=size
        self.screenWidth=screenWidth
        self.screenHeight=screenHeight
    
    def nextStep(self):
        tx=self.cx+self.step[self.direction][0]
        ty=self.cy+self.step[self.direction][1]
        if(tx<0):
            self.cx=0
            self.cy=ty
            if(self.direction==3):
                self.direction=0
            else:
                self.direction=1
        elif(tx>self.screenWidth-self.size):
            self.cx=self.screenWidth-self.size
            self.cy=ty
            if(self.direction==0):
                self.direction=3
            else:
                self.direction=2
        elif(ty<0):
            self.cy=0
            self.cx=tx
            if(self.direction==0):
                self.direction=1
            else:
                self.direction=2    
        elif(ty>self.screenHeight-self.size):
            self.cy=self.screenHeight-self.size
            self.cx=tx
            if(self.direction==1):
                self.direction=0
            else:
                self.direction=3
        else:
            self.cx=tx
            self.cy=ty
        
