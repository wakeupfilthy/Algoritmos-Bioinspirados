# Angel Israel Hernández Testa
#Solución al problema de las N reinas con algoritmos genéticos

import numpy as np 
import random

def get_diagonal(posicion, numero, number_of_queens):
    return posicion+numero, posicion-numero+(number_of_queens-1)

def genGenerator(size):
    Gen = np.random.randint(0, size, size)
    return Gen

def get_attacks(diagonal, diagonal_inv, columna):
    # Crear máscaras booleanas para los elementos mayores que uno
    mascara_diagonal = (diagonal > 1)
    mascara_diagonal_inv = (diagonal_inv > 1)
    mascara_columna = (columna > 1)

    # Aplicar las máscaras y sumar los elementos correspondientes
    attacks = np.sum(diagonal[mascara_diagonal]-1) + \
            np.sum(diagonal_inv[mascara_diagonal_inv]-1) + \
            np.sum(columna[mascara_columna]-1)
    return attacks

def evaluate(Gen, number_of_queens):
    diagonal = np.array([0]*(len(Gen)*2-1))
    diagonal_inv = np.array([0]*(len(Gen)*2-1))
    columna = np.array([0]*len(Gen))
    #Se colocan las reinas en el tablero
    for i in range(len(Gen)):
        diag, diag_inv = get_diagonal(Gen[i], i, number_of_queens)
        diagonal[diag] += 1
        diagonal_inv[diag_inv] += 1
        columna[Gen[i]] += 1
    attacks = get_attacks(diagonal, diagonal_inv, columna)
    return attacks

def calculate_fitness(attacks):
    return 1/(1+attacks)

def rouletteWheel(values, population_size):
    new_values = np.array([0.0 for i in range(len(values))])
    for i in range(len(values)):
        new_values[i] = population_size*(values[i]**5)
    total = sum(new_values)  # Suma de todos los valores de fitness
    # Se genera un número aleatorio entre 0 y la suma de los valores de fitness (la flecha de la ruleta)
    pick = random.uniform(0, total)
    current = 0
    for i,value in enumerate(new_values):
        current += value  # Se va sumando el valor de fitness de cada individuo
        if current > pick:  # Si la suma de los valores de fitness es mayor que el número aleatorio, se selecciona ese individuo
            return i

def unicross(Padre1, Padre2):
    # Se genera una lista de números aleatorios entre 0 y 1
    Aleatoria = [random.choice([0, 1]) for _ in Padre1]
    #print("Vector de cruza aleatoria:\n",Aleatoria)
    Hijo1 = np.array([0]*len(Padre1))
    Hijo2 = np.array([0]*len(Padre2))
    for i in range(len(Padre1)):
        if Aleatoria[i] == 1:  # Si el número aleatorio es 1, se intercambian los genes de los padres
            Hijo1[i] = Padre1[i]
            Hijo2[i] = Padre2[i]
        else:
            Hijo1[i] = Padre2[i]
            Hijo2[i] = Padre1[i]
    return Hijo1, Hijo2

def pointcrossover(Padre1, Padre2):
    crosspoint = np.random.randint(0, len(Padre1))
    #print("Punto de cruza:\n",crosspoint)
    Hijo1 = np.array([0]*len(Padre1))
    Hijo2 = np.array([0]*len(Padre2))
    for i in range(len(Padre1)):
        if i < crosspoint:
            Hijo1[i] = Padre1[i]
            Hijo2[i] = Padre2[i]
        else:
            Hijo1[i] = Padre2[i]
            Hijo2[i] = Padre1[i]
    return Hijo1, Hijo2

def mutation(Gen, number_of_queens):
    # Se genera una lista de números aleatorios entre 0 y 100
    aleatorio = np.random.randint(0, 101, len(Gen))
    for i in range(len(Gen)):
        if aleatorio[i] <= 15:  # Si el número aleatorio es menor que 10, se realiza la mutación
            # Se genera un nuevo gen aleatorio
            Gen[i] = np.random.randint(0, number_of_queens)
    return Gen

def parentselection(Population, fitness, number_of_queens, population_size):
    # Se genera un número aleatorio entre 0 y 100 para determinar si se realiza el cruce
    crossprobab = random.uniform(0, 100)
    i = rouletteWheel(fitness, population_size)  # Se selecciona el primer padre
    j = rouletteWheel(fitness, population_size)  # Se selecciona el segundo padre
    parent1 = Population[i]
    parent2 = Population[j]
    #print("Padre 1:\n",parent1)
    #print("Padre 2:\n",parent2)
    Hijo1 = np.array([0]*number_of_queens)
    Hijo2 = np.array([0]*number_of_queens)
    #print("Probabilidad de cruce:\n",crossprobab)
    if crossprobab <= 85:  # Si el número aleatorio es menor que 85, se realiza el cruce
        Hijo1, Hijo2 = unicross(parent1, parent2)
        mutation(Hijo1, number_of_queens)  # Se realiza la mutación
        mutation(Hijo2, number_of_queens)
        #print("Hijo 1:\n",Hijo1)
        #print("Hijo 2:\n",Hijo2)
        #print("Fitness H1:\n",calculate_fitness(evaluate(Hijo1, number_of_queens)))
        #print("Fitness H2:\n",calculate_fitness(evaluate(Hijo2, number_of_queens)))
        # Se evalua que el hijo tenga mayor fitness que el padre
        if (calculate_fitness(evaluate(Hijo1, number_of_queens)) > fitness[i]):
            Population[i] = Hijo1  # Se actualiza la población
        else:
            # Si el hijo no tiene mayor fitness que el padre, se actualiza la población con el padre
            Population[i] = parent1
        if (calculate_fitness(evaluate(Hijo2, number_of_queens)) > fitness[j]):
            Population[j] = Hijo2
        else:
            Population[j] = parent2

        return Population
    else:  # Si el número aleatorio es mayor que 85, no se realiza el cruce
        return Population

number_of_queens = 6
population_size=300
generations=0
solution_found = False
#Inicialización de la población
Population = np.array([genGenerator(number_of_queens) for _ in range(population_size)])
print("Población inicial:\n",Population)
#Evaluación de la población
attacks = np.array([evaluate(x, number_of_queens) for x in Population])
print("Vector de ataques:\n",attacks)
#Cálculo del fitness
fitness = np.array([calculate_fitness(x) for x in attacks])
print("vector de fitness:\n",fitness)
while not solution_found:
    #Selección de padres
    Population = parentselection(Population, fitness, number_of_queens, population_size)
    #print("Población:\n",Population)
    #Evaluación de la población
    attacks = np.array([evaluate(x, number_of_queens) for x in Population])
    #print("Vector de ataques:\n",attacks)
    #Cálculo del fitness
    fitness = np.array([calculate_fitness(x) for x in attacks])
    #print("Vector de fitness:\n",fitness)
    generations += 1
    print("Generaciones:\n",generations)
    #print("-----------------------------------------------------")
    if 0 in attacks:
        solution_found = True
solucion = Population[np.argmin(attacks)]
print("Población final:\n",Population)
print("Vector de ataques:\n",attacks)
print("Vector de fitness:\n",fitness)
print("Generaciones:\n",generations)
print("Solución:\n",solucion)

