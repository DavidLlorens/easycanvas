#coding: latin1
'''
Created on 29/09/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''
from easycanvas import EasyCanvas

import time,sys

class Planeta:
    def __init__(self,x,y,vx,vy,masa,color):
        self.x,self.y,self.vx,self.vy,self.masa,self.color=x,y,vx,vy,masa,color
    def dibuja(self, ec):
        return ec.create_circle(self.x, self.y, self.masa, self.color)
        
class Demo2(EasyCanvas):
    def gravedad(self,p1,lp):
        for p2 in lp:
            x21=p2.x-p1.x
            y21=p2.y-p1.y
            x12=p1.x-p2.x
            y12=p1.y-p2.y
            r3=(x21*x21 + y21*y21) ** 1.5
            masa1r3=p1.masa/r3
            masa2r3=p2.masa/r3
            p1.vx+=masa2r3*(x21)
            p1.vy+=masa2r3*(y21)
            p2.vx+=masa1r3*(x12)
            p2.vy+=masa1r3*(y12)
        p1.x += p1.vx
        p1.y += p1.vy
      
    def main(self):
        t = 400
        self.easycanvas_configure(title = 'Demo 2 - Caos gravitatorio',
                                  background = 'black',
                                  size = (600,600), 
                                  coordinates = (-t, -t, t, t))
        
        #Si quieres añadir mas planetas, adelante...
        lp=[]
        lp.append(Planeta(-200.0,-200.0,0.1,0.0,20.0,'red'))
        lp.append(Planeta(200.0,200.0,-0.1,0.0,20.0,'magenta'))
        lp.append(Planeta(0.0,0.0,0.1,0.1,0.01,'green'))
        
        lc=[]
        for p in lp: lc.append(p.dibuja(self))
        
        t1=time.time()
        self.create_text(0,-400,"Press any key to exit",10,'S','white')
        exitDemo = False
        for _ in range(1000):
            if self.readkey(False) != None: exitDemo = True; break
            old_x=[]
            old_y=[]
            for p in lp:
                old_x.append(p.x)
                old_y.append(p.y)
            for _ in range(15):
                for i in range(len(lp)):
                    self.gravedad(lp[i],lp[i+1:]) 
            old_lc=lc[:]
            lc=[]
            for i in range(len(lp)):
                lc.append(lp[i].dibuja(self))
                self.erase(old_lc[i])
                self.create_line(old_x[i],old_y[i],lp[i].x,lp[i].y,lp[i].color)
            self.update()  
        t2=time.time()
        sys.stderr.write('Execution time: %f seconds\n' % (t2-t1))
        if not exitDemo: self.readkey(True)
    
Demo2().run()
