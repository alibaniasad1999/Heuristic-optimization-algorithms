import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Ant Colony Optimization
# Part II - ACO for the Traveling Salesman Problem with traffic

# Importing the dataset
dataset = pd.read_csv('pos.csv', header = None)
X = dataset.iloc[:, [0, 1]].values

# Visualising the cities
plt.scatter(X[:,0], X[:,1], s = 100, color = 'red')
plt.title('Cities')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

# Importing the traffic
dataset = pd.read_csv('traffic.csv', header = None)
traffic = dataset.iloc[:, :].values

# Creating the graph
def create_graph(X, traffic):
    graph = np.zeros((len(X), len(X)))
    for i in range(len(X)):
        for j in range(len(X)):
            graph[i,j] = np.sqrt((X[i,0] - X[j,0])**2 + (X[i,1] - X[j,1])**2) / traffic[i,j]
    return graph

graph = create_graph(X, traffic)

# Implementing ACO
def ACO(graph, n_ants, n_iterations, alpha, beta, rho, Q):
    n_cities = len(graph)
    # Initialize pheromone
    pheromone = np.ones((n_cities, n_cities))
    # Initialize best length
    best_length = np.inf
    # Initialize best solution
    best_solution = []
    # ACO main loop
    for i in range(n_iterations):
        # Initialize ants
        ants = []
        for j in range(n_ants):
            # Initialize empty tour
            tour = []
            # Randomly select first city in tour
            current_city = np.random.randint(0, n_cities)
            # Add city to tour
            tour.append(current_city)
            # Initialize tabu list
            tabu_list = []
            tabu_list.append(current_city)
            # Tour construction
            while len(tour) < n_cities:
                # Initialize probabilities
                p = np.zeros(n_cities)
                for k in range(n_cities):
                    if k not in tabu_list:
                        p[k] = (pheromone[current_city, k]**alpha) * ((1.0/graph[current_city, k])**beta)
                # Select next city
                next_city = np.random.choice(n_cities, 1, p = p/p.sum())[0]
                # Add city to tour
                tour.append(next_city)
                # Add city to tabu list
                tabu_list.append(next_city)
                # Update current city
                current_city = next_city
            # Add tour to ants
            ants.append(tour)
        # Update pheromone
        # Initialize pheromone_delta
        pheromone_delta = np.zeros((n_cities, n_cities))
        # Calculate pheromone_delta for each ant
        for j in range(n_ants):
            # Calculate tour length
            tour_length = 0
            for k in range(n_cities):
                tour_length += graph[ants[j][k], ants[j][(k+1)%n_cities]]
            # Update pheromone_delta
            for k in range(n_cities):
                pheromone_delta[ants[j][k], ants[j][(k+1)%n_cities]] += Q/tour_length
        # Update pheromone
        pheromone = (1-rho)*pheromone + pheromone_delta
        # Update best solution found so far
        for j in range(n_ants):
            # Calculate tour length
            tour_length = 0
            for k in range(n_cities):
                tour_length += graph[ants[j][k], ants[j][(k+1)%n_cities]]
            if tour_length < best_length:
                best_length = tour_length
                best_solution = ants[j]
    return best_solution, best_length

best_solution, best_length = ACO(graph, n_ants = 10, n_iterations = 1000, alpha = 1.0, beta = 5.0, rho = 0.5, Q = 100)

# Visualising the results
def plot_solution(X, best_solution):
    plt.scatter(X[:,0], X[:,1], s = 100, color = 'red')
    plt.plot(X[best_solution,0], X[best_solution,1], color = 'blue', alpha = 0.7)
    plt.title('Best solution found')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

plot_solution(X, best_solution)