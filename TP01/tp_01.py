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
    axe, x, n, title, bins="auto", use_int_x_axes=False, start_at_zero=True, func=None
):
    axe.hist(x, bins=bins, edgecolor="black", alpha=0.5, density=True)
    axe.set_title(f"{title} (n={n})")
    axe.set_xlabel("$X = x$")
    axe.set_ylabel("$PMF/PDF$")
    axe.grid(True, linestyle="--", alpha=0.5)
    if use_int_x_axes:
        axe.xaxis.set_major_locator(MultipleLocator(1))
    if start_at_zero:
        axe.set_xlim(left=0)
        axe.set_ylim(bottom=0)

    if func is not None:
        x_vals = np.linspace(axe.get_xlim()[0], axe.get_xlim()[1], 1000)
        y_vals = func(x_vals)

        if isinstance(y_vals, float) or isinstance(y_vals, int):
            axe.axhline(
                y=y_vals,
                color="red",
                linestyle="--",
                linewidth=2,
                label="PDF/PMF théorique",
            )
        else:
            axe.plot(
                x_vals,
                y_vals,
                color="red",
                linestyle="--",
                linewidth=2,
                label="PDF/PMF théorique",
            )
        axe.legend()


def format_value(val):
    return str(val) if val.is_integer() else f"{val:.4}"


def print_x(x, n, esp):
    print(
        f"n: {n:6}, 5 premières et 5 dernières valeurs: [{', '.join([format_value(val) for val in x[:5]])} ... {', '.join([format_value(val) for val in x[-5:]])}]"
    )
    real = np.mean(x)
    delta = real - esp
    print(
        f"n: {n:6}, Espérance théorique: {format_value(esp)}, Espérance constatée: {format_value(real)}, Delta: {format_value(delta)}"
    )


# ========================================================
# DISTRIBUTIONS


def uniform_discrete():
    axes = init_axes()
    print("=== uniform_discrete ===")
    for i, n in enumerate(N_VALUES):
        MIN = 0
        MAX = 20
        rng = np.random.default_rng(seed=SEED)
        x = rng.integers(low=MIN, high=MAX + 1, size=n)
        uniform_pmf = lambda t_x: 1 / (MAX - MIN + 1)
        draw_on_axe(
            axes[i],
            x,
            n,
            "Uniform Discrete",
            bins=np.arange(-0.5, MAX + 1 + 0.5, 1),
            start_at_zero=False,
            use_int_x_axes=True,
            func=uniform_pmf,
        )
        print_x(x, n, (MIN + MAX) / 2)
    plt.tight_layout()
    plt.savefig("uniform_discrete.png")


def uniform_real():
    axes = init_axes()
    print("\n=== uniform_real ===")
    for i, n in enumerate(N_VALUES):
        rng = np.random.default_rng(seed=SEED)
        # By default, rng.uniform return values in range [0.0;1.0] (include)
        x = rng.uniform(size=n)
        MAX = 1
        MIN = 0
        uniform_pmf = lambda t_x: 1 / (MAX - MIN)
        draw_on_axe(axes[i], x, n, "Uniform Real", func=uniform_pmf)
        print_x(x, n, (0.0 + 1.0) / 2)
    plt.tight_layout()
    plt.savefig("uniform_real.png")


def exponential():
    axes = init_axes()
    print("\n=== exponential ===")
    for i, n in enumerate(N_VALUES):
        AVG = 1
        LAMBDA = 1 / AVG
        # More AVG is high, more the distibution decrease quickly
        rng = np.random.default_rng(seed=SEED)
        x = rng.exponential(scale=LAMBDA, size=n)
        exp_pdf = lambda t_x: LAMBDA * np.exp(-LAMBDA * t_x)
        draw_on_axe(axes[i], x, n, "Exponential", func=exp_pdf)
        print_x(x, n, AVG)
    plt.tight_layout()
    plt.savefig("exponential.png")


def normal():
    axes = init_axes()
    print("\n=== normal ===")
    for i, n in enumerate(N_VALUES):
        MU_AVG = 0
        SIGMA_VAR = 1
        rng = np.random.default_rng(seed=SEED)
        x = rng.normal(loc=MU_AVG, scale=SIGMA_VAR, size=n)
        normal_pdf = lambda t_x: np.exp(-(((t_x - MU_AVG) / SIGMA_VAR) ** 2) / 2) / (
            SIGMA_VAR * np.sqrt(2 * np.pi)
        )
        draw_on_axe(axes[i], x, n, "Normal", start_at_zero=False, func=normal_pdf)
        print_x(x, n, MU_AVG)
    plt.tight_layout()
    plt.savefig("normal.png")


def binomial():
    axes = init_axes()
    print("\n=== binomial ===")
    for i, n in enumerate(N_VALUES):
        N = 10
        P = 0.50
        Q = 1 - P
        rng = np.random.default_rng(seed=SEED)
        x = rng.binomial(p=P, n=N, size=n)
        normal_approx = lambda t_x: (1 / np.sqrt(2 * np.pi * N * P * Q)) * np.exp(
            -0.5 * ((t_x - N * P) ** 2) / (N * P * Q)
        )

        draw_on_axe(
            axes[i],
            x,
            n,
            "Binomial",
            bins=np.arange(-0.5, N + 1 + 0.5, 1),
            use_int_x_axes=True,
            start_at_zero=False,
            func=normal_approx,
        )
        print_x(x, n, N * P)
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
