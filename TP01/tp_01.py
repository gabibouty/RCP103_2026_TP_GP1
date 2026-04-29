import numpy as np
import matplotlib.pyplot as plt

SEED = 1

N_VALUES = [10, 100, 1000, 10000]


def init_rdm_and_axes():
    np.random.seed(SEED)
    _, axes = plt.subplots(
        int(np.sqrt(len(N_VALUES))), int(np.sqrt(len(N_VALUES))), figsize=(12, 10)
    )
    axes = axes.ravel()
    return axes


def draw_on_axe(axe, x, n, title):
    axe.hist(x, bins="auto", edgecolor="black", alpha=0.5)
    axe.set_title(f"{title} (n={n})")
    axe.set_xlabel("$x$")
    axe.set_ylabel("$F$")
    axe.grid(True, linestyle="--", alpha=0.5)


def uniform_real():
    axes = init_rdm_and_axes()
    for i, n in enumerate(N_VALUES):
        MIN = 0.0
        MAX = 1.0
        x = np.random.uniform(low=MIN, high=MAX, size=n)
        draw_on_axe(axes[i], x, n, "Uniform")
    plt.tight_layout()
    plt.savefig("uniform_real.png")


def exponential():
    axes = init_rdm_and_axes()
    for i, n in enumerate(N_VALUES):
        AVG = 1
        # More AVG is high, more the distibution decrease quickly
        x = np.random.exponential(scale=1 / AVG, size=n)
        draw_on_axe(axes[i], x, n, "Exponential")
    plt.tight_layout()
    plt.savefig("exponential.png")


def binomial():
    axes = init_rdm_and_axes()
    for i, n in enumerate(N_VALUES):
        TRIES = 10
        P = 0.5
        x = np.random.binomial(p=P, n=TRIES, size=n)
        draw_on_axe(axes[i], x, n, "Binomial")
    plt.tight_layout()
    plt.savefig("binomial.png")


if __name__ == "__main__":
    uniform_real()
    exponential()
    binomial()
