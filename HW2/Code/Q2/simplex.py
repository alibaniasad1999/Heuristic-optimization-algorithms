import numpy as np
import random
import statistics

def function2optimize(x, con):
    if con == 1:
        return sum(x**2) -450
    else:
        ans = 0
        for i in range(len(x)):
            ans += sum(x[0:i+1]**2)
        return ans * (1 + random.random()) - 450

def simplex(x, alpha, con):
    # x is dictionary with keys: 'x0', 'x1', 'x2'
    sorted_x = dict(sorted(x.items()))
    x_keys = list(sorted_x.keys()) # cost
    # x_1 = sorted_x[x_keys[0]] # points
    # x_2 = sorted_x[x_keys[1]]
    x_h = sorted_x[x_keys[len(x_keys)-1]]
    sum_elements = 0
    sorted_x.popitem()
    for i in sorted_x.keys():
        sum_elements = sum_elements + sorted_x[i]
    x_0 = 1/(len(x)-1) * sum_elements


    # quadratic interpolation
    x_r_1 = (1+ alpha) * x_0 - alpha * x_h
    x_r_2 = (1+ 1.1*alpha) * x_0 - 1.1*alpha * x_h
    x_r_3 = (1+ 0.9*alpha) * x_0 - 0.9*alpha * x_h
    A = np.array([[alpha**2, alpha, 1], [(1.1*alpha)**2, 1.1*alpha, 1], [(0.9*alpha)**2, 0.9*alpha, 1]])
    B = np.array([[function2optimize(x_r_1, con)], [function2optimize(x_r_2, con)], [function2optimize(x_r_3, con)]])
    X = np.linalg.inv(A).dot(B)
    # if x_r == x_1 or x_r == x_2:
    #     x_r = np.array([random.random() * 20 -10], [random.random() * 20 -10])
    if X[0] == 0:
        gamma = 0.1
    else:
        gamma = -X[1] / 2 / X[0]


    x_r = (1+ gamma) * x_0 - gamma * x_h
    x_r_key = function2optimize(x_r, con)
    for i in sorted_x.keys():
        if x_r_key == i:
            x_r = x_r + random.random() * 0.1 - 0.05
    
    while True:
        if (x_r_key in sorted_x.keys()):
                for i in sorted_x.keys():
                    if x_r_key == i:
                        x_r = x_r + random.random()  - 0.5
                        x_r_key = function2optimize(x_r, con)
        else:
            break
    
    
    sorted_x[function2optimize(x_r, con)] = x_r
    return sorted_x

# Path: main.py

n = int(input('insert dimension: '))
con = int(input('insert function num: '))
sol = np.ones(25)
itetation = int(1e5)
for k in range(25):
    x = np.random.rand(n+1,n) * 20 - 10
    # x = np.array([[random.random() * 20 -10,  random.random() * 20 -10],  [random.random() * 20 -10, random.random() * 20 -10],  [random.random() * 20 -10,  random.random() * 20 -10]])
    x_array = {}
    for i in x:
        x_array[function2optimize(i, con)] =  np.array(i)

    print(x_array)
    x_array_old = x_array
    alpha = 0.5
    for i in range(itetation):
        # print(x_array)
        x_array_old = x_array
        x_array = simplex(x_array, alpha, con)
        min_sol = min(x_array.keys())
        if sum(x_array.keys()) > sum(x_array_old.keys()):
            alpha = alpha * 0.9
        # if (sum(x_array.keys()) / len(x_array.keys())) > min_sol and statistics.variance(x_array.keys()) < 0.0001:
        #     x = np.array([[random.random() * 20 -10,  random.random() * 20 -10],  [random.random() * 20 -10, random.random() * 20 -10],  [random.random() * 20 -10,  random.random() * 20 -10]])
        #     x_array = {}
        #     for i in x:
        #         x_array[function2optimize(i)] =  np.array(i)
        if sum(x_array.keys()) < 1e-8:
            print('done')
            break

    print(k, min_sol)

    sol[k] = min_sol


np.savetxt('sol'+str(n)+'func'+str(con)+'ite'+str(itetation)+'.csv', sol, delimiter=",")

    
