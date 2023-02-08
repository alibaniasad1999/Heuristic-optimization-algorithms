import numpy as np
from property import Property
from paretoset import paretoset


class Demander:
    def __init__(self, current_location, objective_function,
                 friend=None, best_location=None, next_location=None, purchase_power=None):
        self.current_location = current_location
        if best_location is None:
            self.best_location = Property(np.copy(current_location.location), current_location.objective_function,
                                          current_location.domain)
        else:
            self.best_location = best_location
        if next_location is None:
            self.next_location = Property(np.copy(current_location.location), current_location.objective_function,
                                          current_location.domain)
        else:
            self.next_location = next_location
        self.objective_function = objective_function
        if friend is None:
            self.friend = []
        else:
            self.friend = friend
        if purchase_power is None:
            self.purchase_power = np.random.rand()

    def add_friend(self, demander_friend):
        self.friend.append(demander_friend)

    def move(self):
        self.current_location = self.next_location
        values_current_next = np.array([self.current_location.value(), self.best_location.value()])
        current_next_pareto_opt = paretoset(-values_current_next)

        if current_next_pareto_opt[0]:  # maybe with random will do it better
            self.best_location = self.current_location

    def communication(self, k_sigma_d):
        if len(self.friend) == 0:
            self.next_location = Property(location=np.copy(self.best_location.location),
                                          objective_function=self.best_location.objective_function,
                                          domain=self.best_location.domain, price=self.best_location.price,
                                          demand=self.best_location.demand, supply=self.best_location.supply)
            return

        best_location_array = np.zeros((len(self.friend), len(self.current_location.domain)))

        for counter, i in enumerate(self.friend):
            best_location_array[counter] = i.best_location.value()

        max_value_pareto_opt = paretoset(-best_location_array)
        pareto_optimum_max = np.where(max_value_pareto_opt)[0]

        distance = np.zeros((len(pareto_optimum_max), len(self.current_location.domain)))

        for counter, i in enumerate(pareto_optimum_max):
            distance[counter] = self.current_location.location - self.friend[i].best_location.location

        distance_norm = [np.linalg.norm(i) for i in distance]

        if sum(sum(distance)) == 0:
            self.next_location = Property(
                location=np.copy(self.current_location.location),
                objective_function=self.current_location.objective_function,
                domain=self.current_location.domain,
                price=self.current_location.price,
                demand=self.current_location.demand,
                supply=self.current_location.supply)
            return

        distance_norm_normalized = distance_norm / sum(distance_norm)

        next_best_location_index = np.random.choice(pareto_optimum_max, p=distance_norm_normalized)

        self.next_location = Property(location=np.copy(self.friend[next_best_location_index].best_location.location),
                                      objective_function=self.friend[
                                          next_best_location_index].best_location.objective_function,
                                      domain=self.friend[next_best_location_index].best_location.domain,
                                      price=self.friend[next_best_location_index].best_location.price,
                                      demand=self.friend[next_best_location_index].best_location.demand,
                                      supply=self.friend[next_best_location_index].best_location.supply)

        next_location_mean = self.next_location.location
        next_location_std = k_sigma_d * abs(self.next_location.price) * np.sqrt(-2 * np.log(self.purchase_power))

        new_location = np.random.normal(next_location_mean, next_location_std)
        new_location[new_location > 1] = 1
        new_location[new_location < 0] = 0

        self.next_location = Property(location=np.copy(new_location),
                                      objective_function=self.next_location.objective_function,
                                      domain=self.next_location.domain, price=self.next_location.price,
                                      demand=self.next_location.demand, supply=self.next_location.supply)
