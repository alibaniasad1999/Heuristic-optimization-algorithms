import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray
from paretoset import paretoset

from market import Market


def objective_function(location):
    return [-np.sum((location - 0) ** 2), -np.sum((location - 10) ** 2)]


domain: ndarray = np.array([[-65, 65], [-65, 65]])

market = Market(objective_function=objective_function, domain=domain, demander_number=200, supplier_number=80,
                max_friends=50, characteristics_length=np.sqrt(len(domain)), k_sigma_d=0.7, k_sigma_s=0.7, k_num_s=0.4)

n_iteration = 1000
value_history = np.zeros(n_iteration)
max_value = 0
best_place = 0
history_np_array = np.array([[-np.inf, -np.inf]])
history_np_array_location = np.array([[-np.inf, -np.inf, -np.inf]])
plot_save_counter = 0
for i in range(n_iteration):
    history = [j.best_location.value() for j in market.demanders]
    max_value = max(history)

    pareto_opt = paretoset(-np.array(history))
    pareto_opt_places_location = []
    pareto_opt_places_value = []

    for counter, j in enumerate(np.where(pareto_opt)[0]):
        pareto_opt_places_location.append(market.demanders[j].best_location.location)
        pareto_opt_places_value.append(history[j])

    history_np_array = np.concatenate((history_np_array, history))
    history_np_array = history_np_array[paretoset(-np.array(history_np_array))]

    if i % 20 == 0 and i != 0:
        print(i)
        market.make_friend()
        market.supplier_update()
        # plot pareto opt
        plot_font = {'fontname': 'Times New Roman'}
        plt.plot(np.array(history)[:, 0], np.array(history)[:, 1], 'o')
        plt.plot(np.array(history_np_array)[:, 0], np.array(history_np_array)[:, 1], 'o')
        plt.title(f'Iteration = {i}', **plot_font, fontsize=10)
        plt.xlabel(r'$1^{st}$ Objective function', **plot_font, fontsize=10)
        plt.ylabel(r'$2^{st}$ Objective function', **plot_font, fontsize=10)
        plt.savefig(f'../../Figure/iteration_{plot_save_counter}.png', format='png', dpi=1000)
        plt.close()
        plot_save_counter += 1

    market.price_evaluation()
    market.demander_update()

    # plt.plot(history_np_array[:, 0], history_np_array[:, 1], 'o')
    # plt.plot(history_np_array[pareto_opt][:, 0], history_np_array[pareto_opt][:, 1], 'o')
    # plt.show()

# ax = plt.axes(projection='3d')
# ax.scatter(history_np_array[:, 0], history_np_array[:, 1], history_np_array[:, 2])
# # plt.plot(history_np_array[pareto_opt][:, 0], history_np_array[pareto_opt][:, 1], 'o')
# plt.show()
