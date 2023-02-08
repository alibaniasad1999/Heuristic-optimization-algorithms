import numpy as np
import collections.abc
from paretoset import paretoset
from property import Property
from demander import Demander
from supplier import Supplier


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
                i.current_location.demand)

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
        # # values = np.zeros((2*len()))
        # # for i in self.demanders:
        # #     values.
        # best_location_values = [i.best_location.value() for i in self.demanders]
        # current_location_values = [i.best_location.value() for i in self.demanders]
        # max_value = -np.inf
        # max_price = -np.inf
        # min_value = np.inf
        # # ideal_property = None
        demanders_location_values = [[], [], [],
                                     []]  # first is location of the best location and current location, second is
        # value of the best location and current location, third is price and forth is property
        # (best or current which is grater)
        for count, i in enumerate(self.demanders):  # wwwwwwrrrrrrrooooooonnnnnnggggggg
            demanders_location_values[0].append(i.best_location.location)
            demanders_location_values[0].append(i.current_location.location)
            demanders_location_values[1].append(i.best_location.value())
            demanders_location_values[1].append(i.current_location.value())
            demanders_location_values[2].append(i.best_location.price)
            demanders_location_values[2].append(i.current_location.price)
            demanders_location_values[3].append(i.best_location)
            demanders_location_values[3].append(i.current_location)

        mask_max = paretoset(-np.array(demanders_location_values[1]))  # find pareto set max
        mask_min = paretoset(np.array(demanders_location_values[1]))  # find pareto set min

        pareto_optimum_max = np.where(mask_max)[0]
        pareto_optimum_min = np.where(mask_min)[0]

        location_array = np.array(demanders_location_values[0])
        price_array = np.array(demanders_location_values[2])
        property_array = np.array(demanders_location_values[3])

        best_price_array = [
            [price_array[price_array.argsort()[0:min(len(pareto_optimum_min), len(pareto_optimum_max))]]],
            [location_array[price_array.argsort()[0:min(len(pareto_optimum_min), len(pareto_optimum_max))]]],
            [property_array[price_array.argsort()[0:min(len(pareto_optimum_min),
                                                        len(pareto_optimum_max))]]]]  # first is best price value,
        # second is location of best price value and third is property

        # for i in self.demanders:
        #     if i.best_location.value() > max_value:
        #         max_value = np.copy(i.best_location.value())
        #     if i.current_location.value() > max_value:
        #         max_value = np.copy(i.current_location.value())
        #     if i.best_location.value() < min_value:
        #         min_value = np.copy(i.best_location.value())
        #     if i.current_location.value() < min_value:
        #         min_value = np.copy(i.current_location.value())
        #     if i.current_location.price > max_price or np.isinf(i.current_location.price):
        #         max_price = np.copy(i.current_location.price)
        #         ideal_property = i.current_location
        #     if i.best_location.price > max_price or np.isinf(i.current_location.price):
        #         max_price = np.copy(i.best_location.price)
        #         ideal_property = i.best_location

        for i in np.random.choice(self.suppliers, size=self.max_friends, replace=False):
            distance = np.linalg.norm(i.current_location.location - best_price_array[1])
            if not (isinstance(distance, collections.abc.Sequence)):  # check is scaler or array
                ideal_property = best_price_array[2][0]
                max_value = pareto_optimum_max[0]
                min_value = pareto_optimum_min[0]
            else:
                ideal_property = np.random.choice(np.array(best_price_array[2]).reshape(-1),
                                                  distance / np.sum(distance))
                distance_max = np.linalg.norm(
                    np.array(demanders_location_values[0])[mask_max] - i.current_location.location)
                max_value = np.random.choice(np.array(demanders_location_values[1])[mask_max].reshape(-1),
                                             distance_max / sum(distance_max))

                distance_min = np.linalg.norm(
                    np.array(demanders_location_values[0])[mask_min] - i.current_location.location)
                min_value = np.random.choice(np.array(demanders_location_values[1])[mask_max].reshape(-1),
                                             distance_min / sum(distance_min))

            i.move(ideal_property, max_value, min_value, n_supplier, self.k_sigma_s)

        # [i.move(ideal_property, max_value, min_value, n_supplier, self.k_sigma_s) for i in
        #  np.random.choice(self.suppliers, size=self.max_friends, replace=False)]
