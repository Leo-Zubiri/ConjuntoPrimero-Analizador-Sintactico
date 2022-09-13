
import re # Regular Expressions
class AnalizadorSintactico:
    VARIABLES = set()
    TERMINALES = set()
    INICIAL = ""
    INPUT = {}
    RESULT = {}
    CURRENTVAR = ""
    COUNT = 0

    def ConjuntoPrimero(self,_input,_variables,_terminales,_inicial):
        self.INPUT = _input
        self.VARIABLES = _variables
        self.TERMINALES = _terminales
        self.INICIAL = _inicial
        
        self.VARIABLES = list(self.VARIABLES)
        self.VARIABLES.sort(reverse=True)

        self.TERMINALES = list(self.TERMINALES)
        self.TERMINALES.sort(reverse=True)

        return self.CalcularConjSiguiente()
        #return self.CalcularConjPrimero() 
        

    def RulesConjuntoPrimero(self,cadena=""):
        # Cadena Inicia con un TERMINAL ?
        for T in self.TERMINALES:
            if T in ["(",")","[","]","+","*","-","/"]:
                # Caracter especial para el REGEX
                if re.search("^\{}".format(T), cadena):
                    self.RESULT[cadena] = T
                    return set([T])
            else:
                if re.search("^{}".format(T), cadena):
                    #print(T,cadena)
                    self.RESULT[cadena] = T
                    return set([T])
        # Cadena Inicia con una VARIABLE
        for V in self.VARIABLES:     

            if re.search("^{}".format(V), cadena):
                if self.CURRENTVAR == V and V not in self.RESULT:
                    if self.COUNT == 30:
                        print("Recursividad")
                        self.COUNT = 0
                        return set()
                    self.COUNT += 1
                cadenas = self.INPUT[V] 
                union = set()
                for cadena in cadenas:
                    union.update(set(self.RulesConjuntoPrimero(cadena)))
                self.RESULT[cadena] = union
                
                return union
        return set()

    def CalcularConjPrimero(self):
        #print(self.INPUT)
        RESULT = []

        for variable in self.INPUT:
            self.CURRENTVAR = variable
            for cadena in self.INPUT[variable]:
                res = self.RulesConjuntoPrimero(cadena)
                #print(cadena," ",res)
                RESULT.append({cadena:res})

            self.CURRENTVAR = ""
            
        return RESULT

    # ----------------------------------

    def CalcularConjSiguiente(self):
        RESULT = []
        for var in self.VARIABLES:
            res = self.ConjuntoSiguiente(var) 
            RESULT.append({var:res})  
            print("")
        return RESULT


    def ConjuntoSiguiente(self,var):
        conjResultante = set()
        
        if var == self.INICIAL:
            conjResultante.update(['$'])
            #print("Es inicial")
            
        for key,cadenas in self.INPUT.items():
            A = key
            #print(key,cadenas)
            for cadena in cadenas:
                if var in cadena:
                    alpha = ""
                    B = var 
                    beta = ""
                    
                    aux = cadena.split(B)
                    alpha = aux[0]
                    beta = aux[1]
                    

                    if len(beta) > 0 and beta[0] != "'":
                        print("cadena",cadena,aux)
                        res = self.RulesConjSiguiente(A,alpha,B,beta)
                        conjResultante.update(res)  
        
        print(var,conjResultante)
        return conjResultante
    
    def RulesConjSiguiente(self,A,alpha,B,beta):
        # Produccion A -> alpha B beta
        if beta != "":
            return self.RulesConjuntoPrimero(beta)
        elif alpha != "":
         # Produccion A -> alphaB    
            res = self.ConjuntoSiguiente(A)
            return res