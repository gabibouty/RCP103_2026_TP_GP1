import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=1)
vmin = 0
vmax = 10000

# Distribution normale
m = 50  # moyenne
s = 10  # ecart type

for n in [10, 100, 1000, 10000]:
    # Tirer n normales
    # https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.normal.html
    vrandom = rng.normal(m, s, size=n)
    print(f"=== n = {n} ===\n {vrandom}")

    # Tracé de l'histogramme
    plt.figure(figsize=(10, 6))
    plt.hist(vrandom, bins=20, edgecolor="black", alpha=0.7)
    plt.title(f"Histogramme pour n = {n}")
    plt.xlabel("Valeur")
    plt.ylabel("Fréquence")
    plt.xticks(np.linspace(m - 4 * s, m + 4 * s, 9))
    # plt.xticks(np.linspace(vmin, vmax, 10))
    plt.grid(axis="y", alpha=0.75)
    # plt.show()

    # sauvegarde
    plt.savefig(f"dist_norm_histogramme_n_{n}.png", dpi=200, bbox_inches="tight")
    plt.close()
