import numpy as np
import matplotlib.pyplot as plt


def plot_fit(x, y):
    a, b = np.polyfit(x, y, 1)
    x0 = np.array([x.min(), x.max()])
    y0 = a * x0 + b

    plt.figure(figsize=(6, 6))
    plt.plot(x, y, '.', label='data')
    plt.plot(x0, y0, label=f'{a:.4g}x{b:+.4f}')
    plt.legend()
    plt.show()