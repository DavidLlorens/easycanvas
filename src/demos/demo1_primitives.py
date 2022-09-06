#coding: latin1
'''
Created on 28/09/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''
from easycanvas import EasyCanvas
 
class Demo1(EasyCanvas):      
    def main(self):
        self.easycanvas_configure(title = 'Demo 1 - Funciones predefinidas',
                                  background = 'white',
                                  size = (600,600), 
                                  coordinates = (0,0, 1000, 1000))
        l=[]
        #Dibuja matriz de puntos
        for x in range(50,450,21):
            for y in range(550,950,21):
                l.append(self.create_point(x,y,['black','red'][(x+y)%2]))
                
        #Dibuja dos circulos (uno relleno y otro no)
        l.append(self.create_filled_circle(750,750,250,'black','blue'))
        l.append(self.create_circle(250,250,250,'red'))
    
        #Dibuja dos rectangulos (uno relleno y otro no)
        l.append(self.create_rectangle(300,150,400,350,'red'))
        l.append(self.create_filled_rectangle(100,150,200,350,'black','red'))
        
        #Dibuja dos lineas en cruz
        l.append(self.create_line(500,250,1000,250,'green'))
        l.append(self.create_line(750,0,750,500,'black'))
        
        #escribe texto
        l.append(self.create_text(500,500,"Press any key to delete all",12))
        
        #Borra todos los objetos al pulsar Return
        self.readkey(True)
        for indice in l:
            self.erase(indice)
            
        self.create_text(500,500,"Press any key to exit",12)
        self.readkey(True)


Demo1().run()


