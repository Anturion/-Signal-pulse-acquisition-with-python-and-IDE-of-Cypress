from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QLineEdit,
       QPushButton, QSizePolicy,QVBoxLayout, QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import serial, time

import pandas as pd
import numpy as np
import os
global usuario, clave, Matriz

Psoc= serial.Serial('COM6', baudrate=9600) #timeout=1)
Psoc.setDTR(False)
time.sleep(0.2)

#Se crea la funcion principal de Login y de Registro
class Ventana_graficos(QMainWindow):
    
     
     def __init__(self, *args, **kwargs):
        super(Ventana_graficos, self).__init__(*args, **kwargs)
        self.setWindowTitle("Graficos")
        self.setFixedSize(680,300 )
        self.button3 = QPushButton('Registrar Datos', self)
        self.button3.move(100,80)
        self.button4 = QPushButton('Graficar', self)
        self.button4.move(200,80)
        self.button3.clicked.connect(self.onclick_ECG)
        self.button4.clicked.connect(self.onclick_EEG)
        
#Tanto en el boton de registro como en el boton de usuario se verifica si
#El archivo usuario.csv ya exisite y de ser asi lo abre, si no, crea uno vacio        
        
     def onclick_ECG2(self):
        ECG=PlotECG(self)    # Dirige a la clase PlotECG
        ECG.show()           # Muestra la grafica de la señal ecg_signal.txt
    
     def onclick_EEG2(self):
        EEG=PlotEEG(self)    # Dirige a la clase PlotEEG
        EEG.show()        # Muestra la grafica de la señal eeg.txt
    
     def onclick_EMG2(self):
        EMG=PlotEMG(self)    # Dirige a la clase PlotEMG
        EMG.show()          # Muestra la grafica de la señal emg.txt
        
     def onclick_senal_respiratoria2(self):
        senal=Plotsenal_respiratoria(self) # Dirige a la clase Plotsenal_respiratoria
        senal.show()            # Muestra la grafica de la señal_respiratoria.txt


#Se configura la ventana que muestra los botones para graficar las 4 señales
    
#Funcion que retrona a la clase principal donde despues se va hacia la funcion para graficar la señal ECG
     def onclick_ECG(self):
        self.Toma_datos()
#Funcion que retrona a la clase principal donde despues se va hacia la funcion para graficar la señal EGG  
     def onclick_EEG(self):
         Ventana_graficos.onclick_EEG2(self)
#Funcion que retrona a la clase principal donde despues se va hacia la funcion para graficar la señal EMG 
         
    
     def Toma_datos(self):
       self.bandera=0
       self.contador=0
       
       self.Matriz=np.zeros(1250)
       self.time1=float(time.strftime('%S'))
       
       
       self.datos=pd.DataFrame({"Datos":[],'Tiempo':[]})#Se crea dataframe con columnas correspondientes
       self.datos.to_csv("Datos.csv")
       
       for i in np.arange(len(self.Matriz)):
           self.a=Psoc.readline()
           self.a=self.a.decode('ascii','replace').strip()
           
           if self.a != '':
              self.nuevoregistro=pd.DataFrame({'Datos':[self.a]})
              self.datos=self.datos.append(self.nuevoregistro, ignore_index=True)
              self.nuevoregistro=float(self.a)
              self.Matriz[i]=self.a
              if (self.nuevoregistro > 250) and (self.bandera==0):
                 self.bandera=1
                 self.contador=self.contador+1
              if self.nuevoregistro < 200:
                 self.bandera=0
       
              
       self.time2=float(time.strftime('%S'))
       self.tiempo = self.time2-self.time1
       self.frecuencia=(self.contador/self.tiempo)*60
       print(self.frecuencia)
       self.datos.to_csv("Datos.csv")
       self.mean=np.mean(self.Matriz)
       
       #print(self.mean)
#Se configura la ventana donde se va a graficar la señal ECG
class PlotECG(QMainWindow):
    
    
     def __init__(self,  parent=None):
        super(PlotECG, self).__init__(parent)
        self.setWindowTitle("ECG")
        self.setFixedSize(600,600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.fig = Figure((130.0, 6.0), dpi=70, facecolor="#F6F4F2")
        
        m = PlotCanvasECG(self)
        m.move(0,0)

#Se configura la ventana donde se va a graficar la señal EEG
class PlotEEG(QMainWindow):
    
    
     def __init__(self,  parent=None):
        super(PlotEEG, self).__init__(parent)
        self.setWindowTitle("Pulso")
        self.setFixedSize(600,600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.fig = Figure((130.0, 6.0), dpi=70, facecolor="#F6F4F2")
        
        m = PlotCanvasEEG(self)
        m.move(0,0)

#Se configura la ventana donde se va a graficar la señal EMG        
class PlotEMG(QMainWindow):
    
    def __init__(self,  parent=None):
        super(PlotEMG, self).__init__(parent)
        self.setWindowTitle("EMG")
        self.setFixedSize(600,600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.fig = Figure((130.0, 6.0), dpi=70, facecolor="#F6F4F2")
        
        m = PlotCanvasEMG(self)
        m.move(0,0)
 
#Se configura la ventana donde se va a graficar la señal Señal_respiratoria     
class Plotsenal_respiratoria(QMainWindow):
    
     def __init__(self,  parent=None):
        super(Plotsenal_respiratoria, self).__init__(parent)
        self.setWindowTitle("Señal_respiratoria")
        self.setFixedSize(600,600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.fig = Figure((130.0, 6.0), dpi=70, facecolor="#F6F4F2")
        
        m = PlotCanvasSenal_respiratoria(self)
        m.move(0,0)
 
#Esta clase realiza el plot sobre la ventana ya configurada      
class PlotCanvasECG(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
    
#Se define la función que genera la grafica final del ECG
    def plot(self):
        lista=list()
        lista2=list()
        data = open("ecg_signal.txt").readlines()[:-1] #se lee el .txt
        for a in data:
            s = a.replace('\n',"") #Se eliminan los saltos de linea
            lista.append(s)
        for b in lista:
            z = float(b)
            lista2.append(z)
        x = np.arange(1,500,1)
        ax = self.figure.add_subplot(111)
        ax.plot(x,lista2)
        ax.set_title('Señal ECG')
        self.draw()   #Se muestra el ECG sobre la ventana
 
#Esta clase realiza el plot sobre la ventana ya configurada         
class PlotCanvasEEG(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
    
#Se define la función que genera la grafica final del EEG
    def plot(self):
        
        self.Matriz=np.zeros(1250)
        self.Datos=pd.read_csv('Datos.csv')
        for i in np.arange(len(self.Matriz)):
            self.Matriz[i]=float(self.Datos.loc[:,'Datos'][i])
        ax = self.figure.add_subplot(111)
        ax.plot(self.Matriz)
        ax.set_title('Pulso')
        
        self.draw() #Se muestra el EEG sobre la ventana

#Esta clase realiza el plot sobre la ventana ya configurada 
class PlotCanvasEMG(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

#Se define la función que genera la grafica final del EMG  
    def plot(self):
        lista=list()
        lista2=list()
        data = open("emg.txt").readlines()[:-1]
        for a in data:
            s = a.replace('\n',"") #Se eliminan los saltos de linea
            s = s.replace(',',".") #Se reemplaza la coma por punto para tomar los valores adecuados
            lista.append(s)
        for b in lista:
            z = float(b)
            lista2.append(z)
        x = np.arange(0,16383,1)
        ax = self.figure.add_subplot(111)
        ax.plot(x,lista2)
        ax.set_title('Señal EMG')
        self.draw() #Se muestra el EMG sobre la ventana
        

#Esta clase realiza el plot sobre la ventana ya configurada 
class PlotCanvasSenal_respiratoria(FigureCanvas):
    
     def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

#Se define la función que genera la grafica final del Señal_respiratoria    
     def plot(self):
          
        lista=list()
        lista2=list()
        data = open("Señal_respiratoria.txt").readlines()[:-1]
        for a in data:
            s = a.replace('\n',"") #Se eliminan los saltos de linea
            lista.append(s)
        for b in lista:
            z = float(b)
            lista2.append(z)
        x = np.arange(1,100000,1)
        ax = self.figure.add_subplot(111)
        ax.plot(x,lista2)
        ax.set_title('Señal Respiratoria')
        self.draw()#Se muestra la señal_respiratoria sobre la ventana
        
if __name__ == "__main__":  
    app = QApplication([])
    window = Ventana_graficos()
    window.show()
    app.exec_()