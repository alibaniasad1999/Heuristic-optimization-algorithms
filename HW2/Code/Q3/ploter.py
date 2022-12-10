import numpy as np
import random
import math
import pandas as pd
import matplotlib.pyplot as plt
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
    T_array = []
    cost_array = []
    swap_range=1000
    counter = 0
    min_num = 0
    city_list_final = np.copy(city_list)
    while T > epsion:
        for i in range(100):
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
                xxxxx = random.random()
                if np.exp(-abs((cost - new_cost)) / T) > xxxxx:
                    print(T, np.exp(-abs((cost - new_cost)) / T),xxxxx, abs((cost - new_cost)))
                    cost = np.copy(new_cost)
                    city_list_final = np.copy(city_list)
                    min_num = counter
                    
        cost_array.append(np.copy(cost).tolist())
        T_array.append(np.copy(T).tolist())
        T *= alpha
        swap_range = alpha*swap_range
        # print(T, swap_range, new_cost, city_list)
    return city_list_final, cost, min_num, cost_array, T_array


city_list = np.append([np.linspace(0, 9, 10, dtype=int)], [-1, -1]) # city_list is a list of city index
np.random.shuffle(city_list)

# city_list, cost, min_num = simulated_annealing(city_list, math.inf, 1000, 0.99, 1)

# print(city_list, cost)


data_pd = pd.read_csv('data100.csv', header=None)

data = data_pd.to_numpy()

min_cost = min(data[0][1:])
min_index = np.where(data[0] == min_cost)[0][0]

data_pd = pd.read_csv('random_sampling100.csv', header=None)
data_tuned = data_pd.to_numpy()

T_0   = data_tuned[0][7]
T_f   = data_tuned[1][7]
alpha = data_tuned[2][7]


city_list = np.append([np.linspace(0, 9, 10, dtype=int)], [-1, -1]) # city_list is a list of city index
np.random.shuffle(city_list)
city_list, cost, min_num, cost_array, T_array = simulated_annealing(city_list, math.inf, T_0, alpha, T_f)
print(city_list, cost, min_num)

plt.plot(T_array, cost_array)
plt.xlabel('Temperature')
plt.ylabel('Cost')
plt.savefig('../../Figure/Q3/all.eps', format='eps')
plt.close()

plt.plot(T_array[-100:], cost_array[-100:])
plt.xlabel('Temperature')
plt.ylabel('Cost')
plt.savefig('../../Figure/Q3/final.eps', format='eps')
plt.close()