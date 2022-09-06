#coding: latin1
'''
Created on 28/09/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''
from easycanvas import EasyCanvas

class Demo8(EasyCanvas):
    
    def wait_button(self):
        #espera a que se suelte el botón
        b=1
        while b!=0: b,_,_=self.mouse_state()
        #espera a que se pulse el botón
        b=0
        while b==0: b,x,y=self.mouse_state()
        return b,x,y
            
    def main(self):
        self.easycanvas_configure(title = 'Demo 8 - Uso de los botones del ratón',
                                  background = 'white',
                                  size = (600,600), 
                                  coordinates = (0,0, 1000, 1000))
        self.create_text(500,50,"Botón izq.: dibuja círculo",8,'s')
        self.create_text(500,0,"Botón der.: termina programa",8,'s')
        
        l=[]
        while 1:
            #espera a que se pulse el botón
            b,x,y = self.wait_button()
            
            if b == 1:  #dibuja un circulo
                l.append(self.create_circle(x,y,20))
                if len(l)>20: #como máximo se permiten 20 círculos
                    self.erase(l[0])
                    del l[0]    #se borra el más viejo
            else:       #si pulsa otro boton salir 
                break

Demo8().run()