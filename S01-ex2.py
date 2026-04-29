import numpy as np

rng = np.random.default_rng(seed=0)

U = rng.uniform(0, 1, size=100)
X = np.where(U < 1 / 3, 1, 2)
mean = np.mean(X == 1)
print(f"Mean {mean}")

U = rng.uniform(0, 1, size=1000)
X = np.where(U < 1 / 3, 1, 2)
mean = np.mean(X == 1)
print(f"Mean {mean}")

U = rng.uniform(0, 1, size=1000)
X = np.where(U < 1 / 3, 1, 2)
mean = np.mean(X == 1)
print(f"Mean {mean}")
