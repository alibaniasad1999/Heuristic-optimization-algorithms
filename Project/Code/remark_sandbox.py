def a(b):
    return b ** 2


class Demander:
    def __init__(self, location, objective_function, domain):
        self.location = location
        self.objective_function = objective_function
        self.domain = domain

    def cost_function(self):
        return self.objective_function(self.location)


ali = Demander(1, a, 3)
print(ali.cost_function())

