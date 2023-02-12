import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray
from paretoset import paretoset
from market import Market


def plot_3d(x, y, z, x1, y1, z1, i, legend, legend1):
    plot_font = {'fontname': 'Times New Roman'}
    ax = plt.axes(projection='3d')
    ax.scatter(x, y, z, label=legend)
    ax.scatter(x1, y1, z1, label=legend1)
    # ax.view_init(angle, angle1)
    plt.title(f'Iteration = {i}', **plot_font, fontsize=10)
    ax.set_xlabel(r'$1^{st}$ Objective function', **plot_font, fontsize=10)
    ax.set_ylabel(r'$2^{st}$ Objective function', **plot_font, fontsize=10)
    ax.set_zlabel(r'$3^{st}$ Objective function', **plot_font, fontsize=10)
    plt.legend(loc="upper left")
    # plt.savefig(f'../../Figure/iteration_3d_{number}.png', format='png', dpi=1000)


def plot(x, y, i, legend):
    plot_font = {'fontname': 'Times New Roman'}
    plt.plot(x, y, 'o', label=legend)
    plt.title(f'Iteration = {i}', **plot_font, fontsize=10)
    plt.xlabel(r'$1^{st}$ Objective function', **plot_font, fontsize=10)
    plt.ylabel(r'$2^{st}$ Objective function', **plot_font, fontsize=10)
    plt.legend(loc="upper left")
    # plt.savefig(f'../../Figure/iteration_{number}.png', format='png', dpi=1000)


def objective_function(location):
    ans = 0
    for i in range(len(location)):
        ans += sum(location[0:i + 1]) ** 2
    return [-np.sum((location-5) ** 2), -ans, -ans * (1 + 0.1 * np.random.random())]


domain: ndarray = np.array([[-65, 65], [-65, 65], [-65, 65]])

market = Market(objective_function=objective_function, domain=domain, demander_number=80, supplier_number=20,
                max_friends=20, characteristics_length=np.sqrt(len(domain)), k_sigma_d=0.7, k_sigma_s=0.7, k_num_s=0.4)

n_iteration = 200
value_history = np.zeros(n_iteration)
max_value = 0
best_place = 0
history_np_array = np.array([-np.inf * np.ones(len(objective_function(np.zeros(len(domain)))))])
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

if len(domain) == 2:
    plot(np.array(history)[:, 0], np.array(history)[:, 1], n_iteration, 'demander')
    plot(np.array(history_np_array)[:, 0], np.array(history_np_array)[:, 1], n_iteration, 'demander')
    plt.show()
if len(domain) == 3:

    plot_3d(np.array(history)[:, 0], np.array(history)[:, 1], np.array(history)[:, 2], np.array(history_np_array)[:, 0],
            np.array(history_np_array)[:, 1], np.array(history_np_array)[:, 2], i, 'demander', 'pareto optimum')
    plt.show()
