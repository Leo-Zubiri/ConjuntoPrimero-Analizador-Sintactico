
import re # Regular Expressions
class AnalizadorSintactico:
    VARIABLES = set()
    TERMINALES = set()
    INICIAL = ""
    INPUT = {}
    RESULT = {}

    def ConjuntoPrimero(self,_input,_variables,_terminales,_inicial):
        self.INPUT = _input
        self.VARIABLES = _variables
        self. TERMINALES = _terminales
        self. INICIAL = _inicial
        
        self.VARIABLES = list(self.VARIABLES)
        self.VARIABLES.sort(reverse=True)

        self.TERMINALES = list(self.TERMINALES)
        self.TERMINALES.sort(reverse=True)

        return self.CalcularConjPrimero() 
        

    def RulesConjuntoPrimero(self,cadena=""):
        # Cadena Inicia con un TERMINAL ?
        for T in self.TERMINALES:
            if re.search("^{}".format(T), cadena):
                self.RESULT[cadena] = T
                return set(T)

        # Cadena Inicia con una VARIABLE
        for V in self.VARIABLES:     
            if re.search("^{}".format(V), cadena):
                cadenas = self.INPUT[V] 
                union = set()
                for cadena in cadenas:
                    union.update(set(self.RulesConjuntoPrimero(cadena)))
                self.RESULT[cadena] = union
                return union
        return "{ - }"

    def CalcularConjPrimero(self):
        print(self.INPUT)
        RESULT = []

        for variable in self.INPUT:
            for cadena in self.INPUT[variable]:
                res = self.RulesConjuntoPrimero(cadena)
                print(cadena," ",res)
                RESULT.append({cadena:res})
            
        return RESULT