#Hernández Testa Angel Israel 
#Práctica de optimización por colonia de abejas artificiales
#Realizar la minimización de la función x^2+y^2 +(25 * (senx + seny)
#en el intervalo de valores (-5,5) para x y y.
#Número de abejas obreras: 20
#Número de abejas observadoras: 20
#Límite: 5
#Iteraciones: 50

import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib import animation

#Esta función es la que se va a minimizar x^2+y^2 +(25 * (senx + seny))
def fitness_function(x, y):
    z = (x**2 + y**2 + 25*(np.sin(x)+np.sin(y)))
    return z
#Esta función obtiene la aptitud (fiteness) de cada individuo
def fitness_vectors(fitness):
    fitness_vector= np.array([0.0 for i in range(len(fitness))])
    for i in range(len(fitness)):
        if fitness[i] < 0: #Si f(i) es negativo, se usa la función de aptitud 1+|fitness|
            fitness_vector[i] = 1+abs(fitness[i])
        else: #Si f(i) es positivo, se usa la función de aptitud 1/(1+fitness)
            fitness_vector[i] = 1/(1+fitness[i])
    return fitness_vector
#Esta función actualiza la posición de las abejas obreras con la fórmula de ABC 
def actualizar_obreras(obreras, dominio):
    nuevas_obreras = np.copy(obreras)
    for i in range(len(obreras)):
        # Seleccionar aleatoriamente otra abeja
        k = random.choice([j for j in range(len(obreras)) if j != i]) 
        # Generar un número aleatorio entre -1 y 1
        r2= random.uniform(-1,1)
        # Actualizar la posición de la abeja
        nuevas_obreras[i] = obreras[i] + r2 * (obreras[i] - obreras[k])
        # Si la posición de la nueva abeja se sale del dominio, se regresa al límite
        for j in range(len(dominio)):
            if nuevas_obreras[i][j] < dominio[j][0]:
                nuevas_obreras[i][j] = dominio[j][0]
            if nuevas_obreras[i][j] > dominio[j][1]:
                nuevas_obreras[i][j] = dominio[j][1]
    #se actualiza el fitness de las nuevas abejas obreras
    new_fitness_obreras = np.array([fitness_function(x[0], x[1]) for x in nuevas_obreras])
    new_fitness_vector= fitness_vectors(new_fitness_obreras)
    return nuevas_obreras, new_fitness_vector, new_fitness_obreras
#Esta función selecciona una abeja obrera con la ruleta
def rouletteWheel(values):
    total = sum(values)  # Suma de todos los valores de fitness
    # Se genera un número aleatorio entre 0 y la suma de los valores de fitness (la flecha de la ruleta)
    pick = random.uniform(0, total)
    current = 0
    for index, value in enumerate(values):
        current += value  # Se va sumando el valor de fitness de cada individuo
        if current > pick:  # Si la suma de los valores de fitness es mayor que el número aleatorio, se selecciona ese individuo
            return index
#Esta función envía a las abejas observadoras
def seleccion_observadoras(n_observadoras, obreras, fitness_vector, dominio):
    observadoras = np.copy(obreras)
    seleccion= np.array([0.0 for i in range(n_observadoras)])
    for i in range(n_observadoras):
        # Seleccionar una abeja obrera con la ruleta
        k = rouletteWheel(fitness_vector)
        print("abeja seleccionada: ", k)
        seleccion[i]=k #Se guarda el índice de la abeja seleccionada
        # Seleccionar aleatoriamente otra abeja
        j = random.choice([j for j in range(len(obreras)) if j != k])
        r2 = random.uniform(-1, 1)
        # Actualizar la posición de la abeja
        observadoras[i] = obreras[k] + r2 * (obreras[k] - obreras[j])
        # Si la posición de la nueva abeja se sale del dominio, se regresa al límite
        for j in range(len(dominio)):
            if observadoras[i][j] < dominio[j][0]:
                observadoras[i][j] = dominio[j][0]
            if observadoras[i][j] > dominio[j][1]:
                observadoras[i][j] = dominio[j][1]
        #se actualiza el fitness de las nuevas abejas observadoras
        fitness_observadoras = np.array([fitness_function(x[0], x[1]) for x in observadoras])
        fitness_vector_observadoras = fitness_vectors(fitness_observadoras)
    return observadoras, fitness_vector_observadoras, fitness_observadoras, seleccion
#Esta función realiza el algoritmo de colonia de abejas artificiales
def ABC_optimization(n_obreras, n_observadoras, dominio, limite, iteraciones, ax, images):
    #Inicialización de las abejas obreras con valores aleatorios en el intervalo de valores (-5,5) para x y y
    obreras= np.random.uniform(dominio[:, 0], dominio[:, 1], (n_obreras, dominio.shape[0]))
    print("Abejas obreras: \n", obreras)
    fitness_obreras = np.array([fitness_function(x[0], x[1]) for x in obreras])
    print("Soluciones de las abejas obreras: \n", fitness_obreras)
    X_best = obreras[np.argmin(fitness_obreras)]
    print("Mejor abeja obrera: \n", X_best)
    fitness_vector= fitness_vectors(fitness_obreras)
    print("Vector de fitness: \n", fitness_vector)
    print("-----------------------------")
    for t in range(iteraciones):
        print("iteración: ", t+1)
        #Se actualizan las abejas obreras
        nuevas_obreras, new_fitness_vector, new_fitness_obreras = actualizar_obreras(obreras, dominio)
        print(nuevas_obreras)
        print(new_fitness_vector)
        print(new_fitness_obreras)
        for i in range (n_obreras):
            if new_fitness_vector[i] > fitness_vector[i]: #Si el fitness de la nueva abeja es mayor que el de la abeja obrera, se actualiza
                intentos[i]=0
                fitness_vector[i]=new_fitness_vector[i]
                fitness_obreras[i]=new_fitness_obreras[i]
                for j in range(dimension):
                    obreras[i][j]=nuevas_obreras[i][j]
            else:
                intentos[i]+=1 #Si el fitness de la nueva abeja es menor que el de la abeja obrera, se aumenta el contador de intentos
                if intentos[i]>=limite: #Si el contador de intentos es mayor o igual al límite, abandona la fuente de alimento
                    obreras[i] = np.random.uniform(dominio[:, 0], dominio[:, 1])
                    fitness_obreras[i]=fitness_function(obreras[i][0], obreras[i][1])
                    fitness_vector=fitness_vectors(fitness_obreras)
                    intentos[i]=0
        print("obreras actualizadas: \n", obreras)
        print("evaluación de soluciones: \n", fitness_obreras)
        print("vector de fitness actualizado: \n", fitness_vector)
        #Se envían las abejas observadoras
        observadoras, fitness_vector_observadoras, fitness_observadoras, seleccion = seleccion_observadoras(n_observadoras, obreras, fitness_vector, dominio)
        print("observadoras: \n", observadoras)
        print("fitness de las observadoras: \n", fitness_vector_observadoras)
        print("evaluación de las observadoras: \n", fitness_observadoras)
        for i in range(n_observadoras):
            if fitness_vector_observadoras[i]>fitness_vector[int(seleccion[i])]: #Si la abeja exploradora encuentra una mejor solución que el de la abeja obrera, se actualiza
                obreras[int(seleccion[i])]=observadoras[i] #Se actualizan los valores de las abejas obreras
                fitness_obreras[int(seleccion[i])]=fitness_observadoras[i]
                fitness_vector[int(seleccion[i])]=fitness_vector_observadoras[i]
                intentos[int(seleccion[i])]=0
        print("obreras actualizadas: \n", obreras)
        print("vector de fitness actualizado: \n", fitness_vector)
        print("evaluación de soluciones: \n", fitness_obreras)
        X_best=obreras[np.argmin(fitness_obreras)]
        print("mejor abeja obrera: ", X_best[0], X_best[1])
        print("evaluación de la mejor abeja obrera: ", fitness_function(X_best[0], X_best[1]))
        print("vector de intentos: ", intentos)
        print("-----------------------------\n")
        #Es para visualizar la animación de el movimiento de las abejas en cada iteración
        image = ax.scatter3D([obreras[n][0] for n in range(n_obreras)] + [observadoras[n][0] for n in range(n_observadoras)],
                             [obreras[n][1] for n in range(n_obreras)] + [observadoras[n][1] for n in range(n_observadoras)],
                             [fitness_function(obreras[n][0],obreras[n][1]) for n in range(n_obreras)]+ 
                             [fitness_function(observadoras[n][0], observadoras[n][1]) for n in range(n_observadoras)], c=['r'] * n_obreras + ['b'] * n_observadoras)
        gen_text = ax.text2D(0.05, 0.95, 'Iteración: {} \nobreras = rojo\nobservadoras = azul'.format(t+1), transform=ax.transAxes)
        images.append([image, gen_text])

n_obreras = 20
n_observadoras = 20
dimension=2
dominio = np.array([[-5, 5],
                    [-5, 5]])
limite = 5
intentos = np.array([0.0 for i in range(n_obreras)])
iteraciones = 50
#Realiza la animación de la función de minimización
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

x = np.linspace(dominio[0][0], dominio[0][1], 80)
y = np.linspace(dominio[1][0], dominio[1][1], 80)
X, Y = np.meshgrid(x, y)
Z= fitness_function(X,Y)
ax.plot_wireframe(X, Y, Z, color='green', linewidth=0.2)

#Crea una lista vacía para guardar las imágenes de la animación
images = []

ABC_optimization(n_obreras, n_observadoras, dominio, limite, iteraciones, ax, images)
animated_image = animation.ArtistAnimation(fig, images, interval=800, repeat=True)
#Para guardar la animación
#animated_image.save('abc_animation.gif', writer='pillow')
plt.show()