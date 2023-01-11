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
    # Initialize the pbest and gbest
    pbest = x
    gbest = x[np.argmin(obj_func(x))]
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
                gbest = x[i]
                best_fitness = fitness[i]
        # Update the particle velocity
        w = 0.5
        c1 = 2
        c2 = 2
        v = w * v + c1 * np.random.uniform(0, 1, (n_particles, dim)) * (pbest - x) + c2 * np.random.uniform(0, 1, (n_particles, dim)) * (gbest - x)
        # Update the particle position
        x = x + v
        # Record the best fitness
        fitness_history[iter] = best_fitness
        # Display the iteration information
        print("Iteration: ", iter, " f(x)= ", best_fitness)
    return gbest, fitness_history

# Set the parameters
lb = -100
ub = 100
dim = 50
n_particles = 256
n_iter = 1000

# Run the PSO algorithm
gbest, fitness_history = PSO(obj_func, lb, ub, dim, n_particles, n_iter)

# Plot the convergence curve
plt.plot(fitness_history)
plt.xlabel("Iteration")
plt.ylabel("Fitness")
plt.show()

# Print the results
print("The best position is: ", gbest)
print("The best fitness value is: ", obj_func(gbest))


