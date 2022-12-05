import numpy as np
import random
import math

def function2optimize(x, con):
    if con == 1:
        return sum(x**2) -450
    else:
        ans = 0
        for i in range(len(x)):
            ans += sum(x[0:i+1]**2)
        return ans * (1 + random.random()) - 450

iteration = [1e3, 1e4, 1e5]
iteration = list(map(int, iteration))

func_con = [1, 2]
func_con = list(map(int, func_con))

dimension = [10, 30, 50]
dimension = list(map(int, dimension))

min_cost = math.inf
min_x = np.zeros(25)
for i in iteration:
    for j in func_con:
        for k in dimension:
            for l in range(25):
                x = np.random.rand(i,k) * 20 - 10
                for m in x:
                    if min_cost > function2optimize(m, j):
                        min_cost = function2optimize(m, j)
                min_x[l] = min_cost
                min_cost = math.inf
                print(k, j, i, l, min_x[l])
                np.savetxt('sol_random'+str(k)+'func'+str(j)+'ite'+str(i)+'.csv', min_x, delimiter=",")
            
