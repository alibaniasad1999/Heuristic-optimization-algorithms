# Tanu search for the best path to visit all the cities

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

def swap_random(city_list):
    idx = range(len(city_list))
    i1, i2 = random.sample(idx, 2)
    city_list[i1], city_list[i2] = city_list[i2], city_list[i1]
    return city_list


# tabu search
def tabu_search(city_list, max_iter, tabu_size):
    tabu_list = []
    tabu_list.append(city_list.copy())
    min_cost = cost_calculator(city_list)
    min_num = 0
    for i in range(max_iter):
        city_list = swap_random(city_list)
        if city_list not in tabu_list:
            print('not in tabu: ', i, 'tau len', len(tabu_list))
            tabu_list.append(city_list.copy())
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)
            if cost_calculator(city_list) < min_cost:
                min_cost = cost_calculator(city_list)
                min_num = i
        else:
            print('in tabu: ', i)
            city_list = swap_random(city_list)
    return city_list, min_cost, min_num


city_list = np.append([np.linspace(0, 9, 10, dtype=int)], [-1, -1]) # city_list is a list of city index

np.random.shuffle(city_list)
city_list = city_list.tolist()
print(city_list)
city_list, min_cost, min_num = tabu_search(city_list, 1000, 500)
print(city_list)
print(min_cost)
print(min_num)
