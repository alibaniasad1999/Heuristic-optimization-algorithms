import numpy as np
from property import Property


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
        if self.next_location.value() > self.best_location.value():
            self.best_location = self.current_location

    def communication(self, k_sigma_d):
        self.next_location = Property(location=np.copy(self.best_location.location),
                                      objective_function=self.best_location.objective_function,
                                      domain=self.best_location.domain, price=self.best_location.price,
                                      demand=self.best_location.demand, supply=self.best_location.supply)

        for i in self.friend:
            if i.best_location.value() > self.best_location.value():
                self.next_location = Property(location=np.copy(i.best_location.location),
                                              objective_function=i.best_location.objective_function,
                                              domain=i.best_location.domain, price=i.best_location.price,
                                              demand=i.best_location.demand, supply=i.best_location.supply)

        next_location_mean = self.next_location.location
        next_location_std = k_sigma_d * abs(self.next_location.price) * np.sqrt(-2 * np.log(self.purchase_power))

        new_location = np.random.normal(next_location_mean, next_location_std)
        new_location[new_location > 1] = 1
        new_location[new_location < 0] = 0

        self.next_location = Property(location=np.copy(new_location),
                                      objective_function=self.next_location.objective_function,
                                      domain=self.next_location.domain, price=self.next_location.price,
                                      demand=self.next_location.demand, supply=self.next_location.supply)
