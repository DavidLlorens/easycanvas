#coding: latin1
'''
Created on 30/09/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''
from easycanvas import EasyCanvas
import time

class Demo9(EasyCanvas):
    def main(self):
        self.easycanvas_configure(title = 'Demo 9 - readkey',
                                  background = 'white',
                                  size = (400,200), 
                                  coordinates = (0,0, 1000, 1000))
        
        print("Blocking readkey. Press 'Escape' to exit")
        print("----------------------------------------")
        k = None
        while k != "Escape":
            k=self.readkey()
            print("\t",k)
        
        print()
        print("Non blocking readkey. Press 'Escape' to exit")
        print("--------------------------------------------")
        k=None
        while k!= "Escape":
            k=self.readkey(False)
            print("\t",k)
            time.sleep(0.5)


Demo9().run()


