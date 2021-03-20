import tkinter as tk
import tkinter.ttk as ttk
import queue
import threading
from sense_emu import SenseHat
from time import sleep

sense = SenseHat()

class Aplicacion:
    def __init__(self):
        self.ventana1=tk.Tk()
        self.ventana1.title("Menu SenseHat")

        self.labelframe1=ttk.LabelFrame(self.ventana1, text="Control:")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)        
        
        self.boton1 = tk.Button(self.labelframe1, text = "Parar", command = self.Parar)
        self.boton1.grid(column=1 , row = 0, padx=5, pady=10 )
        
        self.labelframe2=ttk.LabelFrame(self.ventana1, text="Medidas:")        
        self.labelframe2.grid(column=0, row=1, padx=5, pady=10)        
        
        self.dato=tk.StringVar(value="25.0")        
        self.entryCantidad=tk.Entry(self.labelframe2, width=10, textvariable=self.dato)
        self.entryCantidad.grid(column=1, row=1)

        self.seleccion=tk.IntVar()
        self.seleccion.set(2)
        
        self.radio1=tk.Radiobutton(self.labelframe2,text="Temp", variable=self.seleccion, value=1)
        self.radio1.grid(column=0, row=2)
        self.radio2=tk.Radiobutton(self.labelframe2,text="Presion", variable=self.seleccion, value=2)
        self.radio2.grid(column=1, row=2)
        self.radio3=tk.Radiobutton(self.labelframe2,text="Humedad", variable=self.seleccion, value=3)
        self.radio3.grid(column=2, row=2)

        self.labelframe3=ttk.LabelFrame(self.ventana1, text="Resultados:")        
        self.labelframe3.grid(column=0, row=2, padx=5, pady=10, sticky="WE")        

        self.labelResTemp1=tk.Label(self.labelframe3, text="Temp:")
        self.labelResTemp1.grid(column=0, row=4)

        self.labelResTemp2=tk.Label(self.labelframe3, )
        self.labelResTemp2.grid(column=1, row=4)

        self.labelResPresion1=tk.Label(self.labelframe3, text="Presion:")
        self.labelResPresion1.grid(column=0, row=5)

        self.labelResPresion2=tk.Label(self.labelframe3, )
        self.labelResPresion2.grid(column=1, row=5)

        self.labelResHumedad1=tk.Label(self.labelframe3, text="Humedad:")
        self.labelResHumedad1.grid(column=0, row=6)

        self.labelResHumedad2=tk.Label(self.labelframe3, )
        self.labelResHumedad2.grid(column=1, row=6)

        self.ventana1.mainloop()

    def Parar(self):
        self.MostrarDatos()                         

    def process_queue(self):
        try:
            resHumedad = self.queueHumedad.get(0)
            resTemperatura = self.queueTemperatura.get(0)
            resPresion = self.queuePresion.get(0)

            if self.seleccion.get()==1:
                self.labelResTemp2.configure(text=resTemperatura, foreground="blue")
            else:
                self.labelResTemp2.configure(text="-", foreground="red")

            if self.seleccion.get()==2:   
                self.labelResPresion2.configure(text=resPresion , foreground="blue")
            else:
                self.labelResPresion2.configure(text="-", foreground="red")

            if self.seleccion.get()==3:  
                self.labelResHumedad2.configure(text=resHumedad , foreground="blue")
            else:
                self.labelResHumedad2.configure(text="-", foreground="red")

        except queue.Empty:
            self.ventana1.after(100, self.process_queue)

    def MostrarDatos(self):
        self.queueHumedad = queue.Queue()
        self.queueTemperatura = queue.Queue()
        self.queuePresion = queue.Queue()
        Worker(self.queueHumedad, self.queueTemperatura, self.queuePresion)
        


#Hebra
class Worker(threading.Thread):
    def __init__(self, queueHumedad, queueTemperatura, queuePresion):
        threading.Thread.__init__(self)
        self.queueHumedad = queueHumedad
        self.queueTemperatura = queueTemperatura
        self.queuePresion = queuePresion

    def run(self):
        try:
            Humedad = sense.humidity
            Temperatura = sense.temperature
            Presion = sense.pressure
            
            self.queueHumedad.put(Humedad)
            self.queueTemperatura.put(Temperatura)
            self.queuePresion.put(Presion)
        except:
            self.queue.put("Error")


aplicacion1=Aplicacion()