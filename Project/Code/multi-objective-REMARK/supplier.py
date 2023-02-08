import numpy as np


class Supplier:
    def __init__(self, current_location):
        self.current_location = current_location

    def move(self, ideal_property, max_value, min_value, n_supplier, k_sigma_s):
        ideal_property = ideal_property[0]
        norm_value = (ideal_property.value() - min_value) / (max_value - min_value)
        q_supply = (1 - norm_value) / (n_supplier + 1)
        q_supply = np.linalg.norm(q_supply)
        # next_location_mean = self.next_location.location
        # next_location_std = k_sigma_s * abs(self.next_location.price) * np.sqrt(-2*np.log(self.purchase_power))
        new_location = np.copy(np.random.normal(ideal_property.location, k_sigma_s * q_supply))
        new_location[new_location > 1] = 1
        new_location[new_location < 0] = 0
        self.current_location.location = np.copy(new_location)
