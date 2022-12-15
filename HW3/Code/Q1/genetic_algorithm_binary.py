# genetic algorithm binary
# genetic algorithm
# 1. generate a population of random solutions
# 2. evaluate the fitness of each solution
# 3. repeat until a solution is found
# 3.1 select two parents
# 3.2 crossover
# 3.3 mutate
# 3.4 evaluate fitness
# 4. return the best solution found

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


# import data from csv file for cost function
data = pd.read_csv('data.csv', header=None)
data = data.to_numpy()
global x, y
x = data[0, :]
y = data[1, :]

# function to be optimized
def target_function(answer):
    global x, y
    y_ans =  answer[0]*x**3 + answer[1]*x**2 + answer[2]*x + answer[3]*np.sin(answer[4]*x) + answer[5]*np.cos(answer[6]*x)
    return np.sum((y_ans - y)**2)

def y_ans(answer):
    global x
    return answer[0]*x**3 + answer[1]*x**2 + answer[2]*x + answer[3]*np.sin(answer[4]*x) + answer[5]*np.cos(answer[6]*x)

# generate random numbers in the range [0, 1]
def random_number():
    return random.random()  # random.random() generates a random number in the range [0, 1]

# generate random integer in the range [0, n]
def random_int(n):
    return random.randint(0, n)  # random.randint(a, b) generates a random integer in the range [a, b]



# convert a bit string to a real number in the range [lower, upper]
def bitstring_to_real(bitstring):
    answer = np.zeros(int(len(bitstring)/9), dtype=float)
    for i in range(len(bitstring)):
        if i % 9 == 0:
            answer[int(i/9)] = 2**4* bitstring[i] + 2**3* bitstring[i+1] + 2**2* bitstring[i+2] + 2**1* bitstring[i+3] + 2**0* bitstring[i+4] + 2**-1* bitstring[i+5] + 2**-2* bitstring[i+6] + 2**-3* bitstring[i+7] + 2**-4* bitstring[i+8]
    return answer

# create an initial population of random bit strings
def initial_population(pop_size, bitstring_length):
    return np.random.randint(2, size=(pop_size,bitstring_length))



# calculate the fitness of a bit string, higher is better
def fitness(bitstring):
    x = bitstring_to_real(bitstring)
    y = target_function(x)
    return y

# mating Double Tournament Selection without replacing
def selection(population, tournament_size):
    selected_population = np.random.randint(len(population), size=tournament_size, dtype=int)
    min_cost = math.inf
    max_cost = -math.inf
    for i in range(tournament_size):
        if fitness(population[selected_population[i]]) < min_cost:
            min_cost = fitness(population[selected_population[i]])
            min_index = selected_population[i]
        if fitness(population[selected_population[i]]) > max_cost:
            max_cost = fitness(population[selected_population[i]])
            max_index = selected_population[i]
    return population[min_index], population[max_index] # return the best and the worst for parent and dead

# perform uniform crossover of two parents to create two children
def crossover(parent1, parent2):
    child1 = np.zeros(len(parent1), dtype=int)
    child2 = child1.copy()
    for i in range(len(parent1)):
        if random_number() < 0.5:
            child1[i] = parent1[i]
            child2[i] = parent2[i]
        else:
            child1[i] = parent2[i]
            child2[i] = parent1[i]
    return child1, child2


# mutate an individual
def mutation(bitstring, mutation_rate):
    if random_number() < mutation_rate:
        mutation_index = random_int(len(bitstring))
        if mutation_index >= len(bitstring):
            mutation_index = len(bitstring) - 1
        bitstring[mutation_index] = random_int(2)
        print('mutation')
    return bitstring


# genetic algorithm
def genetic_algorithm(pop_size, bitstring_length, mutation_rate, generations, tournament_size):
    # initialize population
    population = initial_population(pop_size, bitstring_length)
    # evaluate fitness
    # ranked_population = rank_by_fitness(population, lower, upper)
    # run the algorithm for the given number of generations
    for i in range(generations):
        print('Generation: ', i)
        # select parents
        parent1, dead1 = selection(population, tournament_size)
        parent2, dead2 = selection(population, tournament_size)
        # crossover parents
        children = crossover(parent1, parent2)
        child1 = children[0]
        child2 = children[1]
        # mutate children
        child1 = mutation(child1, mutation_rate)
        child2 = mutation(child2, mutation_rate)
        # if (parent1 == parent2).all():
        #     print('parent1 == parent2')
            # continue
        # evaluate fitness
        for i in range(len(population)):
            if (population[i] == dead1).all():
                population[i] = np.copy(child1)
                break
        for i in range(len(population)):
            if (population[i] == dead2).all():
                population[i] = np.copy(child2)
                # print('replaced', i)
                break
        
        # print(population)
    best_sol = np.zeros(len(population[0]), dtype=int)
    best_cost = math.inf
    for i in population:
        if fitness(i) < best_cost:
            best_cost = fitness(i)
            best_sol = i
    return best_sol, population

# run the algorithm
if __name__ == '__main__':
    # problem configuration
    bitstring_length = int(9*7) # 7 parameters and 9 bits for each parameter
    # algorithm configuration
    pop_size = 20
    mutation_rate = 0.5
    generations = 10000
    tournament_size = 8
    # execute the algorithm
    best, population = genetic_algorithm(pop_size, bitstring_length, mutation_rate, generations, tournament_size)
    print("Done.")

print(best)

plt.rcParams['text.usetex'] = True
fig, ax = plt.subplots()

ax.plot(x, y, 'r', label='Data')
ax.plot(x, y_ans(bitstring_to_real(best)), 'b', label='Genetic Algorithm optimization')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend()
plt.show()



