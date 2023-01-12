## PSO optimization algorithm
import numpy as np
import matplotlib.pyplot as plt
import random
import math

# Define the objective function
def obj_func(x):
    ans = 0
    for i in range(len(x)):
        ans += sum(x[0:i+1])**2
    return ans * (1 + random.random()) - 450

# Define the PSO algorithm
def PSO(obj_func, lb, ub, dim, n_particles, n_iter):
    # Initialize the particle position
    x = np.random.uniform(lb, ub, (n_particles, dim))
    # Initialize the particle velocity
    v = np.random.uniform(-1, 1, (n_particles, dim))
    # Initialize the v for output
    v_array = np.empty((n_iter, 1))
    # Initialize the pbest and gbest
    global_best = [np.argmin(obj_func(x))]
    pbest = x
    # Initialize the particle fitness
    fitness = np.full(n_particles, float("inf"))
    # Initialize the best fitness value
    best_fitness = float("inf")
    # Initialize the fitness history
    fitness_history = np.empty((n_iter, 1))
    # Iteration
    for iter in range(n_iter):
        for i in range(n_particles):
            # Calculate the fitness
            fitness[i] = obj_func(x[i])
            # Update the pbest
            if fitness[i] < obj_func(pbest[i]):
                pbest[i] = x[i]
            # Update the gbest
            if fitness[i] < best_fitness:
                global_best = fitness[i]
                best_fitness = fitness[i]

        # Update the gbest with ring topology
        gbest = np.empty((n_particles, dim))
        
        for i in range(n_particles):
            if fitness[i] < fitness[(i-1)%n_particles] and fitness[i] < fitness[(i+1)%n_particles]:
                gbest[i] = x[i]
            elif fitness[(i-1)%n_particles] < fitness[i] and fitness[(i-1)%n_particles] < fitness[(i+1)%n_particles]:
                gbest[i] = x[(i-1)%n_particles]
            else:
                gbest[i] = x[(i+1)%n_particles]
        # Update the particle velocity
        w = 0.5
        c1 = 2
        c2 = 2
        v = w * v + c1 * np.random.uniform(0, 1, (n_particles, dim)) * (pbest - x) + c2 * np.random.uniform(0, 1, (n_particles, dim)) * (gbest - x)
        # Update the v for output
        v_array[iter] = sum(sum(v))
        # Update the particle position
        x = x + v
        # Record the best fitness
        fitness_history[iter] = best_fitness
        # Display the iteration information
        print("Iteration: ", iter, " f(x)= ", best_fitness)
    return global_best, fitness_history, v_array

# Set the parameters
lb = -100
ub = 100
dim = 10
n_particles = 80
n_iter = 1000

# Run the PSO algorithm
gbest, fitness_history, v_array = PSO(obj_func, lb, ub, dim, n_particles, n_iter)

# Plot the convergence curve
csfont = {'fontname':'Times New Roman'}
plt.plot(fitness_history)
plt.xlabel("Iteration",**csfont,fontsize=24)
plt.ylabel("Fitness",**csfont,fontsize=24)
fig = plt.gcf()
fig.set_size_inches(8.5, 5.5, forward=True)

plt.savefig('../../Figure/Q1/PSO_II_convergence_curve.eps', format='eps', dpi=1000)
plt.close()


csfont = {'fontname':'Times New Roman'}
plt.plot(v_array)
plt.xlabel("Iteration",**csfont,fontsize=24)
plt.ylabel("Inertia Weight",**csfont,fontsize=24)
fig = plt.gcf()
fig.set_size_inches(8.5, 5.5, forward=True)
plt.savefig('../../Figure/Q1/PSO_II_inertia_weight.eps', format='eps', dpi=1000)
