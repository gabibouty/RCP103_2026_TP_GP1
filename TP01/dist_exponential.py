import numpy as np
import matplotlib.pyplot as plt

SEED = 1
N_VALUES = [10,100,1000,10000]
AVG = 1

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.ravel()

np.random.seed(SEED)

for i, n in enumerate(N_VALUES):
    # More AVG is high, more the distibution decrease quickly
    x = np.random.exponential(scale=1/AVG, size=n)

    axes[i].hist(x, bins='auto', edgecolor='black', alpha=0.5)
    axes[i].set_title(f'Exponential (n={n})')
    axes[i].set_xlabel('$x$')
    axes[i].set_ylabel('$F$')
    axes[i].grid(True, linestyle='--', alpha=0.5)
    
plt.tight_layout()
plt.show()

