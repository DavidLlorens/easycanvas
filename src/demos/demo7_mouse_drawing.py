#coding: latin1
'''
Created on 28/09/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''
from easycanvas import EasyCanvas

class Demo7(EasyCanvas):
    def main(self):
        self.easycanvas_configure(title = 'Demo 7 - Dibujando con el ratón',
                                  background = 'white',
                                  size = (600,600), 
                                  coordinates = (0,0, 1000, 1000))
        self.create_text(500,50,"Dibuja manteniendo el raton pulsado.",8,'s')
        self.create_text(500,0,"Suéltalo para salir.",8,'s')
        
        #espera a que se pulse el botón
        b=0
        while b==0: b,x2,y2=self.mouse_state()

        #mientras botón pulsado
        l=[]
        while 1:
            b,x,y = self.mouse_state()
            if b==0: break
            if x!=None and y!=None and (x!=x2 or y!=y2):
                l.append(self.create_line(x2,y2,x,y))
                if len(l)>60:
                    self.erase(l[0])
                    del l[0]
                x2,y2 = x,y

Demo7().run()