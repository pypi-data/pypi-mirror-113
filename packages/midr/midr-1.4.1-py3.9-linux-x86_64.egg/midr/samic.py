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

from scipy.optimize import minimize_scalar
from scipy.optimize import minimize
from scipy.stats import bernoulli
from scipy.stats import multinomial
import numpy as np
import c_archimedean as c_arch
from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
from midr.idr import sim_m_samples
import midr.log as log
import midr.archimedean as archimedean
import midr.archimediean_plots as archimediean_plots
from pathlib import PurePath
from copy import copy


def random_u(n = 1000, dim = 5, name = "clayton", theta=15):
    import rpy2
    from rpy2.robjects.packages import importr
    copula = importr("copula")
    if name == "clayton":
        u_values = copula.rCopula(
            n=n,
            copula=copula.claytonCopula(param=theta, dim=dim)
        )
        return np.array(u_values)
    if name == "frank":
        u_values = copula.rCopula(
            n=n,
            copula=copula.frankCopula(param=theta, dim=dim)
        )
        return np.array(u_values)
    if name == "gumbel":
        u_values = copula.rCopula(
            n=n,
            copula=copula.gumbelCopula(param=theta, dim=dim)
        )
        return np.array(u_values)
    exit(-1)


def mixture_archimedian(n, dim, params_list):
    from scipy.stats import multinomial
    l_state = multinomial.rvs(n=1, p=params_list['alpha'], size=n) == 1
    score = np.zeros((n, dim))
    for copula in copula_names():
        score[l_state[:, params_list['order'][copula]], :] = random_u(
            n=n,
            dim=dim,
            name=copula,
            theta=params_list[copula]['theta']
        )[l_state[:, params_list['order'][copula]], :]
    return score


def random_mix(n, dim, params_list):
    k_state = bernoulli.rvs(p=params_list['pi'], size=n) == 1
    scores = np.random.rand(n, dim)
    scores[k_state, :] = mixture_archimedian(
        n=n,
        dim=dim,
        params_list=params_list
    )[k_state, :]
    return {'X': scores, 'K': np.array(k_state, dtype="float64")}

COPULA_DENSITY = {
    'gumbel': c_arch.pdf_gumbel,
    'clayton': c_arch.pdf_clayton,
    'frank': archimedean.pdf_frank
}
DMLE_COPULA = {
    'clayton': archimedean.dmle_copula_clayton,
    'frank': archimedean.dmle_copula_frank,
    # 'frank': lambda x: 15.0,
    'gumbel': archimedean.dmle_copula_gumbel
}


def copula_density(copula, u_values, theta, is_log=False):
    """
    return a copula density function
    :param copula:
    :return:
    >>> u_values = np.random.rand(10000,30)
    >>> np.count_nonzero(
    ...     ~np.isnan(
    ...         copula_density('clayton',
    ...             u_values = u_values,
    ...             theta = 6.0,
    ...             is_log = True
    ... )))
    10000
    >>> u_values = np.random.rand(10000,30)
    >>> np.count_nonzero(
    ...     ~np.isnan(
    ...         copula_density('frank',
    ...             u_values = u_values,
    ...             theta = 6.0,
    ...             is_log = True
    ... )))
    10000
    """
    return np.nan_to_num(
        COPULA_DENSITY[copula](u_values, theta, is_log),
        copy=False,
        nan=0.0,
        posinf=0.0,
        neginf=0.0
    )


def copula_number():
    """
    return the number of archimedean copula
    :return:
    """
    return len(COPULA_DENSITY)


def copula_names():
    """
    return the name of the copula density functions
    :return:
    """
    return COPULA_DENSITY.keys()


def dmle_copula(copula):
    """
    return a dmle copula density function
    :param copula:
    :return:
    """
    return np.nan_to_num(DMLE_COPULA[copula], copy=False)


def number_of_missing(u_values, missing=None):
    """
    return number of missing value per row
    :param u_values:
    :param missing:
    :return:
    >>> number_of_missing(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    missing=0.0
    ... )
    array([0, 1, 0, 0, 2, 0, 0, 1, 0, 0])
    """
    return np.sum(u_values == missing, axis=1)


def remove_missing(u_values, missing=None, nb_missing=0):
    """

    :param u_values:
    :param missing:
    :return:
    >>> remove_missing(np.array([
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    ]),
    ...    missing=0.0,
    ...    nb_missing=1,
    ... )
    array([[0.25148149, 0.3378213 , 0.3378213 ],
           [0.82713755, 0.7686878 , 0.7686878 ]])
    """
    return np.reshape(
        u_values[~(u_values == missing)],
        (u_values.shape[0], u_values.shape[1] - nb_missing)
    )


def list_of_u_values(u_values, missing=None):
    """
    return number of missing value per row
    :param u_values:
    :param missing:
    :return:
    >>> list_of_u_values(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    missing=0.0
    ... )
    (array([0, 1, 0, 0, 2, 0, 0, 1, 0, 0]), [array([[0.42873569, 0.18285458, 0.9514195 , 0.9514195 ],
           [0.79410993, 0.76175687, 0.0709562 , 0.0709562 ],
           [0.02694249, 0.45788802, 0.6299574 , 0.6299574 ],
           [0.66878367, 0.38075101, 0.5185625 , 0.5185625 ],
           [0.90365653, 0.19654621, 0.6809525 , 0.6809525 ],
           [0.22437343, 0.16907646, 0.57404   , 0.57404   ],
           [0.66752741, 0.69487362, 0.3329266 , 0.3329266 ]]), array([[0.25148149, 0.3378213 , 0.3378213 ],
           [0.82713755, 0.7686878 , 0.7686878 ]]), array([[0.3952206, 0.6299574]]), array([], shape=(0, 1), dtype=float64)])
    """
    nb_missing_row = number_of_missing(u_values=u_values, missing=missing)
    list_u_values = [remove_missing(
                u_values=u_values[nb_missing_row == nb_missing, :],
                missing=missing,
                nb_missing=nb_missing
            ) for nb_missing in range(u_values.shape[1])]
    return (nb_missing_row, list_u_values)


def censored_copula_density(u_values, theta, copula, missing=None):
    """
    compute pdf of copula for censored data
    :param u_values:
    :param theta:
    :param copula:
    :param missing:
    :return:
    >>> np.exp(censored_copula_density(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    theta=6,
    ...    copula="frank",
    ...    missing=0.0
    ... ))
    array([0.01076583, 3.20545269, 0.02025168, 0.0171356 , 1.02461261,
           3.06315388, 0.02965913, 4.78125626, 0.65824184, 0.90881984])
    >>> np.exp(censored_copula_density(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.3378213, 0.3378213, 0.0],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.0, 0.39522060, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    theta=6,
    ...    copula="frank",
    ...    missing=0.0
    ... ))
    array([0.01076583, 3.20545269, 0.02025168, 0.0171356 , 1.02461261,
           3.06315388, 0.02965913, 4.78125626, 0.65824184, 0.90881984])
    >>> np.exp(censored_copula_density(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    theta=2,
    ...    copula="gumbel",
    ...    missing=0.0
    ... ))
    array([6.06628394e-03, 2.58088497e+00, 6.63892197e-02, 5.72009627e-02,
           1.11589049e+00, 2.90817712e+00, 7.62035940e-02, 6.16647093e+00,
           1.08801162e+00, 1.22184286e+00])
    >>> np.exp(censored_copula_density(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    theta=2,
    ...    copula="clayton",
    ...    missing=0.0
    ... ))
    array([3.50439735e-02, 3.68342742e+00, 7.46301436e-03, 6.54688263e-06,
           1.10049896e+00, 2.61709390e+00, 5.40124152e-02, 3.30222057e+00,
           6.27832609e-01, 1.25018803e+00])
    """
    if missing is None:
        return copula_density(
            copula,
            u_values=u_values,
            theta=theta,
            is_log=True
        )
    (nb_missing_row, list_u_values) = list_of_u_values(
        u_values=u_values,
        missing=missing
    )
    cdensity = np.zeros(u_values.shape[0])
    for nb_missing in range(u_values.shape[1]):
        cdensity[nb_missing_row == nb_missing] = copula_density(
            copula,
            u_values=list_u_values[nb_missing],
            theta=theta,
            is_log=True
        )
    return cdensity


def delta(params_list, threshold):
    """
    Return true if the difference between two iteration of samic if less than
    the threhsold
    :param params_list: list of model parameters
    :param threshold: flood withe the minimal difference to reach
    :return: bool
    >>> delta(
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'pi_old': np.log(0.8),
    ...        'alpha': np.array(np.log([0.3333, 0.3333, 0.3333])),
    ...        'alpha_old': np.array(np.log([0.3333, 0.3333, 0.3333])),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'clayton': {'theta': 8, 'pi': 0.2, 'theta_old': 6, 'pi_old': 2.3}
    ...    },
    ...    threshold=0.1
    ... )
    True
    >>> delta(
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'pi_old': np.log(0.8),
    ...        'alpha': np.array(np.log([0.3333, 0.3333, 0.3333])),
    ...        'alpha_old': np.array(np.log([0.3333, 0.3333, 0.3333])),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2}
    ...    },
    ...    threshold=0.1
    ... )
    False
    """
    max_delta = [
        max(abs(np.exp(params_list['alpha']) -
                np.exp(params_list['alpha_old']))),
        abs(np.exp(params_list['pi']) - np.exp(params_list['pi_old'])),
    ]
    for copula in copula_names():
        max_delta.append(
            abs(params_list[copula]['theta'] -
                params_list[copula]['theta_old'])
        )
    return max(max_delta) >= threshold


def expectation_k(u_values, params_list, dcopula=None):
    """
    compute proba for each copula mix to describe the data
    :param u_values:
    :param params_list:
    :param dcopula:
    :return:
    >>> np.exp(expectation_k(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... ))
    array([0.00724737, 0.12708761, 0.00081767, 0.00660034, 0.00861115,
           0.18035533, 0.00356172, 0.00996085, 0.08777781, 0.05167504])
    >>> u_values = np.random.rand(10000,30)
    >>> np.count_nonzero(~np.isnan(expectation_k(u_values,
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... )))
    10000
    >>> np.random.seed(123)
    >>> u_values = np.random.rand(10,5)
    >>> np.exp(expectation_k(u_values * u_values,
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... ))
    array([0.05334154, 0.01773934, 0.22080577, 0.11382547, 0.43456438,
           0.66661805, 0.507021  , 0.00266574, 0.02776513, 0.00915402])
    """
    if dcopula is None:
        dcopula = np.zeros((u_values.shape[0], copula_number()))
        for copula in copula_names():
            dcopula[:,
                list(copula_names()).index(copula)
            ] = partial_loglikelihood_copula(
                    u_values=u_values,
                    copula=copula,
                    params_list=params_list
                )
    k_state = archimedean.lsum(dcopula, is_log=True, axis=1)
    return (
        k_state + np.log(1.0 - np.exp(params_list['pi'])) -
        np.log(
            np.exp(params_list['pi']) + (1.0 - np.exp(params_list['pi'])) *
            np.exp(k_state)
        )
    )


def expectation_l(u_values, params_list, dcopula=None):
    """
    compute proba for each copula mix to describe the data
    :param u_values:
    :param params_list:
    :param dcopula:
    :return:
    >>> np.sum(np.exp(expectation_l(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... )), axis=1)
    array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])
    >>> np.exp(expectation_l(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... ))
    array([[9.99241613e-01, 5.13503781e-07, 7.57873317e-04],
           [9.84106292e-01, 1.58920980e-02, 1.61032426e-06],
           [9.99999854e-01, 1.41403781e-07, 5.09198107e-09],
           [9.99993441e-01, 6.55870887e-06, 1.00492585e-12],
           [9.99993118e-01, 6.88235836e-06, 1.72340850e-13],
           [5.77654946e-01, 1.12341237e-01, 3.10003817e-01],
           [9.99788543e-01, 8.08002235e-07, 2.10648992e-04],
           [9.94643749e-01, 2.06163638e-05, 5.33563491e-03],
           [8.68352025e-01, 8.87728833e-02, 4.28750915e-02],
           [9.43093479e-01, 5.21635253e-03, 5.16901688e-02]])

    >>> u_values = np.random.rand(10000,30)
    >>> np.count_nonzero(~np.isnan(expectation_l(u_values,
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... )))
    30000
    """
    l_state = np.zeros((u_values.shape[0], copula_number()))
    if dcopula is None:
        dcopula = partial_loglikelihood_theta(
            u_values=u_values,
            params_list=params_list
        )
    for copula in copula_names():
        l_state[:, params_list['order'][copula]] = (
                dcopula[:, params_list['order'][copula]] -
                archimedean.lsum(dcopula, is_log=True, axis=1)
            )
    return l_state


def partial_loglikelihood_copula(u_values, copula, params_list):
    """
    pdf of the samic mixture for a given copula
    :param u_values:
    :param copula:
    :param params_list:
    :return:
    >>> np.exp(partial_loglikelihood_copula(
    ...    u_values = np.array([
    ...       [0.42873569, 0.18285458, 0.9514195],
    ...       [0.25148149, 0.05617784, 0.3378213],
    ...       [0.79410993, 0.76175687, 0.0709562],
    ...       [0.02694249, 0.45788802, 0.6299574],
    ...       [0.39522060, 0.02189511, 0.6332237],
    ...       [0.66878367, 0.38075101, 0.5185625],
    ...       [0.90365653, 0.19654621, 0.6809525],
    ...       [0.28607729, 0.82713755, 0.7686878],
    ...       [0.22437343, 0.16907646, 0.5740400],
    ...       [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    copula = 'frank',
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... ))
    array([0.02917896, 0.57310548, 0.00327336, 0.02657659, 0.03474353,
           0.50843079, 0.0142948 , 0.0400287 , 0.33422576, 0.20555988])
    >>> u_values = np.random.rand(10000,30)
    >>> np.count_nonzero(~np.isnan(partial_loglikelihood_copula(u_values,
    ...    copula = 'frank',
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... )))
    10000
    >>> u_values = np.random.rand(10000,30)
    >>> np.count_nonzero(~np.isnan(partial_loglikelihood_copula(u_values,
    ...    copula = 'gumbel',
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... )))
    10000
    >>> u_values = np.random.rand(10000,30)
    >>> np.count_nonzero(~np.isnan(partial_loglikelihood_copula(u_values,
    ...    copula = 'clayton',
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... )))
    10000
    """
    return params_list['alpha'][params_list['order'][copula]] + \
        censored_copula_density(
            u_values=u_values,
            theta=params_list[copula]['theta'],
            copula=copula,
            missing=params_list['missing']
        )


def partial_loglikelihood_theta(u_values, params_list):
    """
    pdf of the samic mixture for a given copula
    :param u_values:
    :param params_list:
    :return:

    >>> np.exp(partial_loglikelihood_theta(
    ...    u_values = np.array([
    ...       [0.42873569, 0.18285458, 0.9514195],
    ...       [0.25148149, 0.05617784, 0.3378213],
    ...       [0.79410993, 0.76175687, 0.0709562],
    ...       [0.02694249, 0.45788802, 0.6299574],
    ...       [0.39522060, 0.02189511, 0.6332237],
    ...       [0.66878367, 0.38075101, 0.5185625],
    ...       [0.90365653, 0.19654621, 0.6809525],
    ...       [0.28607729, 0.82713755, 0.7686878],
    ...       [0.22437343, 0.16907646, 0.5740400],
    ...       [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... ))
    array([[2.91789605e-02, 1.49948785e-08, 2.21307392e-05],
           [5.73105482e-01, 9.25494385e-03, 9.37790632e-07],
           [3.27335992e-03, 4.62865538e-10, 1.66678892e-11],
           [2.65765927e-02, 1.74309277e-07, 2.67076801e-14],
           [3.47435253e-02, 2.39119037e-07, 5.98776988e-15],
           [5.08430787e-01, 9.88786536e-02, 2.72854038e-01],
           [1.42948001e-02, 1.15526733e-08, 3.01182210e-06],
           [4.00287013e-02, 8.29690299e-07, 2.14728677e-04],
           [3.34225756e-01, 3.41683824e-02, 1.65024776e-02],
           [2.05559880e-01, 1.13697404e-03, 1.12665660e-02]])
    >>> u_values = np.random.rand(10000,30)
    >>> np.count_nonzero(~np.isnan(partial_loglikelihood_theta(u_values,
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... )))
    30000
    """
    dcopula = np.zeros((u_values.shape[0], copula_number()))
    for copula in copula_names():
        dcopula[:, params_list['order'][copula]] = \
            partial_loglikelihood_copula(
                u_values=u_values,
                copula=copula,
                params_list=params_list
            )
    return dcopula


def loglikelihood_theta(theta, u_values, copula, params_list, dcopula=None):
    """
    pdf of the samic mixture for a given copula
    :param u_values:
    :param copula:
    :param theta:
    :param dcopula:
    :param params_list:
    :return:
    >>> loglikelihood_theta(
    ...    theta=2,
    ...    u_values = np.array([
    ...       [0.42873569, 0.18285458, 0.9514195],
    ...       [0.25148149, 0.05617784, 0.3378213],
    ...       [0.79410993, 0.76175687, 0.0709562],
    ...       [0.02694249, 0.45788802, 0.6299574],
    ...       [0.39522060, 0.02189511, 0.6332237],
    ...       [0.66878367, 0.38075101, 0.5185625],
    ...       [0.90365653, 0.19654621, 0.6809525],
    ...       [0.28607729, 0.82713755, 0.7686878],
    ...       [0.22437343, 0.16907646, 0.5740400],
    ...       [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    copula = "frank",
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... )
    1.4747355660553325
    >>> loglikelihood_theta(
    ...    theta=2,
    ...    u_values = np.array([
    ...       [0.42873569, 0.18285458, 0.9514195],
    ...       [0.25148149, 0.05617784, 0.3378213],
    ...       [0.79410993, 0.76175687, 0.0709562],
    ...       [0.02694249, 0.45788802, 0.6299574],
    ...       [0.39522060, 0.02189511, 0.6332237],
    ...       [0.0, 0.38075101, 0.5185625],
    ...       [0.66878367, 0.38075101, 0.5185625],
    ...       [0.90365653, 0.19654621, 0.6809525],
    ...       [0.28607729, 0.82713755, 0.7686878],
    ...       [0.22437343, 0.16907646, 0.5740400],
    ...       [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    copula = "frank",
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': 0.0
    ...    }
    ... )
    1.4072509026421054
    >>> loglikelihood_theta(
    ...    theta=2,
    ...    u_values = np.array([
    ...       [0.42873569, 0.18285458, 0.9514195],
    ...       [0.25148149, 0.05617784, 0.3378213],
    ...       [0.79410993, 0.76175687, 0.0709562],
    ...       [0.02694249, 0.45788802, 0.6299574],
    ...       [0.39522060, 0.02189511, 0.6332237],
    ...       [0.0, 0.38075101, 0.5185625],
    ...       [0.66878367, 0.38075101, 0.5185625],
    ...       [0.90365653, 0.19654621, 0.6809525],
    ...       [0.28607729, 0.82713755, 0.7686878],
    ...       [0.22437343, 0.16907646, 0.5740400],
    ...       [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    copula = "clayton",
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': 0.0
    ...    }
    ... )
    1.3944790628903807
    >>> loglikelihood_theta(
    ...    theta=2,
    ...    u_values = np.array([
    ...       [0.42873569, 0.18285458, 0.9514195],
    ...       [0.25148149, 0.05617784, 0.3378213],
    ...       [0.79410993, 0.76175687, 0.0709562],
    ...       [0.02694249, 0.45788802, 0.6299574],
    ...       [0.39522060, 0.02189511, 0.6332237],
    ...       [0.0, 0.38075101, 0.5185625],
    ...       [0.66878367, 0.38075101, 0.5185625],
    ...       [0.90365653, 0.19654621, 0.6809525],
    ...       [0.28607729, 0.82713755, 0.7686878],
    ...       [0.22437343, 0.16907646, 0.5740400],
    ...       [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    copula = "gumbel",
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': 0.0
    ...    }
    ... )
    1.2126174989266756
    """
    if dcopula is None:
        dcopula = partial_loglikelihood_theta(
            u_values=u_values,
            params_list=params_list
        )
    dcopula[:, params_list['order'][copula]] = (
        params_list['alpha'][params_list['order'][copula]] +
        censored_copula_density(
            u_values=u_values,
            theta=theta,
            copula=copula,
            missing=params_list['missing']
        )
    )
    return -np.sum(
        np.log(
            np.exp(params_list['pi']) +
            (1 - np.exp(params_list['pi'])) *
            archimedean.explsum(dcopula, is_log=True, axis=1)
        ),
        axis=0
    )


def local_idr(u_values, params_list, missing=None):
    """
    Compute local idr for the samic method
    :param u_values:
    :param params_list:
    :return:
    >>> local_idr(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... )
    array([0.99275263, 0.87291239, 0.99918233, 0.99339966, 0.99138885,
           0.81964467, 0.99643828, 0.99003915, 0.91222219, 0.94832496])
    """
    return 1.0 - np.exp(
        expectation_k(u_values=u_values, params_list=params_list)
    )


def minimize_alpha(l_state):
    """
    compute maximization of alpha
    >>> u_values = np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ... ])
    >>> l_state = expectation_l(u_values=u_values,
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... )
    >>> np.exp(minimize_alpha(l_state))
    array([0.93668671, 0.02222581, 0.04108749])
    >>> np.round(np.sum(np.exp(minimize_alpha(l_state))), decimals=4)
    1.0
    >>> u_values = np.random.rand(10000,30)
    >>> l_state = expectation_l(u_values=u_values,
    ...    params_list={
    ...        'pi': np.log(0.8),
    ...        'alpha': np.log([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... )
    >>> np.round(np.sum(np.exp(minimize_alpha(l_state))), decimals=4)
    1.0
    """
    return archimedean.lsum(l_state, is_log=True, axis=0) - np.log(
        float(l_state.shape[0]))


def build_bounds(copula, eps=1e-4):
    """
    return set of bound for a given copula
    :param copula:
    :param eps:
    :return:
    >>> build_bounds("frank")
    (0.0001, 744.9999)
    >>> build_bounds("clayton")
    (0.0001, 999.9999)
    >>> build_bounds("gumbel")
    (1.0001, 99.9999)
    """
    thetas = {
        'clayton': {
            'theta_min': 0.0,
            'theta_max': 1000.0
        },
        'frank': {
            'theta_min': 0.0,
            'theta_max': 745.0
        },
        'gumbel': {
            'theta_min': 1.0,
            'theta_max': 100
        }
    }
    return (
        thetas[copula]['theta_min'] + eps, thetas[copula]['theta_max'] - eps
    )


def minimize_pi(k_state):
    """
    find theta that minimize the likelihood of the copula density
    :param k_state:
    :return:
    >>> THETA_TEST = {'pi': 0.35, 'mu': 2.0, 'sigma': 1.0, 'rho': 1.0}
    >>> THETA_0 = {'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=10000,
    ...                      m_sample=2,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> np.exp(minimize_pi(np.log(DATA['K'])))
    0.3488999999999998
    >>> np.random.seed(123)
    >>> np.exp(minimize_pi(
    ...     k_state = np.log(np.random.rand(10000, 1))))
    0.4982311453103447
    """
    return min([
        archimedean.lsum(k_state, is_log=True, axis=0)[0] - float(
        np.log(len(k_state))),
        np.log(1.0 - 1e-14)
        ]
    )


def minimize_theta(u_values, copula, params_list, dcopula=None,
                   threshold=1e-10, optim=None, outdir="log"):
    """
    find theta that minimize the likelihood of the copula density
    :param u_values:
    :param copula:
    :param params_list:
    :param dcopula:
    :return:
    >>> import rpy2
    >>> from rpy2.robjects.packages import importr
    >>> copula = base = importr("copula")
    >>> u_values = copula.rCopula(
    ...    n=1000,
    ...    copula=copula.claytonCopula(param=15, dim = 5)
    ... )
    >>> np.round(minimize_theta(
    ...     np.array(u_values),
    ...     copula="clayton",
    ...     params_list={
    ...        'pi': np.log(0.01),
    ...        'alpha': np.log([0.0, 1., 0.]),
    ...        'order': {'frank': 2, 'gumbel': 0, 'clayton': 1},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... ))
    15.0
    >>> u_values = copula.rCopula(
    ...    n=1000,
    ...    copula=copula.frankCopula(param=12, dim = 5)
    ... )
    >>> np.round(minimize_theta(
    ...     np.array(u_values),
    ...     copula="frank",
    ...     params_list={
    ...        'pi': np.log(0.01),
    ...        'alpha': np.log([0., 0., 1.]),
    ...        'order': {'frank': 2, 'gumbel': 0, 'clayton': 1},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... ))
    12.0
    >>> u_values = copula.rCopula(
    ...    n=10000,
    ...    copula=copula.gumbelCopula(param=17, dim = 5)
    ... )
    >>> np.round(minimize_theta(
    ...     np.array(u_values),
    ...     copula="gumbel",
    ...     params_list={
    ...        'pi': np.log(0.01),
    ...        'alpha': np.log([1., 0., 0.]),
    ...        'order': {'frank': 2, 'gumbel': 0, 'clayton': 1},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... ))
    17.0
    """
    log.logging.info(
        "minimize theta for %s",
        copula
    )
    old_theta = params_list[copula]['theta']
    log.logging.debug("%s", str([build_bounds(copula)]) + " minimize() bounds")
    log.logging.debug("%s", str(old_theta) + " old_theta")
    if dcopula is None:
        dcopula = partial_loglikelihood_theta(
            u_values=u_values,
            params_list=params_list
        )
    if optim is None:
        res = minimize(
            fun=loglikelihood_theta,
            args=(u_values, copula, params_list, dcopula),
            x0=old_theta,
            bounds=[build_bounds(copula)],
        )
        new_theta = res.x[0]
    else:
        if optim == "SLSQP":
            res = minimize(
                fun=loglikelihood_theta,
                x0=old_theta,
                args=(u_values, copula, params_list, dcopula),
                bounds=[build_bounds(copula)],
                method="SLSQP",
                tol=threshold
            )
            new_theta = res.x[0]
        else:
            np.seterr(over="ignore", invalid="ignore")
            res = minimize_scalar(
                fun=loglikelihood_theta,
                args=(u_values, copula, params_list, dcopula),
                bracket=build_bounds(copula),
                bounds=build_bounds(copula),
                method="brent",
                options={"xtol": threshold, "maxiter": 1000}
            )
            new_theta = res.x
    # if log.logging.root.level == log.logging.DEBUG:
    #     archimediean_plots.pdf_copula_plot(
    #         lower=build_bounds(copula)[0],
    #         upper=build_bounds(copula)[1],
    #         copula=copula,
    #         pdf_function=loglikelihood_theta,
    #         u_values=u_values,
    #         params_list=params_list,
    #         min_y=res.x,
    #         outdir=outdir
    #     )
    log.logging.debug("%s", res)
    if np.isnan(new_theta):
        log.logging.debug("%s", str(old_theta) + " new_theta = old_theta")
        return old_theta
    else:
        log.logging.debug("%s", str(new_theta) + " new_theta")
        return min(
            max(new_theta, build_bounds(copula)[0]),
            min(new_theta, build_bounds(copula)[1])
        )


def samic_init(u_values, threshold=None, missing=None, outdir=None):
    """
    initialisation function for samic procedure
    :return:
    """
    params_list = {'order': {}}
    i = 0
    for copula in copula_names():
        params_list[copula] = {
            'theta': 10.,
            'theta_old': np.nan
        }
        params_list['order'][copula] = i
        i += 1
    if threshold is None:
        params_list['threshold'] = 10**-(len(str(u_values.shape[0])) - 1)
    else:
        params_list['threshold'] = threshold
    params_list['missing'] = missing
    params_list['k_state'] = np.zeros(u_values.shape[0])
    params_list['l_state'] = np.zeros((u_values.shape[0], copula_number()))
    params_list['pi'] = np.log(0.5)
    params_list['pi_old'] = 0.0
    params_list['alpha'] = np.log(
        np.repeat(1.0 / copula_number(), copula_number())
    )
    params_list['alpha_old'] = params_list['alpha'][:]
    params_list['dcopula'] = partial_loglikelihood_theta(
        u_values=u_values,
        params_list=params_list,
    )
    params_list['outdir'] = outdir
    params_list['log_file'] = write_header(params_list)
    log.logging.info(
        "%s",
        log_samic(params_list)
    )
    return params_list


def samic_expectation(u_values, params_list):
    """
    exceptation step of the EM
    :return:
    """
    params_list['k_state'] = expectation_k(
        u_values=u_values,
        params_list=params_list,
        dcopula=params_list['dcopula'],
    )
    params_list['l_state'] = expectation_l(
        u_values=u_values,
        params_list=params_list,
        dcopula=params_list['dcopula'],
    )
    params_list['alpha_old'] = params_list['alpha'][:]
    params_list['pi_old'] = params_list['pi']
    return params_list


def samic_minimize(u_values, params_list, outdir):
    """
    minimization step of the EM
    :param outdir:
    :param u_values:
    :param params_list:
    :return:
    """
    params_list['pi'] = minimize_pi(
        k_state=params_list['k_state']
    )
    params_list['alpha'] = minimize_alpha(
        l_state=params_list['l_state']
    )
    for copula in COPULA_DENSITY:
        params_list[copula]['theta_old'] = params_list[copula]['theta']
        params_list[copula]['theta'] = minimize_theta(
            u_values=u_values,
            copula=copula,
            params_list=params_list,
            dcopula=params_list['dcopula'],
            threshold=params_list['threshold'],
            outdir=outdir
        )
        params_list['dcopula'][:, params_list['order'][copula]] = \
            partial_loglikelihood_copula(
                u_values=u_values,
                copula=copula,
                params_list=params_list,
            )
        log.logging.info(
            "%s %s",
            copula,
            log_samic(params_list)
        )
    return params_list


def variational_samic_minimize(u_values, params_list, outdir, frac=.8):
    """
    minimization step of the EM
    :param outdir:
    :param u_values:
    :param params_list:
    :return:
    """
    sample = bernoulli.rvs(p=frac, size=u_values.shape[0]) == 1
    run_params_list = copy(params_list)
    run_params_list['dcopula'] = run_params_list['dcopula'][sample, :]
    run_params_list['k_state'] = run_params_list['k_state'][sample]
    run_params_list['l_state'] = run_params_list['l_state'][sample, :]
    run_params_list = samic_minimize(
        u_values=u_values[sample, :],
        params_list=run_params_list,
        outdir=outdir
    )
    params_list['pi'] = run_params_list['pi']
    params_list['alpha'] = run_params_list['alpha']
    params_list['clayton']['theta'] = run_params_list['clayton']['theta']
    params_list['frank']['theta'] = run_params_list['frank']['theta']
    params_list['gumbel']['theta'] = run_params_list['gumbel']['theta']
    for copula in COPULA_DENSITY:
        params_list['dcopula'][:, params_list['order'][copula]] = \
            partial_loglikelihood_copula(
                u_values=u_values,
                copula=copula,
                params_list=params_list,
            )
    return params_list


def samic_optim(u_values, threshold=None, missing=None, outdir=None):
    """
    run EM to optimize model parameters
    :return:
    >>> u_values = random_mix(n=1000, dim=5, params_list={
    ...        'pi': 0.6,
    ...        'alpha': [0.4, 0.2, 0.4],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'clayton': {'theta': 6},
    ...        'frank': {'theta': 15},
    ...        'gumbel': {'theta': 4},
    ...        'missing': None
    ...    })
    >>> results = samic_optim(u_values['X'], threshold=0.01)
    >>> np.exp(results['pi'])
    >>> results['order']
    >>> np.exp(results['alpha'])
    >>> results['gumbel']['theta']
    >>> results['frank']['theta']
    >>> results['clayton']['theta']
    >>> def theta_clayton(theta):
    ...     return samic_optim(random_u(100, 5, "clayton", np.float(theta)))[
    ...     'clayton']['theta']
    >>> def theta_gumbel(theta):
    ...     return samic_optim(random_u(100, 5, "gumbel", np.float(theta)))[
    ...     'gumbel']['theta']
    >>> def theta_frank(theta):
    ...     return samic_optim(random_u(100, 5, "frank", np.float(theta)))[
    ...     'frank']['theta']
    >>> np.mean(np.array(list(map(theta_clayton, np.linspace(2., 40., 40)))
    ... ) - np.linspace(2., 40., 40)) < 1.
    True
    >>> np.mean(np.array(list(map(theta_gumbel, np.linspace(2., 40., 40)))
    ... ) - np.linspace(2., 40., 40)) < 1.
    True
    >>> np.mean(np.array(list(map(theta_frank, np.linspace(2., 40., 10)))
    ... ) - np.linspace(2., 40., 10)) < 1.
    True
    >>> theta = samic_optim(random_u(1000, 5, "clayton", 15))['clayton']['theta']
    >>> np.round(theta)
    15.0
    >>> theta = samic_optim(random_u(1000, 5, "frank", 15))['frank']['theta']
    >>> np.round(theta)
    17.0
    >>> theta = samic_optim(random_u(1000, 5, "gumbel", 15))['gumbel']['theta']
    >>> np.round(theta)
    15.0
    """
    params_list = samic_init(
        u_values=u_values,
        threshold=threshold,
        missing=missing,
        outdir=outdir
    )
    if log.logging.root.level == log.logging.DEBUG:
        params_plot = archimediean_plots.ParamsPlot(
            params_list=params_list,
            copula_names=copula_names(),
            outdir=outdir
        )
    while delta(params_list, params_list['threshold']):
        params_list = samic_expectation(
            u_values=u_values,
            params_list=params_list
        )
        params_list = samic_minimize(
            u_values=u_values,
            params_list=params_list,
            outdir=outdir
        )
        log.logging.warning(
            "%s",
            log_samic(params_list)
        )
        if log.logging.root.level == log.logging.DEBUG:
            # archimediean_plots.pdf_density_copula_plot(
            #      pdf_function=censored_copula_density,
            #      params_list=params_list,
            #      copula_names=copula_names(),
            #      u_values=u_values,
            #      outdir=outdir
            # )
            params_plot.update(params_list=params_list)
    
    if log.logging.root.level == log.logging.DEBUG:
        params_plot.plot()
    return params_list


def samic(x_score, threshold=None, missing=None, cpu=1, outdir=None,
          randomize_equality=True):
    """
    implementation of the samic method for m samples
    :param cpu:
    :param x_score np.array of score (measures x samples)
    :param threshold float min delta between every parameters between two
    iterations
    :param missing: float value equal to the value considered to be missing
    :return (theta: dict, lidr: list) with theta the model parameters and
    lidr the local idr values for each measures
    >>> THETA_TEST_0 = {'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> THETA_TEST_1 = {'pi': 0.3, 'mu': 2.0, 'sigma': 2.0, 'rho': 0.65}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=1000,
    ...                      m_sample=4,
    ...                      theta_0=THETA_TEST_0,
    ...                      theta_1=THETA_TEST_1)
    >>> lidr = samic(DATA["X"])
    >>> (np.sum((lidr < 0.5).all() == DATA["K"]) / len(lidr))
    0.714
    >>> (np.sum((lidr < 0.5).all() == DATA["K"]) / len(lidr)) - ( 1. -
    ... THETA_TEST_1['pi']) <= 0.1
    True
    """
    log.logging.info("%s", "computing idr")
    u_values = compute_empirical_marginal_cdf(
        compute_rank(
            x_score=x_score,
            missing=missing,
            randomize_equality=randomize_equality
        ),
        missing=missing,
    )
    params_list = samic_optim(
        u_values=u_values,
        threshold=threshold,
        missing=missing,
        outdir=outdir
    )
    if params_list['outdir'] is not None:
        params_list['log_file'].close()
    return local_idr(
        u_values=u_values,
        params_list=params_list,
    )


def log_samic(params_list):
    """
    return str of pseudo_likelihood parameter estimate
    :param params_list:
    :return:
    """
    write_params(params_list)
    log_str = str('{' +
                  '"pi": ' + str(np.exp(params_list['pi']))
                  )
    for copula in copula_names():
        log_str += str(
            ', \n"' + copula + '": {' +
            '"alpha": ' +
            str(np.exp(params_list['alpha'][params_list["order"][copula]])) +
            ', "theta": ' +
            str(params_list[copula]['theta']) +
            '}')
    return log_str + ' }'


def write_header(params_list):
    """
    write parameter estimation to log_file
    :param params_list:
    :return:
    """
    log_file = None
    if params_list['outdir'] is not None:
        log_file = open(
            PurePath(params_list['outdir']).joinpath("idr_params.tsv"),
            "w"
        )
        log_str = "pi"
        for copula in copula_names():
            log_str += "\t" + "alpha_" + copula
        for copula in copula_names():
            log_str += "\t" + "theta_" + copula
        log_file.write(log_str + "\n")
    return log_file


def write_params(params_list):
    """
    write parameter estimation to log_file
    :param params_list:
    :return:
    """
    log_str = str(np.exp(params_list['pi']))
    for copula in copula_names():
        log_str += "\t" + str(
            np.exp(params_list['alpha'][params_list["order"][copula]])
        )
    for copula in copula_names():
        log_str += "\t" + str(
            params_list[copula]['theta']
        )
    if params_list['outdir'] is not None:
        params_list['log_file'].write(log_str + "\n")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
