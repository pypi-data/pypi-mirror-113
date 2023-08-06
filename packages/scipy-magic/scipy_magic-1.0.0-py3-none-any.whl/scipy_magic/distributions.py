from functools import lru_cache

import matplotlib.pyplot as plt
import numpy as np

from IPython.core.pylabtools import print_figure
from scipy.stats._distn_infrastructure import rv_frozen


def _repr_pretty_(distribution, p, cycle) -> None:
    name = distribution.dist.name
    with p.group(len(name) + 1, name + "(", ")"):
        for i, arg in enumerate(distribution.args):
            if i > 0:
                p.text(",")
                p.breakable()
            p.pretty(arg)
        for i, (key, value) in enumerate(distribution.kwds.items()):
            if i > 0 or len(distribution.args) > 0:
                p.text(",")
                p.breakable()
            p.text(key + "=")
            p.pretty(value)


@lru_cache
def _repr_png_(distribution: rv_frozen) -> bytes:
    title = (
        f"{distribution.dist.name}(args={distribution.args},"
        f" kwargs={distribution.kwds}), N=1000"
    )

    fig, axs = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(9, 4))

    x = np.linspace(distribution.ppf(0.01), distribution.ppf(0.99), 100)

    # PDF
    pdf = distribution.pdf(x)
    axs[0].plot(x, pdf, "-", lw=5, alpha=0.6)

    # CDF
    cdf = distribution.cdf(x)
    axs[1].plot(x, cdf, "-", lw=5, alpha=0.6)

    # Empirical PDF
    sample = distribution.rvs(size=1000)

    # discrete samples
    delta = np.max(pdf) * 5e-2
    axs[0].plot(sample[:100], -delta - delta * np.random.random(100), "+k")

    fig.suptitle(title)
    axs[0].set_title("PDF")
    axs[0].set_ylabel(r"$f$")
    axs[0].set_xlabel(r"$x$")

    axs[1].set_title("CDF")
    axs[1].set_ylabel(r"$F$")
    axs[1].set_xlabel(r"$x$")

    data = print_figure(fig, "png")

    # We MUST close the figure, otherwise IPython's display machinery
    # will pick it up and send it as output, resulting in a double display
    plt.close(fig)
    return data


def load_ipython_extension(ipython) -> None:
    png_f = ipython.display_formatter.formatters["image/png"]
    png_f.for_type_by_name(
        "scipy.stats._distn_infrastructure", "rv_frozen", _repr_png_
    )

    plain_f = ipython.display_formatter.formatters["text/plain"]
    plain_f.for_type_by_name(
        "scipy.stats._distn_infrastructure", "rv_frozen", _repr_pretty_
    )
