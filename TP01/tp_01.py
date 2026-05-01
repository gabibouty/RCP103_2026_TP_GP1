import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

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


def draw_on_axe(
    axe, x, n, title, bins="auto", use_int_x_axes=False, start_at_zero=True
):
    axe.hist(x, bins=bins, edgecolor="black", alpha=0.5)
    axe.set_title(f"{title} (n={n})")
    axe.set_xlabel("$x$")
    axe.set_ylabel("$F$")
    axe.grid(True, linestyle="--", alpha=0.5)
    if use_int_x_axes:
        axe.xaxis.set_major_locator(MultipleLocator(1))
    if start_at_zero:
        axe.set_xlim(left=0)
        axe.set_ylim(bottom=0)


# ========================================================
# DISTRIBUTIONS


def uniform_discrete():
    axes = init_axes()
    for i, n in enumerate(N_VALUES):
        MIN = 0
        MAX = 20
        rng = np.random.default_rng(seed=SEED)
        x = rng.integers(low=MIN, high=MAX + 1, size=n)
        draw_on_axe(
            axes[i],
            x,
            n,
            "Uniform Discrete",
            bins=np.arange(-0.5, MAX + 1 + 0.5, 1),
            start_at_zero=False,
            use_int_x_axes=True,
        )
    plt.tight_layout()
    plt.savefig("uniform_discrete.png")


def uniform_real():
    axes = init_axes()
    for i, n in enumerate(N_VALUES):
        rng = np.random.default_rng(seed=SEED)
        # By default, rng.uniform return values in range [0.0;1.0] (include)
        x = rng.uniform(size=n)
        draw_on_axe(axes[i], x, n, "Uniform Real")
    plt.tight_layout()
    plt.savefig("uniform_real.png")


def exponential():
    axes = init_axes()
    for i, n in enumerate(N_VALUES):
        AVG = 1
        # More AVG is high, more the distibution decrease quickly
        rng = np.random.default_rng(seed=SEED)
        x = rng.exponential(scale=(1 / AVG), size=n)
        draw_on_axe(axes[i], x, n, "Exponential")
    plt.tight_layout()
    plt.savefig("exponential.png")


def normal():
    axes = init_axes()
    for i, n in enumerate(N_VALUES):
        MU_AVG = 0
        SIGMA_VAR = 1
        rng = np.random.default_rng(seed=SEED)
        x = rng.normal(loc=MU_AVG, scale=SIGMA_VAR, size=n)
        draw_on_axe(axes[i], x, n, "Normal", start_at_zero=False)
    plt.tight_layout()
    plt.savefig("normal.png")


def binomial():
    axes = init_axes()
    for i, n in enumerate(N_VALUES):
        TRIES = 10
        P = 0.50
        rng = np.random.default_rng(seed=SEED)
        x = rng.binomial(p=P, n=TRIES, size=n)
        draw_on_axe(
            axes[i],
            x,
            n,
            "Binomial",
            bins=np.arange(-0.5, TRIES + 1 + 0.5, 1),
            use_int_x_axes=True,
            start_at_zero=False,
        )
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
