# -*- coding: utf-8 -*-
"""
Spyder Editor

Programa que permite generar la lista de los núumeros primos que hay entre 1 
y un número introducido por el ususario.

Recordemos que un número es primo si únicamente es divisible entre sí mismo y 
la unidad

"""

######### DECLARACIÓN DE VARIABLES #########

lista = []  #Almacena el conjunto de números primos.

######### DECLARACIÓN DE FUNCIONES #########

def generarPrimos(numero):
    """
    La función generarPrimos muestra por pantalla los números primos comprendidos
    entre 1 y un número pasado como parámetro a la función.

    Parameters
    ----------
    numero : Integer
        Parámetro que especifica el valor máximo de la serie de números primos.

    Returns
    -------
    None.

    """
    for dividendo in range(2, numero):
        
        esPrimo = True    #Por defecto, definimos que el núumero es primo.
        
        for divisor in range(2, dividendo):
            
             #Comprobamos el resultado de la division(resto) entre el Dividendo
             #y cada número existente 
            if(dividendo % divisor == 0):  
                
                esPrimo = False     #Si el resto = 0, no es primo. Se sale del bucle.
                break
            
        #Si la variable esPrimo contiene el valor True, el dividendo no es divisible
        #por ningún número inferior a su valor. El dividendo es primo y se añade
        #a la lista.            
        if (esPrimo):
            lista.append(dividendo)
            
    print(f"La lista de números primos entre 1 y {numero} es: \n")
    
    #Se recorre la lista donde están almacenados los números primos y se 
    #muestra por pantalla.
    for i in range(0,len(lista)):
        print(str(lista[i])+" ",end="")
            
# -*- coding: utf-8 -*-

