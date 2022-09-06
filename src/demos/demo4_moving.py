#coding: latin1
'''
Created on 28/09/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''
from easycanvas import EasyCanvas

import time

class Demo4(EasyCanvas):
    def main(self):
        self.easycanvas_configure(title = 'Demo 4 - Interferencia',
                                  background = 'steelblue',
                                  size = (600,600), 
                                  coordinates = (0,0, 1000, 1000))       
        for i in range(25):
            self.create_circle(0,500,i*20,'black',tags='c')
            self.create_circle(1000,500,i*20,'black',tags='c2')

        for i in range(1000):
            time.sleep(0.005)
            self.move('c',1,0)
            self.move('c2',-1,0)
        
        textId=self.create_text(500,500,"Press any key to delete left circles",12)
        self.readkey(True)
        self.erase(['c2',textId])
        self.create_text(500,500,"Press any key to exit",12)
        self.readkey(True)
    
Demo4().run()