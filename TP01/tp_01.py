import numpy as np
import matplotlib.pyplot as plt

# ========================================================
# CONSTANTS

SEED = 1
N_VALUES = [10, 100, 1000, 10000]


# ========================================================
# COMMONS


def init_axes():
    _, axes = plt.subplots(
        int(np.sqrt(len(N_VALUES))), int(np.sqrt(len(N_VALUES))), figsize=(12, 10)
    )
    axes = axes.ravel()
    return axes


def draw_on_axe(axe, x, n, title, bins = 'auto'):
    axe.hist(x, bins=bins, edgecolor="black", alpha=0.5)
    axe.set_title(f"{title} (n={n})")
    axe.set_xlabel("$x$")
    axe.set_ylabel("$F$")
    axe.grid(True, linestyle="--", alpha=0.5)


# ========================================================
# DISTRIBUTIONS


def uniform_discrete():
    axes = init_axes()
    for i, n in enumerate(N_VALUES):
        np.random.seed(SEED)
        MIN = 0
        MAX = 20
        x = np.random.randint(low=MIN, high=MAX + 1, size=n)
        draw_on_axe(axes[i], x, n, "Uniform Discrete", bins=MAX)
    plt.tight_layout()
    plt.savefig("uniform_discrete.png")


def uniform_real():
    axes = init_axes()
    for i, n in enumerate(N_VALUES):
        np.random.seed(SEED)
        MIN = 0.0
        MAX = 1.0
        x = np.random.uniform(low=MIN, high=MAX, size=n)
        draw_on_axe(axes[i], x, n, "Uniform Real")
    plt.tight_layout()
    plt.savefig("uniform_real.png")


def exponential():
    axes = init_axes()
    for i, n in enumerate(N_VALUES):
        np.random.seed(SEED)
        AVG = 1
        # More AVG is high, more the distibution decrease quickly
        x = np.random.exponential(scale=(1 / AVG), size=n)
        draw_on_axe(axes[i], x, n, "Exponential")
    plt.tight_layout()
    plt.savefig("exponential.png")


def normal():
    axes = init_axes()
    for i, n in enumerate(N_VALUES):
        np.random.seed(SEED)
        MU_AVG = 0
        SIGMA_VAR = 1
        x = np.random.normal(loc=MU_AVG, scale=SIGMA_VAR, size=n)
        draw_on_axe(axes[i], x, n, "Normal")
    plt.tight_layout()
    plt.savefig("normal.png")


def binomial():
    axes = init_axes()
    for i, n in enumerate(N_VALUES):
        np.random.seed(SEED)
        TRIES = 10
        P = 0.5
        x = np.random.binomial(p=P, n=TRIES, size=n)
        draw_on_axe(axes[i], x, n, "Binomial")
    plt.tight_layout()
    plt.savefig("binomial.png")


# ========================================================
# MAIN
if __name__ == "__main__":
    uniform_discrete()
    uniform_real()
    exponential()
    normal()
    binomial()
