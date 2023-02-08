import numpy as np
from numpy import ndarray
from property import denorm
from market import Market


def objective_function(location):
    return -np.sum(location ** 2)


domain: ndarray = np.array([[-65, 65], [-65, 65], [-65, 65], [-65, 65], [-65, 65], [-65, 65], [-65, 65], [-65, 65],
                            [-65, 65], [-65, 65]])

market = Market(objective_function=objective_function, domain=domain, demander_number=80, supplier_number=20,
                max_friends=20, characteristics_length=np.sqrt(len(domain)), k_sigma_d=0.7, k_sigma_s=0.7, k_num_s=0.4)

n_iteration = 100
value_history = np.zeros(n_iteration)
max_value = 0
best_place = 0
for i in range(n_iteration):
    history = [j.best_location.value() for j in market.demanders]
    max_value = max(history)
    max_argument = np.argmax(history)
    print(f"iteration num: {i}\n max value: {max_value}")

    if i % 8 == 0 and i != 0:
        market.make_friend()
        market.supplier_update()

    market.price_evaluation()
    market.demander_update()

    best_place = denorm(market.demanders[max_argument].best_location.location, domain)
    print(best_place)

print(f"best place: {best_place}\n max_value: {max_value}")
