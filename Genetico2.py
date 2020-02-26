"""
<h1>Curso de Sistemas Inteligentes</h1>
<h2>Práctica de Algoritmos Genéticos - David Hernández Cárdenas - Periodo 2020-1</h2>
<hr>

<h4> Se requiere optimizar la producción de una empresa de manufactura y para ello se hará uso de un algoritmo genético. </h4>

El individuo planteado se basa en una lista de números que representan maquinas. Cabe resaltar que cada máquina que se encuentra en el arreglo es la seleccionada para la realización de una operación:

[[2,1,2,1,3,2,1,3]]

Por otro lado, el índice de cada uno de los valores de la lista es la operación que se realizará en dicha máquina. Se denota en otra lista de manera referencial (no es el individuo) así:

[[[1,1]],[[1,2]],[[1,3]],[[2,1]],[[2,2]],[[3,1]],[[3,2]],[[3,3]]]
"""

import random

cPrevioOp = [[1,1],[1,2],[1,3],[2,1],[2,2],[3,1],[3,2],[3,3]]
cPrevioMaq = [[1,2],[2],[1,2,3],[1,2],[1],[2,3],[1,2,3],[1,2,3]]
cPrevioTiempo = [[10,8],[12],[4,5,6],[11,18],[20],[12,16],[7,12,4],[14,11,9]]
maxMaq = 3


# Función de selección
# Elige dos individuos aleatoriamente que van a ser cruzados
# generacion: lista de individuos que componen la generacion actual
# Retorna las posiciones de dos individuos en la generacion
def seleccion(generacion):
    tGen = len(generacion)
    ind1 = random.randint(1, tGen-2)
    ind2 = ind1
    while ind1 == ind2:
        ind2 = random.randint(1,tGen-2)
    return (generacion[ind1], generacion[ind2])


# Función de selección tipo ruleta
# Elige dos individuos aleatoriamente al rodar una ruleta dónde aquellos individuos con mejor fitness tienen mayor probabilidad de salida
# Se procede calculando la suma total del fitness de todos los indiviuos
# Posteriormente se crea una lista de repetidos dónde aquellos individuos con mejor fitness tienen más apariciones
# generacion: lista de individuos que componen la generacion actual
# Retorna dos individuos en la generacion
def seleccionRuleta(generacion):
    tGen = len(generacion)
    fitnessT,prob,suma = 0,0,0
    listInd = []
    val = 0
    for i in generacion:
        fitnessT += fitness(i)
    for i in generacion:
        val = int(fitnessT/fitness(i))
        listInd += [i] * val
    ind1 = random.choice(listInd)
    ind2 = ind1
    if len(set(tuple(row) for row in listInd))!=1:
        while ind1 == ind2:
            ind2 = random.choice(listInd)
    return (ind1,ind2)

# Funcion de descarte de los individuos menos aptos
# generacion: lista de individuos que componen la generacion actual
# Retorna la generacion despues de eliminar la mitad menos apta
def descarte(generacion):
    tGen = len(generacion)
    return (generacion[:tGen//2])


# Funcion de cruce
# Precondicion: ambos individuos tienen la misma longitud
# El orden de las operaciones se respeta al cruzar
# ind1 e ind2 son individuos de la generacion actual
# Retorna dos nuevos individuos obtenidos a partir de ind1 e ind2 por cruce
def cruce(ind1,ind2):
    tInd = len(ind1)
    pivot = random.randint(1,tInd-1)
    new1 = ind1[:pivot] + ind2[pivot:]
    new2 = ind2[:pivot] + ind1[pivot:]
    return (new1, new2)


# Funcion de mutacion
# ind es un individuo de la generacion actual
# cPrevioMaq son aquellas máquinas elegibles para cada operación
# prob es un valor entre 0 y 1 que corresponde a la probabilidad de mutacion
# Se elige una de las maquinas de manera aleatoria y se cambia por otra de las maquinas elegibles de esa operación
# En caso tal de no tener otra máquina elegible no se muta
# Retorna un individuo que puede ser identico al que entró o puede tener un cambio aleatorio en una posicion
def mutacion(ind,cPrevioMaq,prob):
    flg = True
    while flg:
        p = random.randint(1,100)
        if p < prob*100: 
            tInd = len(ind)
            q = random.randint(0,tInd-1)
            val = ind[q]
            for i in range(len(cPrevioMaq[q])-1):
                if cPrevioMaq[q][i]!=val: 
                    val = cPrevioMaq[q][i]
            flg = False
    ind[q] = val      
    return (ind)

# Funcion newInd
# cPrevioMaq son aquellas máquinas elegibles para cada operación
# Genera un nuevo individuo aleatorio
# Retorna el individuo construido
def newInd(cPrevioMaq):
    tcPrevio = len(cPrevioMaq)
    ind = []
    for i in range(tcPrevio):
        x = random.choice(cPrevioMaq[i])
        ind.append(x)
    return ind

# Funcion primeraGen
# nIndGen: numero de individuos por generacion
# cPrevioMaq son aquellas máquinas elegibles para cada operación
# Retorna la primera generacion poblada con el numero de individuos requeridos
def primeraGen(nIndGen,cPrevioMaq):
    generacion = []
    for i in range(nIndGen):
        generacion.append(newInd(cPrevioMaq))
    return generacion

# Funcion fitness
# ind: es un individuo de la generacion actual
# Se le asigna como puntaje el tiempo total de la realización de todos los trabajos
# Retorna un valor numerico que representa la aptitud del individuo
def fitness(ind):
    tcPrevio = len(cPrevioMaq)
    score = 0
    maq = 0
    vals = []
    vals = []
    times = [0]*maxMaq
    for i in range(tcPrevio):
        maq = cPrevioMaq[i].index(ind[i])
        vals.append(cPrevioTiempo[i][maq])
    for i in range(tcPrevio):
        times[ind[i]-1]+=vals[i]
    score = max(times)
    return score

# Funcion general
# nIndGen: numero de individuos por generacion
# nGen: numero de generaciones que realizara el algoritmo
# pMut: probabilidad de mutacion
def genetico(nIndGen,nGen,pMut):
    generacion = primeraGen(nIndGen,cPrevioMaq)
    while nGen > 0: 
        generacion.sort(key = fitness)
        print(generacion[0], fitness(generacion[0]))
        generacion = descarte(generacion)
        children = []
        while len(children) + len(generacion) < nIndGen:
            parent1, parent2 = seleccion(generacion)
            child1, child2 = cruce(parent1,parent2)
            child1 = mutacion(child1, cPrevioMaq, pMut)
            child2 = mutacion(child2, cPrevioMaq, pMut)
            children.append(child1)
            children.append(child2)
        generacion = generacion + children
        nGen = nGen - 1
    print(fitness(generacion[0]))

genetico(50,200,0.1)