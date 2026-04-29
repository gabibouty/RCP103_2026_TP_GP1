import numpy as np
import matplotlib.pyplot as plt

SEED = 1

N_VALUES = [10,100,1000,10000]

def uniform_real ():
    np.random.seed(SEED)
    MIN = 0.0
    MAX = 1.0
    _, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.ravel()

    for i, n in enumerate(N_VALUES):
        x = np.random.uniform(low=MIN, high=MAX, size=n)
        axes[i].hist(x, bins='auto', edgecolor='black', alpha=0.5)
        axes[i].set_title(f'Uniform (n={n})')
        axes[i].set_xlabel('$x$')
        axes[i].set_ylabel('$F$')
        axes[i].grid(True, linestyle='--', alpha=0.5)        
    plt.tight_layout()
    plt.savefig("uniform_real.png")


def exponential ():
    np.random.seed(SEED)
    AVG = 1
    _, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.ravel()
    for i, n in enumerate(N_VALUES):
        # More AVG is high, more the distibution decrease quickly
        x = np.random.exponential(scale=1/AVG, size=n)

        axes[i].hist(x, bins='auto', edgecolor='black', alpha=0.5)
        axes[i].set_title(f'Exponential (n={n})')
        axes[i].set_xlabel('$x$')
        axes[i].set_ylabel('$F$')
        axes[i].grid(True, linestyle='--', alpha=0.5)      
    plt.tight_layout()
    plt.savefig("exponential.png")


def binomial ():
    np.random.seed(SEED)
    TRIES = 10
    P = 0.5
    _, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.ravel()
    for i, n in enumerate(N_VALUES):
        x = np.random.binomial(p=P, n=TRIES, size=n)
        axes[i].hist(x, bins='auto', edgecolor='black', alpha=0.5)
        axes[i].set_title(f'Binomial (n={n})')
        axes[i].set_xlabel('$x$')
        axes[i].set_ylabel('$F$')
        axes[i].grid(True, linestyle='--', alpha=0.5)      
    plt.tight_layout()
    plt.savefig("binomial.png")


if __name__ == "__main__":
    uniform_real()
    exponential()
    binomial()
