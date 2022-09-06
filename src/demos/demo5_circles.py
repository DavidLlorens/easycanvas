#coding: latin1
'''
Created on 28/09/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''
from easycanvas import EasyCanvas

from random import random
from time import sleep

class Demo5(EasyCanvas):
    colores=['red','green','blue','yellow','orange','black','pink']
    
    def entero_azar_rango(self,a,b):
        return int(random()*(b-a+1)+a)
    
    def dibuja_circulo_azar(self):
        x=self.entero_azar_rango(0,1000)
        y=self.entero_azar_rango(0,1000)
        tam=self.entero_azar_rango(10,300)
        col=self.colores[self.entero_azar_rango(0,len(self.colores)-1)]
        return self.create_filled_circle(x,y,tam,col)
  
    def main(self):
        self.easycanvas_configure(title = 'Demo 5 - Círculos aleatorios',
                                  background = 'steelblue',
                                  size = (600,600), 
                                  coordinates = (0,0, 1000, 1000))
        
        self.create_text(500,0,"Press any key to exit",12, anchor="s")       
        l=[]
        k=None
        while k==None:
            k=self.readkey(False)
            if len(l)==10:
                self.erase(l[0])
                del l[0]
            l.append(self.dibuja_circulo_azar())
            sleep(0.05)

Demo5().run()

