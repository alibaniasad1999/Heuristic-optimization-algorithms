import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray
from paretoset import paretoset
from market import Market


def plot_3d(x, y, z, i, number):
    plot_font = {'fontname': 'Times New Roman'}
    ax = plt.axes(projection='3d')
    ax.scatter(x, y, z)
    plt.title(f'Iteration = {i}', **plot_font, fontsize=10)
    ax.set_xlabel(r'$1^{st}$ Objective function', **plot_font, fontsize=10)
    ax.set_ylabel(r'$2^{st}$ Objective function', **plot_font, fontsize=10)
    ax.set_zlabel(r'$3^{st}$ Objective function', **plot_font, fontsize=10)
    # plt.savefig(f'../../Figure/iteration_3d_{number}.png', format='png', dpi=1000)


def plot(x, y, i, number):
    plot_font = {'fontname': 'Times New Roman'}
    plt.plot(x, y, 'o')
    plt.title(f'Iteration = {i}', **plot_font, fontsize=10)
    plt.xlabel(r'$1^{st}$ Objective function', **plot_font, fontsize=10)
    plt.ylabel(r'$2^{st}$ Objective function', **plot_font, fontsize=10)
    # plt.savefig(f'../../Figure/iteration_{number}.png', format='png', dpi=1000)


def objective_function(location):
    return [-np.sum((location - 0) ** 2), -np.sum((location - 10) ** 2), -np.sum((location + 10) ** 2)]


domain: ndarray = np.array([[-65, 65], [-65, 65], [-65, 65]])

market = Market(objective_function=objective_function, domain=domain, demander_number=80, supplier_number=20,
                max_friends=20, characteristics_length=np.sqrt(len(domain)), k_sigma_d=0.7, k_sigma_s=0.7, k_num_s=0.4)

n_iteration = 100
value_history = np.zeros(n_iteration)
max_value = 0
best_place = 0
history_np_array = np.array([-np.inf * np.ones(len(objective_function(0)))])
history_np_location = np.array([-np.inf * np.ones(len(domain))])
plot_save_counter = 0
for i in range(n_iteration):
    history = [j.best_location.value() for j in market.demanders]
    location_history = [j.best_location.location for j in market.demanders]

    history_np_array = np.concatenate((history_np_array, history))
    history_np_location = np.concatenate((history_np_location, location_history))

    pareto_opt = paretoset(-np.array(history_np_array))
    history_np_array = history_np_array[pareto_opt]
    history_np_location = history_np_location[pareto_opt]

    if i % 20 == 0 and i != 0:
        print(i)
        market.make_friend()
        market.supplier_update()

    market.price_evaluation()
    market.demander_update()
