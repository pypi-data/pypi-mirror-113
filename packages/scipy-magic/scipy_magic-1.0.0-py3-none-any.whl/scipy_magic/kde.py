from functools import lru_cache

import matplotlib.pyplot as plt
import numpy as np

from IPython.core.pylabtools import print_figure
from scipy.stats.kde import gaussian_kde


@lru_cache
def _repr_png_(kde: gaussian_kde) -> bytes:
    sample = kde.dataset
    n, dim = sample.shape

    if n == 1:
        sample = sample.flatten()
        n, dim = dim, 1

    x_eval = np.linspace(
        np.min(sample, axis=0), np.max(sample, axis=0), num=200
    )
    pdf = kde(x_eval)

    fig, ax = plt.subplots()

    ax.plot(x_eval, pdf, "-", lw=5, alpha=0.6)

    # discrete samples
    delta = np.max(pdf) * 5e-2
    n = min(n, 100)
    ax.plot(sample[:n], -delta - delta * np.random.random(n), "+k")

    ax.set_ylabel(r"$f$")
    ax.set_xlabel(r"$x$")

    data = print_figure(fig, "png")

    # We MUST close the figure, otherwise IPython's display machinery
    # will pick it up and send it as output, resulting in a double display
    plt.close(fig)
    return data


def load_ipython_extension(ipython) -> None:
    png_f = ipython.display_formatter.formatters["image/png"]
    png_f.for_type_by_name("scipy.stats.kde", "gaussian_kde", _repr_png_)
