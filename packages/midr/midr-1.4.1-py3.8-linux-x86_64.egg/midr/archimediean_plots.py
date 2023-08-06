#!/usr/bin/python3

"""Compute the Irreproducible Discovery Rate (IDR) from NarrowPeaks files

Implementation of the IDR methods for two or more replicates.

LI, Qunhua, BROWN, James B., HUANG, Haiyan, et al. Measuring reproducibility
of high-throughput experiments. The annals of applied statistics, 2011,
vol. 5, no 3, p. 1752-1779.

Given a list of peak calls in NarrowPeaks format and the corresponding peak
call for the merged replicate. This tool computes and appends a IDR column to
NarrowPeaks files.
"""

import numpy as np
import midr.archimedean as archimedean
import matplotlib.pyplot as plt


def pdf_copula_plot(lower, upper,
                    copula,
                    pdf_function,
                    params_list,
                    u_values=np.array([
                        [0.42873569, 0.18285458, 0.9514195],
                        [0.25148149, 0.05617784, 0.3378213],
                        [0.79410993, 0.76175687, 0.0709562],
                        [0.02694249, 0.45788802, 0.6299574],
                        [0.39522060, 0.02189511, 0.6332237],
                        [0.66878367, 0.38075101, 0.5185625],
                        [0.90365653, 0.19654621, 0.6809525],
                        [0.28607729, 0.82713755, 0.7686878],
                        [0.22437343, 0.16907646, 0.5740400],
                        [0.66752741, 0.69487362, 0.3329266]
                    ]),
                    min_y=None):
    """
    :param lower:
    :param upper:
    :param copula:
    :param pdf_function:
    :param params_list:
    :param u_values:
    :return:
    """
    bx, ax = plt.subplots()
    ax.plot(
        np.linspace(
                start=lower,
                stop=upper,
                num=100
            ),
        list(
            map(lambda x: pdf_function(
                x,
                u_values=u_values,
                copula=copula,
                params_list=params_list
            ), np.linspace(
                start=lower,
                stop=upper,
                num=100
            )
            )
        )
    )
    if min_y is not None:
        plt.axvline(x=min_y)
    ax.set(
        xlabel='theta', ylabel='log pdf', title=copula
    )
    plt.show()

