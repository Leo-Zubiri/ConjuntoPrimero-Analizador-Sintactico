"""
Instrucción para convertir la ventana .ui en .py
pyuic5 Window.ui -o Window.py
"""
import Analyzer

from statistics import linear_regression
import sys
from PyQt5 import uic, QtWidgets

qtCreatorFile = "Window.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Área de los Signals
        self.btnGenerar.clicked.connect(self.Generar)

        # Área de variables
        self.Input = []
        self.Variables = set()
        self.Terminales = set()
        self.Inicial = ""
        self.Output = ""

        self.analyze = Analyzer.AnalizadorSintactico()
        
    # Área de los Slots

    def Generar(self):
        print("Generando")

        self.Input = self.txtInput.toPlainText().replace(" ","").split('\n')
        self.Variables = self.txtVariables.toPlainText().replace(" ","").split('\n')
        self.Terminales = self.txtTerminales.toPlainText().replace(" ","").split('\n')
        self.Inicial = self.txtInicial.toPlainText().replace(" ","")

        mapaInputValores = self.mapearInput(self.Input) 
        conjVariables = self.conjuntoElementos(self.Variables)  
        conjTerminales = self.conjuntoElementos(self.Terminales)
        nodoInicial = self.Inicial

        res = self.analyze.ConjuntoPrimero(mapaInputValores,conjVariables,conjTerminales,nodoInicial)

        #[{aB:'a'},{}]
        resFormato = ""

        for cadenaCalc in res:
            for cadena in cadenaCalc:
                resFormato += "Sig({}) = {} \n".format(cadena,cadenaCalc[cadena])

        print(res)
        print(resFormato)

        self.txtOutput.setPlainText(resFormato)


    def conjuntoElementos(self,lista = []):
        conjunto = set()
        for linea in lista:
            linea = linea.split(',')
            conjunto.update(set(linea))
        return conjunto
        
    def mapearInput(self,lista=[]):
        dictionary = {}
        for linea in lista:
            if "->" in linea:
                linea = linea.split('->')
                key = linea[0]
                value = linea[1].split('|')
                dictionary[key] = value
        return dictionary


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())