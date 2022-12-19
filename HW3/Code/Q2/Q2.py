# Tanu search for the best path to visit all the cities

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
    location = np.array([[-19, 25, -40, 2, 21, -21, 41, -25, 33, 44],
                         [-5, -40, -24, 47, -19, 35, 13, -42, 8, -44]])
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
                cost[list_city.index(i)] += np.linalg.norm(new_location[i[j]] - new_location[i[j - 1]])

    return max(cost)


def swap_random(city_list):
    idx = range(len(city_list))
    i1, i2 = random.sample(idx, 2)
    city_list[i1], city_list[i2] = city_list[i2], city_list[i1]
    return city_list


# tabu search
def tabu_search(city_list, max_iter, tabu_size):
    cost = []
    tabu_list = [city_list.copy()]
    min_cost = cost_calculator(city_list)
    min_num = 0
    for i in range(max_iter):
        city_list = swap_random(city_list)
        neighber_ans = city_list.copy()
        min_neighber_ans = math.inf
        for j in range(50):
            city_list = swap_random(city_list)
            # tabu_list.append(city_list.copy())
            if cost_calculator(city_list) < min_neighber_ans:
                min_neighber_ans = cost_calculator(city_list)
                neighber_ans = city_list.copy()
        city_list = neighber_ans.copy()

        if city_list not in tabu_list:
            print('not in tabu: ', i, 'tau len', len(tabu_list))
            tabu_list.append(city_list.copy())
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)
            if cost_calculator(city_list) < min_cost:
                min_cost = cost_calculator(city_list)
                min_num = i
                # temp_cost = (cost_calculator(city_list))
                # cost.append(temp_cost.copy())
        else:
            print('in tabu: ', i)
            city_list = swap_random(city_list)
        
        temp_cost = (cost_calculator(city_list))
        cost.append(temp_cost.copy())
    return city_list, min_cost, min_num, cost


city_list_array = []
min_cost_array = []
min_city_list = []
min_cost = math.inf
for i in range(1):
    city_list = np.append([np.linspace(0, 9, 10, dtype=int)], [-1, -1])  # city_list is a list of city index
    np.random.shuffle(city_list)
    city_list = city_list.tolist()
    print(city_list)
    city_list, min_cost, min_num, cost = tabu_search(city_list, 10000, 500)
    if min_cost < min_cost:
        min_cost = min_cost
        min_city_list = city_list.copy()
    city_list_array.append(city_list)  # city_list_array is a list of city_list
    min_cost_array.append(min_cost) # min_cost_array is a list of min_cost

print('mean cost: ', np.mean(min_cost_array), 'std cost: ', np.std(min_cost_array), 'min cost: ', min(min_cost_array), 'max cost: ', max(min_cost_array))
print('min city list: ', city_list_array, min_cost_array)

# print the result
fig, ax = plt.subplots()    
ax.plot(cost)
ax.set(xlabel='iteration', ylabel='cost')
name = 'tabu' + '.pdf'
name = '../../Figure/Q2/' + name
plt.savefig(name, format='pdf')
