import numpy as np
from numpy import ndarray


def objective_function(location):
    return -np.sum(location ** 2)


def denorm(data, domain):
    domain.sort()
    return data * (domain[:, 1] - domain[:, 0]) + domain[:, 0]  # data * (max - min) + min


class Property:
    def __init__(self, location, objective_function, domain, price=None, demand=None, supply=None):
        self.location = location
        self.objective_function = objective_function
        self.domain = domain
        if price is None:
            self.price = None
        else:
            self.price = price
        if demand is None:
            self.demand = None
        else:
            self.demand = demand
        if supply is None:
            self.supply = None
        else:
            self.supply = supply

    def value(self):
        return self.objective_function(denorm(self.location, self.domain))


class Supplier:
    def __init__(self, current_location):
        self.current_location = current_location

    def move(self, ideal_property, max_value, min_value, n_supplier, k_sigma_s):
        norm_value = (ideal_property.value() - min_value) / (max_value - min_value)
        q_supply = (1 - norm_value) / (n_supplier + 1)
        # next_location_mean = self.next_location.location
        # next_location_std = k_sigma_s * abs(self.next_location.price) * np.sqrt(-2*np.log(self.purchase_power))
        new_location = np.copy(np.random.normal(ideal_property.location, k_sigma_s * q_supply))
        new_location[new_location > 1] = 1
        new_location[new_location < 0] = 0
        self.current_location.location = np.copy(new_location)


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


class Market:
    def __init__(self, objective_function, domain, demander_number, supplier_number, max_friends,
                 characteristics_length, k_sigma_d, k_sigma_s, k_num_s, demanders=None, suppliers=None):
        self.max_friends = max_friends
        dimension = len(domain)
        if demanders is None:
            self.demanders = [
                Demander(Property(np.random.uniform(size=(dimension,)), objective_function, domain), objective_function)
                for _ in range(demander_number)]
        else:
            self.demanders = demanders
        if suppliers is None:
            self.suppliers = [Supplier(Property(np.random.uniform(size=(dimension,)), objective_function, domain)) for
                              _ in range(supplier_number)]
        else:
            self.suppliers = suppliers
        self.characteristics_length = characteristics_length
        self.k_sigma_d = k_sigma_d
        self.k_num_s = k_num_s
        self.k_sigma_s = k_sigma_s

    def make_friend(self):
        for i in self.demanders:
            i.friend = []
            [i.add_friend(j) for j in
             np.random.choice(self.demanders, size=self.max_friends, replace=False)]

    def demand_evaluation(self):
        occupied_property = [np.copy(i.current_location.location) for i in self.demanders]
        for i in self.demanders:
            i.current_location.demand = (1 / self.characteristics_length / len(self.demanders)) * sum(
                self.characteristics_length - np.sqrt(
                    np.sum((i.current_location.location - occupied_property) ** 2, axis=1)))
            i.best_location.demand = np.copy(
                i.current_location.demand)  # bug in sum(self.characteristics_length - np.sqrt(np.sum((
            # i.current_location.loc - occupied_property)**2))) calculation dont have bug but check in debug

    def supply_evaluation(self):
        occupied_property = []
        [occupied_property.append(np.copy(i.current_location.location)) for i in self.suppliers]
        for i in self.demanders:
            i.current_location.supply = (1 / self.characteristics_length / len(self.suppliers)) * sum(
                self.characteristics_length - np.sqrt(
                    np.sum((i.current_location.location - occupied_property) ** 2, axis=1)))
            i.best_location.supply = np.copy(i.current_location.supply)

    def price_evaluation(self):
        self.demand_evaluation()
        self.supply_evaluation()
        for i in self.demanders:
            i.current_location.price = i.current_location.demand - i.current_location.supply
            i.best_location.price = i.best_location.demand - i.best_location.supply

    def demander_update(self):
        for i in self.demanders:
            i.communication(self.k_sigma_d)
            i.move()

    def supplier_update(self):
        n_supplier = np.ceil(self.k_num_s * len(self.suppliers))
        # selected = randi(length(obj.spl), 1, nSupplier); selected_supplier = np.array([np.copy(i) for i in
        # self.suppliers[np.random.choice(len(self.suppliers), size=self.max_friends, replace=False)]])
        max_value = -np.inf
        max_price = -np.inf
        min_value = np.inf
        # ideal_property = None

        for i in self.demanders:
            if i.best_location.value() > max_value:
                max_value = np.copy(i.best_location.value())
            if i.current_location.value() > max_value:
                max_value = np.copy(i.current_location.value())
            if i.best_location.value() < min_value:
                min_value = np.copy(i.best_location.value())
            if i.current_location.value() < min_value:
                min_value = np.copy(i.current_location.value())
            if i.current_location.price > max_price or np.isinf(i.current_location.price):
                max_price = np.copy(i.current_location.price)
                ideal_property = i.current_location
            if i.best_location.price > max_price or np.isinf(i.current_location.price):
                max_price = np.copy(i.best_location.price)
                ideal_property = i.best_location
            # if ideal_property is None:
            # ideal_property =

        [i.move(ideal_property, max_value, min_value, n_supplier, self.k_sigma_s) for i in
         np.random.choice(self.suppliers, size=self.max_friends, replace=False)]


domain: ndarray = np.array([[-65, 65], [-65, 65], [-65, 65], [-65, 65], [-65, 65], [-65, 65], [-65, 65], [-65, 65],
                            [-65, 65], [-65, 65]])

market = Market(objective_function=objective_function, domain=domain, demander_number=80, supplier_number=20,
                max_friends=20, characteristics_length=np.sqrt(len(domain)), k_sigma_d=0.7, k_sigma_s=0.7, k_num_s=0.4)

n_iteration = 1000
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
