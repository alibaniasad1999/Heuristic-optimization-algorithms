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
