# Angel Israel Hernández Testa 2022630048, Algoritmos bioinspirados
# última modificación 17/10/2023
# -----------------------------------------------------------------------------------------------
# Descripción: Se realizará un algoritmo genético para resolver el problema de la mochila
# con 7 objetos de distintos valores y un peso máximo de 30.
# La población inicial será de 30 individuos, se realizarán 300 generaciones y se
# seleccionarán los padres mediante la ruleta, se realizará un cruce uniforme con una
# probabilidad del 85% y una mutación del 5%. Se usa el método de sustitución del padre más debil
import random

# Función para generar un individuo aleatorio


def genGenerator(Weight):
    Gen = [0]*len(Weight)
    # Genera un cromosoma aleatorio (el método .randrange() es uniforme )
    Gen = [random.randrange(0, 11) for _ in Weight]
    if Gen[1] < 3 or Gen[3] < 2:  # Se verifica que cumplan los requisitos del problema
        Gen[1] = random.randrange(3, 10)
        Gen[3] = random.randrange(2, 10)
    return Gen

# Esta función evalua que el individuo no supere el peso máximo


def evaluateGen(Weight, Gen, MaxWeight):
    W = 0
    for i in range(len(Weight)):
        W += Gen[i]*Weight[i]
    if W > MaxWeight:
        return False
    else:
        return True

# Esta función calcula el fitness de un individuo


def indivFitness(Price, Gen):
    P = 0
    for i in range(0, len(Price)):
        P += Gen[i]*Price[i]
    return P

# Esta función calcula el fitness de toda la población


def totalFitness(Price, Pop, P1):
    for i in range(0, len(Pop)):
        P1[i] = indivFitness(Price, Pop[i])
    return P1

# Esta función selecciona un individuo de la población mediante la ruleta (los individuos con mayor fitness tienen mayor probabilidad de ser seleccionados)


def rouletteWheel(values):
    total = sum(values)  # Suma de todos los valores de fitness
    # Se genera un número aleatorio entre 0 y la suma de los valores de fitness (la flecha de la ruleta)
    pick = random.uniform(0, total)
    current = 0
    for value in values:
        current += value  # Se va sumando el valor de fitness de cada individuo
        if current > pick:  # Si la suma de los valores de fitness es mayor que el número aleatorio, se selecciona ese individuo
            return values.index(value)

# Esta función selecciona los padres, realiza el cruce, la mutación y actualiza la población


def parentselection(Population, values, Weight, Price, MaxWeight):
    # Se genera un número aleatorio entre 0 y 100 para determinar si se realiza el cruce
    crossprobab = random.uniform(0, 100)
    i = rouletteWheel(values)  # Se selecciona el primer padre
    j = rouletteWheel(values)  # Se selecciona el segundo padre
    parent1 = Population[i]
    parent2 = Population[j]
    Hijo1 = [0]*len(parent1)
    Hijo2 = [0]*len(parent2)
    while parent1 == parent2:  # Se verifica que los padres sean distintos
        parent2 = Population[rouletteWheel(values)]
    if crossprobab <= 85:  # Si el número aleatorio es menor que 85, se realiza el cruce
        Hijo1, Hijo2 = unicross(parent1, parent2)
        mutation(Hijo1)  # Se realiza la mutación
        mutation(Hijo2)
        # Se evalua que el hijo no supere el peso máximo
        if (evaluateGen(Weight, Hijo1, MaxWeight) == True):
            # Se evalua que el hijo tenga mayor fitness que el padre
            if (indivFitness(Price, Hijo1) > indivFitness(Price, Population[i])):
                Population[i] = Hijo1  # Se actualiza la población
            else:
                # Si el hijo no tiene mayor fitness que el padre, se actualiza la población con el padre
                Population[i] = parent1
        else:
            # Si el hijo no cumple con el peso máximo, se actualiza la población con el padre
            Population[i] = parent1
        if (evaluateGen(Weight, Hijo2, MaxWeight) == True):
            if (indivFitness(Price, Hijo2) > indivFitness(Price, Population[j])):
                Population[j] = Hijo2
            else:
                Population[j] = parent2
        else:
            Population[j] = parent2

        return Population
    else:  # Si el número aleatorio es mayor que 85, no se realiza el cruce
        return Population

# Esta función realiza el cruce uniforme


def unicross(Padre1, Padre2):
    # Se genera una lista de números aleatorios entre 0 y 1
    Aleatoria = [random.choice([0, 1]) for _ in Padre1]
    Hijo1 = [0]*len(Padre1)
    Hijo2 = [0]*len(Padre2)
    for i in range(len(Padre1)):
        if Aleatoria[i] == 1:  # Si el número aleatorio es 1, se intercambian los genes de los padres
            Hijo1[i] = Padre1[i]
            Hijo2[i] = Padre2[i]
        else:
            Hijo1[i] = Padre2[i]
            Hijo2[i] = Padre1[i]
    return Hijo1, Hijo2

# Esta función realiza la mutación


def mutation(Gen):
    # Se genera una lista de números aleatorios entre 0 y 100
    aleatorio = [random.uniform(0, 100) for _ in Gen]
    for i in range(len(Gen)):
        if aleatorio[i] <= 10:  # Si el número aleatorio es menor que 10, se realiza la mutación
            # Se genera un nuevo gen aleatorio
            Gen[i] = random.randrange(0, 11)
            if Gen[1] < 3 or Gen[3] < 2:  # Se verifica que cumpla con los requisitos del problema
                Gen[1] = random.randrange(3, 11)
                Gen[3] = random.randrange(2, 11)
    return Gen


generations = 0  # Contador de generaciones
MaxWeight = 30  # Peso máximo de la mochila
Weight = [4, 2, 5, 5, 2, 1.5, 1]  # Peso de los objetos
Price = [10, 8, 12, 6, 3, 2, 2]  # Precio o valor
Population = [0]*30  # Tamaño de la población inicial
P1 = [0]*30  # Valor de las soluciones
for i in range(len(Population)):  # Se genera la población inicial
    Population[i] = genGenerator(Weight)
    while evaluateGen(Weight, Population[i], MaxWeight) == False:
        Population[i] = genGenerator(Weight)
print("Población inicial: ", Population)
P1 = totalFitness(Price, Population, P1)
print("fitness inicial de la población", P1)
# Se realizan 1000 generaciones
while generations < 1000:
    Population = parentselection(Population, P1, Weight, Price, MaxWeight)
    P1 = totalFitness(Price, Population, P1)
    print("Generación: ", generations)
    print("Fitness de la población: ", P1)
    print("Mejor solución: ", max(P1), "\n")
    generations += 1

print("Población Final: ", Population)
print("Fitness final de la población", P1)
print("Solución Final: ", Population[P1.index(
    max(P1))], "con un valor de: ", max(P1))
