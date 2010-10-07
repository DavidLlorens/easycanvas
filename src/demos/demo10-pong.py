#coding: latin1
'''
Created on 30/09/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''
from easycanvas import EasyCanvas
import time

class Ball():
    def __init__(self, ec, r, x, y, dx, dy, xmax, ymax): 
        self.ec = ec
        self.r, self.x, self.y, self.dx, self.dy = r, x, y, dx, dy
        self.xmax, self.ymax = xmax, ymax
        self.id = ec.create_filled_circle(x,y,r,"black", "whitesmoke", tag="ball")
        
    def tick(self):
        xold, yold = self.x, self.y
        x2 = self.x+self.dx
        if (x2-self.r <= 0):
            x2=self.r
            self.dx*=-1
        elif (x2+self.r >= self.xmax):
            x2=self.xmax-self.r
            self.dx*=-1
        self.x = x2   
        y2 = self.y+self.dy
        if (y2-self.r <= 0):
            xy=self.r
            self.dy*=-1
        elif (y2+self.r >= self.ymax):
            y2=self.ymax-self.r
            self.dy*=-1
        self.y = y2
        #self.ec.move("ball",self.x-xold, self.y-yold)
        id=self.id
        self.id = self.ec.create_filled_circle(self.x, self.y, self.r, "black", "whitesmoke")
        self.ec.erase(id)
        
class Demo10(EasyCanvas):
    def tick(self):
        k = self.keys_pressed()    
        #mueve la pala
        x2 = self.x
        if "Left" in k and "Right" not in k:
            self.x-=self.a
            if self.x<0: self.x=0 
        elif "Right" in k and "Left" not in k:
            self.x+=self.a
            if self.x+self.sx>=self.tx: self.x=self.tx-self.sx-1 
        self.move("pala",self.x-x2,0)
        #mueve la bola
        self.ball.tick()

        if "Escape" not in k:
            self.after(1000//40, self.tick)

    def main(self):
        self.tx = 601
        self.easycanvas_configure(title = "Demo 10 - keys_pressed for 'analog' gaming",
                                  background = 'steelblue',
                                  size = (self.tx,601), 
                                  coordinates = (0,0, self.tx-1, 600))
        self.sx, self.sy = 100, 20
        self.x, self.y = 10,10
        self.create_rectangle(self.x, self.y, self.x+self.sx, self.y+self.sy, "black", "whitesmoke", tag="pala")
        self.a=self.tx//30
        
        self.ball = Ball(self,10,100,100,5,10, 600, 600)
        self.tick()
        while (True):
            time.sleep(1)
            
Demo10().run()