VARIABLES = set()
TERMINALES = set()


def RulesConjuntoPrimero(cadena=""):
    if cadena in VARIABLES:
        # Union de conjuntos
        pass
    elif cadena in TERMINALES:
        return set(cadena)
    
    return set()