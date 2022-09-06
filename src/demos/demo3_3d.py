#coding: latin1
'''
Created on 29/09/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''
from easycanvas import EasyCanvas

from libsimple3d import Escena3D, Cubo3D, Piramide3D, Punto3D #importa módulo de 3D
from math import sin, cos, pi
import time

class Demo3(EasyCanvas):
    ppd=1500  
    escena = Escena3D(ppd) 
    
    def paseo(self):
        pi2 = 2*pi
        lin2 = []
        nl2 = 0
        t=0.0
        pv = Punto3D(lambda t: 10000*sin(t),
                     lambda t: 10000*sin(t),
                     lambda t: 10000*cos(t))
        f=0
        inc = 0.04
        fps = None
        self.create_text(0,-500,"Pulsa <Return> para salir:",10,'S')
        t1 = time.time()
        while 1:
            f += 1
            t = (t+inc) % pi2    
            pv.posParametrica(t)
            self.escena.puntoVista(pv)
            lineas = self.escena.dibuja()
            nl = len(lineas)
            lin=[]
            for i in range(nl):
                lin.append(self.create_line(*lineas[i]))
                if i<nl2: self.erase(lin2[i])
            self.erase(lin2[nl:])
            #if t>pi: break
            if t>pi-1e-2 or t<1e-2: inc=-inc
            lin2 = lin
            nl2 = nl
            if fps!=None: self.erase(fps)
            t2 = time.time()
            if t2 != t1:
                fps = self.create_text(0,-450, "Frames por segundo: %.2f" % (float(f)/(t2-t1)),10,'S')
            self.update()
            if self.readkey(False) == "Return": break
        return f
    
    def main(self):
        self.easycanvas_configure(title = 'Demo 3 - Paseo 3D',
                                  background = 'steelblue',
                                  size = (600,600), 
                                  coordinates = (-500,-500,500,500))
        for x,y,z in [(1000,1000,1000),(1000,1000,-1000),
                      (1000,-1000,1000),(1000,-1000,-1000),  
                      (-1000,1000,1000),(-1000,1000,-1000),  
                      (-1000,-1000,1000),(-1000,-1000,-1000)]:
            if y==-1000:
                cubo = Cubo3D(1500,Punto3D(x,y,z))  
            else:  
                cubo = Piramide3D(Punto3D(1500,1500,1500),Punto3D(x,y,z))  
            self.escena.insertar(cubo)   


        self.paseo()

Demo3().run()