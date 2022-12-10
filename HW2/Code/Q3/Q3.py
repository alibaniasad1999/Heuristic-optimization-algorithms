import numpy as np
import random
import math
import pandas as pd
def cost_calculator(city_array):
    num = 0
    list_city = [[], [], []]
    # seperate the city_array into 3 lists
    for i in city_array:
        if i != -1:
            list_city[num].append(i)
        else:
            num += 1
    # calculate the cost of each list
    location = np.array([[-19, 25, -40, 2 ,  21, -21, 41, -25, 33,  44],
                [-5 ,-40, -24, 47, -19,  35, 13, -42,  8, -44]])
    new_location = np.empty((10, 2))
    origin = np.array([0, 0])
    for i in range(len(location[0])):
        new_location[i] = location[:, i]
    
    cost = np.zeros(3)

    for i in list_city:
        for j in range(len(i)):
            if j == 0:
                cost[list_city.index(i)] += np.linalg.norm(new_location[i[j]] - origin)
            else:
                cost[list_city.index(i)] += np.linalg.norm(new_location[i[j]] - new_location[i[j-1]])

    return max(cost)

def swap_random(city_list, num):
    if num == 2:
        idx = range(len(city_list))
        i1, i2 = random.sample(idx, 2)
        city_list[i1], city_list[i2] = city_list[i2], city_list[i1]
    elif num == 3:
        idx = range(len(city_list))
        i1, i2, i3 = random.sample(idx, 3)
        city_list[i1], city_list[i2], city_list[i3] = city_list[i2], city_list[i3], city_list[i1]
    else:
        idx = range(len(city_list))
        i1, i2, i3, i4 = random.sample(idx, 4)
        city_list[i1], city_list[i2], city_list[i3], city_list[i4] = city_list[i2], city_list[i3], city_list[i4], city_list[i1]


def simulated_annealing(city_list, cost, T, alpha, epsion):
    swap_range=1000
    counter = 0
    min_num = 0
    city_list_final = np.copy(city_list)
    while T > epsion:
        for i in range(10):
            counter += 1
            if swap_range < 2:
                swap_range = 2
            city_list = np.copy(city_list_final)
            swap_random(city_list, int(swap_range))
            new_cost = cost_calculator(city_list)
            if new_cost < cost:
                cost = np.copy(new_cost)
                city_list_final = np.copy(city_list)
                min_num = counter
            else:
                if np.exp((cost - new_cost) / T) > random.random():
                    cost = np.copy(new_cost)
                    city_list_final = np.copy(city_list)
                    min_num = counter
        T *= alpha
        swap_range = alpha*swap_range
        # print(T, swap_range, new_cost, city_list)
    return city_list_final, cost, min_num


city_list = np.append([np.linspace(0, 9, 10, dtype=int)], [-1, -1]) # city_list is a list of city index
np.random.shuffle(city_list)

# city_list, cost, min_num = simulated_annealing(city_list, math.inf, 1000, 0.99, 1)

# print(city_list, cost)

        

T_0   = np.random.uniform(low=1e2 , high=1e8  , size=(2))
T_f   = np.random.uniform(low=1e-4, high=1e0  , size=(2))
alpha = np.random.uniform(low=0.9 , high=0.999, size=(2))
random_sampling = np.array([T_0, T_f, alpha])

result = np.zeros((2, 200))
direction_result = np.zeros((200, 12))

for i in range(len(random_sampling[0])):
    city_list = np.append([np.linspace(0, 9, 10, dtype=int)], [-1, -1]) # city_list is a list of city index
    np.random.shuffle(city_list)
    city_list, cost, min_num = simulated_annealing(city_list, math.inf, random_sampling[0][i], random_sampling[2][i], random_sampling[1][i])
    print(city_list, cost)
    result[0][i] = cost
    result[1][i] = min_num
    direction_result[i] = city_list

pd.DataFrame(result).to_csv("data.csv", header=None)
pd.DataFrame(direction_result).to_csv("direction.csv", header=None)
pd.DataFrame(random_sampling).to_csv("random_sampling.csv", header=None)