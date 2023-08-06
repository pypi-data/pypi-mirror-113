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
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


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
                    min_y=None,
                    outdir="log"):
    """
    :param outdir:
    :param min_y:
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
        xlabel='theta', ylabel='log pdf', title=copula + " " + str(min_y)
    )
    date_time = datetime.now()
    plt.savefig(
        str(outdir) + '/' + date_time.strftime("%b_%d_%Y_%H") + '_' +
        str(copula) + '.pdf')


def pdf_density_copula_plot(
                    pdf_function,
                    params_list,
                    copula_names,
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
                    outdir="log"):
    """
    :param outdir:
    :param copula_names:
    :param pdf_function:
    :param params_list:
    :param u_values:
    :return:
    """
    data_dcopula = pd.DataFrame()
    for copula_name in copula_names:
        data_dcopula = data_dcopula.append(
            pd.DataFrame().from_dict(
                {
                    'copula': [copula_name for i in range(60)],
                    'dcopula': list(
                        map(lambda x: pdf_function(
                            x,
                            u_values=u_values,
                            copula=copula_name,
                            params_list=params_list
                        ), np.linspace(
                            start=0.5,
                            stop=60,
                            num=60
                        )
                        )
                    )
                }
            )
        )
    print(data_dcopula)
    sns.relplot(
        data=data_dcopula,
        x="dcopula", col="copula",
        binwidth=3, height=3, facet_kws=dict(margin_titles=True)
    )
    date_time = datetime.now()
    plt.savefig(
        str(outdir) + '/' + date_time.strftime("%b_%d_%Y_%H") + '_dcopula.pdf')


class ParamsPlot:
    """
    self contained log class to make parameters evolution plots

    >>> params_list={
    ...        'pi': np.log(0.01),
    ...        'alpha': np.log([0.005, 0.005, 0.99]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': 0.0
    ...    }
    >>> my_plot = ParamsPlot(params_list=params_list, copula_names=[
    ... 'frank', 'gumbel', 'clayton'])
    >>> my_plot.update(params_list=params_list)
    """

    def __init__(self, params_list: dict, copula_names: list, outdir: str):
        """
        initalisation of a Params_plot object from a initial parameters list
        and the list of copula names
        :param params_list:
        :param copula_names:
        """
        self.copula_names = copula_names
        self.outdir = outdir
        self.params = pd.DataFrame()
        self.new_line(params_list=params_list)

    def new_line(self, params_list: dict):
        params_size = len(self.copula_names) * 2 + 1
        params_dict = {
            'times': [(self.params.shape[0] / params_size) for i in range(params_size)],
            'params': ["pi"],
            'values': [np.exp(params_list['pi'])]
        }
        for copula_name in self.copula_names:
            params_dict['params'].append(copula_name + "_alphas")
            params_dict['values'].append(
                np.exp(
                    params_list["alpha"][params_list["order"][copula_name]]
                )
            )
            params_dict['params'].append(copula_name + "_thetas")
            params_dict['values'].append(
                params_list[copula_name]["theta"]
            )
        if self.params.shape[0] == 0:
            self.params = pd.DataFrame.from_dict(params_dict)
        else:
            self.params = self.params.append(
                pd.DataFrame.from_dict(params_dict), ignore_index=True
            )

    def update(self, params_list: dict):
        self.new_line(params_list=params_list)
        self.plot()

    def plot(self):
        sns.relplot(
            data=self.params,
            x="times", y="values",
            col="params",
            hue="params",
            kind="line"
        )
        date_time = datetime.now()
        plt.savefig(
            str(self.outdir) + '/' + date_time.strftime("%b_%d_%Y_%H") +
            '_parameters.pdf'
        )



if __name__ == "__main__":
    import doctest
    doctest.testmod()