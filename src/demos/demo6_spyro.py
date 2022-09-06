#coding: latin1
'''
Created on 28/09/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''
from easycanvas import EasyCanvas

from math import sin,cos,pi
import time

class Demo6(EasyCanvas):
    #Cambiando estos valores se obtiene dibujos diferentes
    radioCirculo = 200
    radioDisco = 75
    distLapizCentroDisco = 50
    
    velocidad = 0.05    #reducir para aumentar velocidad
    dientesCirculo = 40 # no es necesario cambiar este valor
    
    def rueda(self, x0, y0, radio, numDientes, profDiente, ini):
        r1 = radio-profDiente/2.0
        r2 = radio+profDiente/2.0
        l=[]
        da = 2.0*pi/numDientes/4.0
        cte = 2.0*pi/numDientes
        ini = ini-da*3/2 
        for i in range(0,numDientes):
            angle = i*cte+ini
            l.append((r1*cos(angle)+x0, r1*sin(angle)+y0))
            l.append((r2*cos(angle+da)+x0, r2*sin(angle+da)+y0))
            l.append((r2*cos(angle+2*da)+x0, r2*sin(angle+2*da)+y0))
            l.append((r1*cos(angle+3*da)+x0, r1*sin(angle+3*da)+y0))
        return l+[l[0]]
    
    def mcm(self,i,j):
        while 1:
            r=i%j
            if r==0: return j
            i,j=j,r
    
    def spyro(self,a,b,rd,di):
        profD=10 # profundidad diente
        self.create_filled_circle(0,0,3,'red')
        xx2, yy2 = a-b, 0
        print("Tamaño diente: %g" % (float(a)/di))
        print("Nº dientes agujero:",di)
        l=self.rueda(0, 0, a-profD/2, di, profD, 0)
        self.dibuja_rueda(l,'red')
        self.rold=[] # para que no se borre la rueda roja (es fija)
        n2=int(di*float(b)/a)
        print("Nº dientes disco:",n2)
        b2=n2*float(a)/di
        if b2!=b:
            print("Ajustado radio del disco: %g -> %g" % (b,b2))
            b=b2
          
        rab=(a-b)
        l=self.rueda(rab, 0, b-profD/2, n2, profD, 0)
        self.dibuja_rueda(l,'blue')
        self.create_filled_circle(rab,0,3,'blue',tags='disco')
        self.create_filled_circle(rab+rd,0,3,'black',tags='lapiz')
        theta=0.0
        thetad=pi*0.02#12#52
        aoverb=float(di)/n2
        N = n2/self.mcm(di,n2)
        print("Vueltas:",N)
        x2, y2 = rab+rd, 0.0
        ang=0
        inc=-((di-n2)*(2*pi/n2))/100
        l=self.create_line(x2,y2,xx2,yy2,'blue')
        for _ in range(1, int(100*N+1)):
            ang+=1
            theta+=thetad
            phi=theta*aoverb
            phi=-ang*inc
            xx, yy = rab*cos(theta), rab*sin(theta)
            x, y   = xx+rd*cos(phi), yy-rd*sin(phi)
            self.create_line(x,y,x2,y2)
            self.move('lapiz',x-x2,y-y2)
            c=self.rueda(xx, yy, b-profD/2, n2, profD, -phi)
            self.dibuja_rueda(c,'blue')
            self.move('disco',xx-xx2,yy-yy2)
            self.erase(l)
            l = self.create_line(x, y, xx, yy, 'blue')
            x2, y2   = x, y
            xx2, yy2 = xx, yy
            time.sleep(self.velocidad)
    
    def dibuja_rueda(self,l,color):
        r=[]
        x2,y2=l[0]
        for x,y in l[1:]:
            r.append(self.create_line(x,y,x2,y2,color))
            if len(self.rold)>0: 
                self.erase(self.rold[0])
                del self.rold[0]
            x2,y2=x,y
        self.erase(self.rold)
        self.rold = r
    
    def main(self):
        self.easycanvas_configure(title = 'Demo 6 - Spyro',
                                  background = 'white',
                                  size = (600,600), 
                                  coordinates = (-250,-250,250,250))
        self.rold=[]
        self.spyro(self.radioCirculo,self.radioDisco,self.distLapizCentroDisco,self.dientesCirculo)

        self.create_text(0,-250,"Press any key to exit",12,'s')
        self.readkey(True)
    
Demo6().run()
