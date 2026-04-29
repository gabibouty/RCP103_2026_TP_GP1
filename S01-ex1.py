import numpy as np
import matplotlib.pyplot as plt

# COMMON
n_steps = 100
x = np.zeros(n_steps)
plt.figure(figsize=(10, 5))
plt.xlabel("n")
plt.ylabel("$X_n$")
plt.grid(True, linestyle="--", alpha=0.9)

# PART 1
x[0] = 5
for i in range(1, n_steps):
    x[i] = (3 * x[i - 1]) % 150
plt.plot(x, marker="o", linestyle="-", color="b", markersize=4, alpha=0.6)
plt.show()

# PART 2
x[0] = 3
for i in range(1, n_steps):
    x[i] = (5 * x[i - 1] + 7) % 200
plt.plot(x, marker="o", linestyle="-", color="b", markersize=4, alpha=0.6)
plt.show()
