#coding: latin1
'''
Created on 28/09/2010

@author: David Llorens
@contact: dllorens@lsi.uji.es
@copyright: Universitat Jaume I de Castelló (2010)
'''

import tkinter
import threading, queue, time, sys

class MiExcepcion(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MiExcepcion2(Exception):
    def __init__(self, value1,value2):
        self.value1 = value1
        self.value2 = value2
    def __str__(self):
        return repr(self.value1)+repr(self.value2)

class ThreadedProgram(threading.Thread):
    def __init__(self, p, close):
        threading.Thread.__init__(self)
        self.prog = p
        self.close = close
    def run(self):
        self.prog()
        self.close()
                
class EasyCanvas(object):
    def __init__(self):
        self.kkLock = threading.Lock()
        self._title = "EasyCanvas"
        self._background = "white"
        self.alto = self.ancho = 100    
        self.id = 0
        self.lock = threading.Lock()
        self.exiting = False
        self.ultimoEstadoRaton=(0,None,None)
        self.teclaApretada = False
        self.ultimaTecla = None
        self.bufTeclado = []
        self.keyspressed_set = set()
        self.usedCloseWindowButton = False    
        self.root = tkinter.Tk()
        #self.root.withdraw()
        self.root.resizable(width=False, height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.root.title(self._title)
        self.canvas = tkinter.Canvas(self.root, borderwidth=0, highlightthickness=0, 
                                     height=self.alto, width=self.ancho, background=self._background)
        self.canvas.pack(padx=0,pady=0)
        #self.canvas.bind('<Motion>',self.eventoRatonMovido)
        self.canvas.bind('<B1-Motion>',self.eventoRatonMovidoB1)
        self.canvas.bind('<B2-Motion>',self.eventoRatonMovidoB2)
        self.canvas.bind('<B3-Motion>',self.eventoRatonMovidoB3)
        self.canvas.bind('<Leave>',self.eventoRatonFuera)
        self.canvas.bind('<ButtonRelease>',self.eventoBotonSoltado)
        self.canvas.bind('<Button-1>',self.eventoBoton1Pulsado)
        self.canvas.bind('<Button-2>',self.eventoBoton2Pulsado)
        self.canvas.bind('<Button-3>',self.eventoBoton3Pulsado)

        self.root.bind_all('<KeyPress>', self.eventoTeclaPulsada)
        self.root.bind_all('<KeyRelease>', self.eventoTeclaSoltada)
        self.root.bind_all('<Control-c>', lambda e: self.close())
        
        self.closing = False
        self.cmd_queue = queue.Queue()
        self.event = threading.Event()
        self.easycanvas_configure(coordinates=(0,0, 1000, 1000))
        
        #with self.lock:
        #    p = ThreadedProgram(self.main, self.close)
        #    p.daemon = True
        #    p.start()  
        #self.root.after(100, self.idle)
        #self.root.mainloop()
        
    def idle(self, td=0.5):
        # read and execute any commands waiting on the queue
        #t1 = time.time()
        worked = False
        while True:
            if self.closing: break
            if self.cmd_queue.empty(): break
            
            try:
                func, args, kw = self.cmd_queue.get(block=False)
            except queue.Empty:
                break
            
            try:
                func (*args, **kw)
                worked = True
            except:
                break
            #if time.time() > t1+td: break

        if worked: self.canvas.update_idletasks()  

        self.event.set()
        
        if self.closing:
            self.lock.acquire(True) 
            self.root.destroy()
            self.root.quit()
        else: 
            self.root.after(1, self.idle)
            
    # -----------------------------------------------------------------
    def update(self):
        if self.cmd_queue.empty(): return
        self.event.clear()
        self.event.wait()
    def eventoRatonMovido(self, event, boton=0):
        with self.lock:
            x = event.x/self.escala_x - self.xinf
            y = self.yinf - (event.y-self.alto+1)/self.escala_y
            #sys.__stderr__.write("(%d %d) (%d %d)\n" % (event.x,event.y,x,y))
            self.ultimoEstadoRaton=(boton,x,y)
            return "break"
    def eventoRatonMovidoB1(self, event):
        return self.eventoRatonMovido(event,1)
    def eventoRatonMovidoB2(self, event):
        return self.eventoRatonMovido(event,2)
    def eventoRatonMovidoB3(self, event):
        return self.eventoRatonMovido(event,3)
    def eventoRatonFuera(self,event):
        with self.lock:
            self.ultimoEstadoRaton=(None,None,None)
    def eventoBotonPulsado(self,boton,event):
        with self.lock:
            x = event.x/self.escala_x-self.xinf
            y = self.yinf - (event.y-self.alto+1)/self.escala_y
            self.ultimoEstadoRaton=(boton,x,y)
            return "break"
    def eventoBotonSoltado(self, event):
        with self.lock:
            self.ultimoEstadoRaton=(0,self.ultimoEstadoRaton[1],self.ultimoEstadoRaton[2])
            return "break"
    def eventoBoton1Pulsado(self, event):
        return self.eventoBotonPulsado(1,event)
    def eventoBoton2Pulsado(self, event):
        return self.eventoBotonPulsado(2,event)
    def eventoBoton3Pulsado(self, event):
        return self.eventoBotonPulsado(3,event)
    # -----------------------------------------------------------------    
    
    def eventoTeclaPulsada(self, event):
        x = event.keysym
        if len(x)==1: x=x.lower()
        self.keyspressed_set.add(x)
        
        #if event.char=="":         
        #    return
        
        #print("XXX",event.keysym, event.char, event.keycode)
        self.ultimaTecla = event.keysym
        self.bufTeclado.append(x)
        if len(self.bufTeclado)>1: del self.bufTeclado[0]
        self.teclaApretada = True
        #return "break"
        
    def eventoTeclaSoltada(self, event):
        #print(event.keysym, event.char, event.keycode)
        x = event.keysym
        if len(x)==1: x=x.lower()
        if (x in self.keyspressed_set):
            self.keyspressed_set.remove(x)
        self.teclaApretada = False
        
    def mouse_state(self):
        self.event.clear()
        self.event.wait()
        with self.lock:
            return self.ultimoEstadoRaton
         
    def easycanvas_configure(self, size=(600,400), coordinates=(0,0,1000,1000), title='EasyCanvas', background = 'white'):
        with self.lock:
            if size!=None:
                self.ancho, self.alto = size
                args = {}
                args["width"] = self.ancho
                args["height"] = self.alto
                self.cmd_queue.put((self.canvas.configure, (), args))
            if coordinates!=None:
                self.xinf,self.yinf,self.xsup,self.ysup = coordinates
            if size!=None or coordinates!=None:
                self.cmd_queue.put((self.__erase_all, (), {}))                 
                self.escala_x = (self.ancho-1) / float(self.xsup-self.xinf)
                self.escala_y = (self.alto-1)  / float(self.ysup-self.yinf)
            
            if title != None:
                self.title = title
                self.cmd_queue.put((self.root.title, (title,), {}))          
            if background != None:
                args = {}
                args["background"] = background
                self.cmd_queue.put((self.canvas.configure, (), args))
    
    def readkey(self, blocking=True):
        if blocking:
            while len(self.bufTeclado)==0 and self.closing==False:
                time.sleep(0.01)
        with self.lock:        
            if len(self.bufTeclado)==0:
                return None
            x = self.bufTeclado[0]
            del self.bufTeclado[0]
            return x
    
    def keys_pressed(self):
        with self.lock:
            return self.keyspressed_set
         
    def create_rectangle(self,x1,y1,x2,y2,color='black',relleno=None,**args):
        with self.lock:
            args['outline']=color[:]
            if relleno!=None: args['fill']=relleno[:]
            try:
                x1b = (x1-self.xinf) * self.escala_x 
                y1b = self.alto - 1 - (y1- self.yinf) * self.escala_y
                x2b = (x2-self.xinf) * self.escala_x
                y2b = self.alto - 1 - (y2-self.yinf) * self.escala_y
            except:
                raise MiExcepcion2("coordenadaserroneas", (x1,y1,x2,y2))
    
            try:
                #return self.canvas.create_rectangle(x1b, y1b, x2b, y2b, args)
                self.cmd_queue.put((self.canvas.create_rectangle, (x1b, y1b, x2b, y2b), args))
                self.id+=1
                return self.id
            except:
                if relleno!=None:
                    raise MiExcepcion2("rectanguloRellenoError", (x1,y1,x2,y2,color,relleno))
                else:
                    raise MiExcepcion2("rectanguloError", (x1,y1,x2,y2,color))
           
    def create_filled_rectangle(self,x1,y1,x2,y2,color='black',relleno=None,**args):
        if relleno==None: relleno=color
        return self.create_rectangle(x1,y1,x2,y2,color,relleno,**args);
             
    def create_circle(self,x,y,radio,color='black',relleno=None,**args):
        with self.lock:
            #if (self.exiting): return
            args['outline']=color[:]
            if relleno!=None: args['fill']=relleno[:]
            try:
                x1b=(x-self.xinf-radio)* self.escala_x
                x2b=(x-self.xinf+radio)* self.escala_x
                y1b=self.alto - 1 - (y-self.yinf-radio)* self.escala_y
                y2b=self.alto - 1 - (y-self.yinf+radio)* self.escala_y
            except:
                raise MiExcepcion2("coordenadaserroneas", (x,y))
            try:
                #return self.canvas.create_oval(x1b, y1b, x2b, y2b, args)
                self.cmd_queue.put((self.canvas.create_oval, (x1b, y1b, x2b, y2b), args))
                self.id+=1
                return self.id
            except:
                if relleno!='no':
                    print(self.canvas)
                    raise MiExcepcion2("circuloRellenoError", (x,y,radio,color,relleno))
                else:
                    raise MiExcepcion2("circuloError", (x,y,radio,color))
             
    def create_filled_circle(self,x,y,radio,color='black',relleno=None,**args):
        if relleno==None: relleno=color
        return self.create_circle(x,y,radio,color,relleno,**args) 
         
    def create_point(self,x,y,color='black',**args):
        """Draws a point

        Arguments:
            x, y -- point coordinates
            color -- color name (default is 'black')

        Returns:
            A number (identifier). You can use this 'id' to move o delete the point
        """
        with self.lock:
            args['fill']=color[:]
            args['width']=2
            try:
                x1b=(x-self.xinf)*self.escala_x - 0.5
                x2b=x1b+2
                y1b=self.alto - 1 - (y-self.yinf)*self.escala_y
            except:
                raise MiExcepcion2("coordenadaserroneas", (x,y))
            try:
                #return self.canvas.create_line(x1b, y1b, x2b, y1b, args)
                self.cmd_queue.put((self.canvas.create_line, (x1b, y1b, x2b, y1b), args))
                self.id+=1
                return self.id
            except:
                raise MiExcepcion2("puntoError", (x,y,color))
        
    def create_line(self,x1,y1,x2,y2,color='black',**args):
        """Draws a line between two points

        Arguments:
            x1, y1 -- start point coordinates
            x2, y2 -- end point coordinates
            color -- color name (default is 'black')

        Returns:
            A number (identifier). You can use this 'id' to move o delete the line
        """
        with self.lock:
            args['fill']=color
            try:
                x1b = (x1-self.xinf) * self.escala_x 
                y1b = self.alto - 1 - (y1- self.yinf) * self.escala_y
                x2b = (x2-self.xinf) * self.escala_x
                y2b = self.alto - 1 - (y2-self.yinf) * self.escala_y
            except:
                raise MiExcepcion2("coordenadaserroneas", (x1,y1,x2,y2))
            try:
                #id = self.canvas.create_line(x1b, y1b, x2b, y2b, args.copy())
                self.cmd_queue.put((self.canvas.create_line, (x1b, y1b, x2b, y2b), args))
                self.id+=1
                return self.id
            except:
                print(x1b, y1b, x2b, y2b, args)
                raise MiExcepcion2("lineaError", (x1,y1,x2,y2,color))
         
    def create_text(self,x,y,cadena,tam=10,anchor='center',color='black',justify="left",**args):
        with self.lock:
            args['text']=cadena
            args['anchor']=anchor.lower()
            args['fill']=color
            args['justify']=justify
            args['font']=('courier',int(tam*1.15+2),'bold')
            try:
                xb = (x-self.xinf) * self.escala_x 
                yb = self.alto - 1 - (y- self.yinf) * self.escala_y
            except:
                raise MiExcepcion2("coordenadaserroneas",(x,y))
            try:
                #return self.canvas.create_text(xb, yb, args)
                self.cmd_queue.put((self.canvas.create_text, (xb, yb), args))
                self.id+=1
                return self.id
            except:
                raise MiExcepcion2("textoError", (x,y,cadena,anchor))
    
    def __erase_list(self, alist): 
        for indice in alist: self.canvas.delete(indice)
    
    def __erase_all(self): 
        for indice in self.canvas.find_all(): self.canvas.delete(indice)
            
    def erase(self,indice=None):
        with self.lock:
            if indice==None:
                try: 
                    #self.__erase_all()
                    self.cmd_queue.put((self.__erase_all, (), {}))
                except tkinter.TclError: pass
            elif isinstance(indice, list) and len(indice)>0:
                try: 
                    #list(map(self.canvas.delete, indice))
                    self.cmd_queue.put((self.__erase_list, (indice,), {}))
                except:
                    raise MiExcepcion2("indiceBorradoError", indice)
            else:
                try:
                    #self.canvas.delete(indice)
                    self.cmd_queue.put((self.canvas.delete, (indice,), {}))
                except:
                    raise MiExcepcion2("indiceBorradoError", indice)
    
    def save_EPS(self, nombre):
        self.cmd_queue.put((self.__save_EPS, (nombre), {}))
        
    def __save_EPS(self, nombre):
        data=self.canvas.postscript(pagey=430,pagex=297,
                                    height=self.alto,width=self.ancho+2,x=-1,
                                    pagewidth='20.0c')
        try:
            f=open(nombre,'w')
            try:     f.write(data)
            finally: f.close()
            res=1
        except:
            res=0
        return res
     
    def move(self,tags,x,y):
        with self.lock:
            try:
                xb = x*self.escala_x 
                yb = -y*self.escala_y
            except:
                raise MiExcepcion2("coordenadaserroneas", (x,y))
            try: 
                #self.canvas.move(tags,xb,yb)
                self.cmd_queue.put((self.canvas.move, (tags, xb, yb), {}))
            except:
                raise MiExcepcion2("moveError", (tags,x,y))
    
    def after(self, t, func):
        with self.lock:
            if self.closing: return
            self.root.after(t, func)
            
    def close(self):
        self.usedCloseWindowButton = False 
        self.closing = True

    def closeWindow(self):
        self.usedCloseWindowButton = True
        self.closing = True
        
    def run(self, efunc=None):
        if efunc==None: 
            func = self.main
        else:
            func = lambda: efunc(self)
        with self.lock:
            p = ThreadedProgram(func, self.close)
            p.daemon = True 
            p.start()  

        self.root.after(100, self.idle)
        self.root.mainloop()
        if self.usedCloseWindowButton:
            sys.exit()
        
    def main(self):
        self.easycanvas_configure(title = 'EasyCanvas test',
                                  background = 'white',
                                  size = (600,600), 
                                  coordinates = (0,0, 1000, 1000))
        self.create_filled_rectangle(100, 100, 900, 900, "black", "red")
        self.create_text(500, 500, "To exit press any key\nor\nclose the window", 14, justify="center")
        self.readkey(True)
    
if __name__ == "__main__":
    EasyCanvas().run()