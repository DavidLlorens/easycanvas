#coding: latin1
'''
Created on 04/10/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''
#Es preferible utilizar EasyCanvas creando una clase nueva que hereda de EasyCanvas por dos motivos:
# 1. El editor de Eclipse (PyDev) puede autocompletar.
# 2. El código queda mejor estructurado usando clases
#
#De todos modos, en este ejemplo se muestra cómo utilizarlo sin crear ninguna clase.

from easycanvas import EasyCanvas
       
def main(easycanvas): #puedes poner cualquier otro identificador (p.e. 'ec')
    easycanvas.easycanvas_configure(title = 'Demo 11 - Funciones predefinidas',
                                    background = 'white',
                                    size = (600,600), 
                                    coordinates = (0,0, 1000, 1000))
    #Dibuja matriz de puntos
    for x in range(50,450,21):
        for y in range(550,950,21):
            easycanvas.create_point(x,y,['black','red'][(x+y)%2])
    
    #Dibuja dos circulos (uno relleno y otro no)
    easycanvas.create_filled_circle(750,750,250,'black','blue')
    easycanvas.create_circle(250,250,250,'red')
    
    #Dibuja dos rectangulos (uno relleno y otro no)
    easycanvas.create_rectangle(300,150,400,350,'red')
    easycanvas.create_filled_rectangle(100,150,200,350,'black','red')
    
    #Dibuja dos lineas en cruz
    easycanvas.create_line(500,250,1000,250,'green')
    easycanvas.create_line(750,0,750,500,'black')
    
    #Espera una tecla y termina    
    easycanvas.create_text(500,500,"Press any key to exit",12)
    easycanvas.readkey(True)

EasyCanvas().run(main)
