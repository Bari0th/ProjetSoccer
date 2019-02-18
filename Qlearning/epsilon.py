import random

class EpsilonGreedy:
    def __init__(self, epsilon=0.1, n_arms = 1):
        self.epsilon = epsilon
        self.n_arms = n_arms
        self.counts = None
        self.values = None

        self.initialize()

    def initialize(self):
        self.counts = [0 for col in range(self.n_arms)]
        self.values = [0.0 for col in range(self.n_arms)]

    def ind_max(self, x):
        m = max(x)
        return x.index(m)

    def select_arm(self):
        if random.random() > self.epsilon :
            return self.ind_max(self.values)
        return random.randrange(len(self.values))

    def update(self, reward):
        chosen_arm = self.select_arm()
        self.counts[chosen_arm] += 1
        n = self.counts[chosen_arm]

        value = self.values[chosen_arm]
        new_value = ((n-1)/float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_arm] = new_value


if __name__ == "__main__":
    algo = EpsilonGreedy(0.2, 4)
    for i in range(50):
        algo.update(0.5 * i * (i%2 * - 1))