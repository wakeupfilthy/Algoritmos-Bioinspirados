#Hernández Testa Angel Israel 5BV1
#Práctica de Inteligencia de Enjambre
#Realizar la minimización de la función x^2+y^2 +(25 * (senx + seny)
#en el intervalo de valores (-5,5) para x y y.
#Versión de PSO: Global
#Número de partículas: 20
#Iteraciones: 50
#a= 0.8    (inercia)
#b1= 0.7  (aprendizaje local)
#b2 = 1    (aprendizaje global)

import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib import animation

#Esta función es la que se va a minimizar x^2+y^2 +(25 * (senx + seny))
def fitness_function(x, y):
    z = (x**2 + y**2 + 25*(np.sin(x)+np.sin(y)))
    return z
#Esta función actualiza la velocidad de las partículas
def update_velocity(particle, velocity, pbest, gbest, a, b1, b2):
    num_particles = len(particle) #Establece las veces que se va a repetir el ciclo, basado en la dimensión de la partícula en este caso (x,y)
    new_velocity = np.array([0.0 for i in range(num_particles)]) #Crea un arreglo con la dimensión de la partícula
    r1 = random.uniform(0,1) #Genera un número aleatorio entre 0 y 1
    r2 = random.uniform(0,1)
    #Actualiza la velocidad de la partícula basado en la fórmula de PSO global, para cada dimensión de la partícula
    for i in range(0, num_particles):
        new_velocity[i] = (a * velocity[i]) + (b1 * r1 * (pbest[i] - particle[i])) + (b2 * r2 * (gbest[i] - particle[i]))
    return new_velocity
#Esta función actualiza la posición de las partículas
def update_position(particle, velocity):
    new_particle = particle + velocity
    return new_particle
#Esta función es la que realiza el algoritmo de PSO
def pso(population, dimension, position_min, position_max, generation, a, b1, b2, ax, images):
    #Crea la población de partículas con valores aleatorios en el intervalo de valores (-5,5) para x y y
    particles = [[random.uniform(position_min, position_max) for j in range(dimension)] for i in range(population)]
    #La posición inicial es la mejor
    pbest_position = particles
    #Fitness de la posición inicial evaluada en la función de minimización
    pbest_fitness = [fitness_function(p[0],p[1]) for p in particles]
    #Se obtiene el índice de la mejor partícula que es la que tiene el menor fitness
    gbest_index = np.argmin(pbest_fitness)
    #Se obtiene la posición de la mejor partícula
    gbest_position = pbest_position[gbest_index]
    #Se crea el vector de velocidades
    velocity = [[0.0 for j in range(dimension)] for i in range(population)]

    #Ciclo que realiza el algoritmo de PSO
    for t in range(generation):
        for n in range(population):
            #Actualiza la velocidad de las partículas
            velocity[n] = update_velocity(particles[n], velocity[n], pbest_position[n], gbest_position, a, b1, b2)
            #Actualiza la posición de las partículas
            particles[n] = update_position(particles[n], velocity[n])
            #Es para visualizar la animación de el movimiento de las partículas en cada iteración
            image = ax.scatter3D([
                          particles[n][0] for n in range(population)],
                         [particles[n][1] for n in range(population)],
                         [fitness_function(particles[n][0],particles[n][1]) for n in range(population)], c='r')
            gen_text = ax.text2D(0.05, 0.95, 'Generation: {}'.format(t), transform=ax.transAxes)
            images.append([image, gen_text])
            print('Particle position: ', particles[n])
            print('Velocity: ', velocity[n])
            print('pbest: ', pbest_position[n])


        #Calcula el fitness de la posición de las partículas
        pbest_fitness = [fitness_function(p[0],p[1]) for p in particles]
        #Actualiza la mejor posición de las partículas
        gbest_index = np.argmin(pbest_fitness)
        gbest_position = pbest_position[gbest_index]

        print('Global Best Position: ', gbest_position)
        print('Best Fitness Value: ', min(pbest_fitness))
        print('Average Particle Best Fitness Value: ', np.average(pbest_fitness))
        print('Number of Generation: ', t)
        print('===============================================')


population = 20 
min_position = -5
max_position = 5
generations = 50
a = 0.8 #inercia
b1 = 0.7 #aprendizaje local
b2 = 1 #aprendizaje global

#Realiza la animación de la función de minimización
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

x = np.linspace(min_position, max_position, 80)
y = np.linspace(min_position, max_position, 80)
X, Y = np.meshgrid(x, y)
Z= fitness_function(X,Y)
ax.plot_wireframe(X, Y, Z, color='green', linewidth=0.2)

#Crea una lista vacía para guardar las imágenes de la animación
images = []

#Llama a la función de PSO
pso(population, 2, min_position, max_position, generations, a, b1, b2, ax, images)
animated_image = animation.ArtistAnimation(fig, images)
#Para guardar la animación
#animated_image.save('pso_simple.gif', writer='pillow')
plt.show()