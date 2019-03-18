import numpy as np
from scipy import stats
import random
import matplotlib.pyplot as plt

n = 10
arms = np.random.rand(n)
eps = 0.1 # 0 = full exploitation, 1 = full exploration

av = np.ones(n)
counts = np.zeros(n)

def reward(prob):
    total = 0
    for i in range(10):
        if random.random() < prob :
            total += 1

    return total

def bestArm(memory_array):
    return np.argmax(memory_array)

plt.xlabel("Plays")
plt.ylabel("Avg Reward")
for i in range(500):
    if random.random() > eps : # exploitation
        choice = bestArm(av)
    else : # exploration
        choice = np.where(arms == np.random.choice(arms))[0][0]

    counts[choice] += 1
    k = counts[choice]
    rwd = reward(arms[choice])
    old_avg = av[choice]
    new_avg = old_avg + (1/k) * (rwd - old_avg)
    av[choice] = new_avg
    
    #have to use np.average and supply the weights to get a weighted average
    runningMean = np.average(av, weights=np.array([counts[j]/np.sum(counts) for j in range(len(counts))]))
    plt.scatter(i, runningMean)

plt.show()