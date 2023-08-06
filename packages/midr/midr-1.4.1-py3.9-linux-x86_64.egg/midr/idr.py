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

from copy import deepcopy
import multiprocessing as mp
from scipy.stats import norm
from scipy.stats import multivariate_normal
from scipy.stats import bernoulli
from scipy.optimize import brentq
import numpy as np
import midr.log as log
from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank


def cov_matrix(m_sample, theta):
    """
    compute multivariate_normal covariance matrix

    >>> cov_matrix(3, {'rho':0.5, 'sigma':1.})
    array([[1. , 0.5, 0.5],
           [0.5, 1. , 0.5],
           [0.5, 0.5, 1. ]])
    >>> cov_matrix(4, {'rho':0.5, 'sigma':2.})
    array([[2., 1., 1., 1.],
           [1., 2., 1., 1.],
           [1., 1., 2., 1.],
           [1., 1., 1., 2.]])
    >>> cov_matrix(3, {'rho':0., 'sigma':1.})
    array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]])
    """
    cov = np.full(
        shape=(m_sample, m_sample),
        fill_value=theta['rho'] * theta['sigma']
    )
    np.fill_diagonal(a=cov, val=theta['sigma'])
    return cov


def sim_multivariate_gaussian(n_value, m_sample, theta):
    """
    draw from a multivariate Gaussian distribution

    >>> sim_multivariate_gaussian(10, 2, \
        {'mu': 1, 'rho': 0.5, 'sigma': 1}).shape
    (10, 2)
    >>> np.mean(sim_multivariate_gaussian(10000, 1, \
         {'mu': 1, 'rho': 0.5, 'sigma': 1})[:,0]) > 0.9
    True
    >>> np.mean(sim_multivariate_gaussian(10000, 1, \
         {'mu': 1, 'rho': 0.5, 'sigma': 1})[:,0]) < 1.1
    True
    >>> np.var(sim_multivariate_gaussian(10000, 1, \
        {'mu': 1, 'rho': 0.5, 'sigma': 1})[:,0]) > 0.9
    True
    >>> np.var(sim_multivariate_gaussian(10000, 1, \
        {'mu': 1, 'rho': 0.5, 'sigma': 1})[:,0]) < 1.1
    True
    """
    return np.random.multivariate_normal(
        mean=[float(theta['mu'])] * int(m_sample),
        cov=cov_matrix(
            m_sample=m_sample,
            theta=theta
        ),
        size=int(n_value)
    )


def sim_m_samples(n_value, m_sample,
                  theta_0,
                  theta_1):
    """
    simulate sample where position score are drawn from two different
    multivariate Gaussian distribution

    >>> sim_m_samples(100, 4, THETA_INIT, THETA_INIT)['X'].shape
    (100, 4)
    >>> len(sim_m_samples(100, 4, THETA_INIT, THETA_INIT)['K'])
    100
    """
    k_state = bernoulli.rvs(p=theta_1['pi'], size=n_value) == 1
    scores = sim_multivariate_gaussian(
        n_value=n_value,
        m_sample=m_sample,
        theta=theta_0
    )
    scores[k_state, :] = sim_multivariate_gaussian(
        n_value=n_value,
        m_sample=m_sample,
        theta=theta_1
    )[k_state, :]
    return {'X': scores, 'K': np.array(k_state, dtype="float64")}


def g_function(z_values, theta):
    """
    compute scalded Gaussian cdf for Copula
    >>> THETA_0 = {'mu': 0., 'sigma': 1., 'rho': .0}
    >>> THETA_TEST = {'pi': .5, 'mu': -1., 'sigma': .8, 'rho': .65}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=1000,
    ...                      m_sample=1,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> np.mean(g_function(DATA["X"], THETA_TEST))
    0.5087722962779593
    >>> np.min(g_function(DATA["X"], THETA_TEST))
    0.0005859929003354202
    >>> np.max(g_function(DATA["X"], THETA_TEST))
    0.9985775573884005
    """
    return (1. - theta['pi']) * norm.cdf(z_values) + \
           theta['pi'] * norm.cdf(
               z_values,
               loc=theta['mu'],
               scale=np.sqrt(theta['sigma'])
           )


def compute_grid(theta,
                 function=g_function,
                 size=1000,
                 z_start=-4.0,
                 z_stop=4.0):
    """
    compute a grid of function(z_values) from z_start to z_stop
    :param function: function
    :param theta: function parameters
    :param size: size of the grid
    :param z_start: start of the z_values
    :param z_stop: stop of the z_values
    :return: pd.array of 'z_values' paired with 'u_values'

    >>> compute_grid(
    ...    theta={'pi': 0.4, 'mu': -4.0, 'sigma': 2.0, 'rho': 0.0},
    ...    size=4
    ... )
    array([[-4.        ,  0.14144036],
           [-1.33333333,  0.32917659],
           [ 1.33333333,  0.82809301],
           [ 4.        ,  0.88282371]])
    """
    zu_grid = np.zeros((size, 2))
    zu_grid[:, 0:] = np.linspace(
        start=z_start,
        stop=z_stop,
        num=size
    ).reshape((size, 1))
    zu_grid[:, 1] = function(zu_grid[:, 0], theta=theta)
    return zu_grid


def optim_function(x, u_value, theta):
    return g_function(z_values=x, theta=theta) - u_value


def grid_optim_function(i, theta, grid, u_values):
    a_loc = np.argwhere(grid[:, 1] <= u_values[i])
    if len(a_loc) >=1:
        a_val = grid[0, 0]
    else:
        a_val = grid[0, 0]

    b_loc = np.argwhere(grid[:, 1] >= u_values[i])
    if len(b_loc) >= 1:
        b_val = grid[b_loc[0], 0]
    else:
        b_val = grid[-1, 0]
    try:
        return brentq(
            f=lambda x: optim_function(x, u_value=u_values[i], theta=theta),
            a=a_val,
            b=b_val,
            maxiter=500
        )
    except ValueError as err:
        log.logging.error(err)
        raise Exception(
            "a = " + str(a_val) + " b = " + str(b_val) +
            " f(a) = " + str(optim_function(a_val, u_values[i], theta)) +
            " f(b) = " +
            str(optim_function(b_val, u_values[i], theta))
        )
        quit(-1)


def z_from_u_worker(q: mp.JoinableQueue, theta, grid, u_values, z_values):
    """
    z_from_u unit function in case of multiprocessing
    :param q:
    :param theta:
    :param grid:
    :param u_values:
    :param z_values:
    :return:
    """
    while not q.empty():
        i = q.get()
        z_values[i] = grid_optim_function(
            i=i,
            theta=theta,
            grid=grid,
            u_values=u_values
        )
        q.task_done()


def z_from_u(u_values, theta, grid, thread_num=mp.cpu_count()):
    """
    Compute z_values from u_values
    :param u_values: list of u_values
    :param theta:
    :param grid:
    :param thread_num
    :return: list of z_value
    >>> z_from_u(
    ...    u_values=np.array([0.2, 0.3, 0.5, 0.9]),
    ...    theta=THETA_INIT,
    ...    grid=compute_grid(
    ...        theta=THETA_INIT,
    ...        size=20
    ...    ),
    ...    thread_num=1
    ... )
    array([-1.91958191, -1.16136202, -0.26120387,  1.78220351])
    >>> np.random.seed(124)
    >>> u_values = compute_empirical_marginal_cdf(
    ...     compute_rank(
    ...         x_score=np.random.rand(10, 2)
    ...     ),
    ...     gaussian=True
    ... )
    >>> z_values = z_from_u(
    ...    u_values=u_values[:, 0],
    ...    theta=THETA_INIT,
    ...    grid=compute_grid(
    ...        theta=THETA_INIT,
    ...        size=4
    ...    ),
    ...    thread_num=1
    ... )
    >>> z_values[1:5]
    array([-1.01076666,  0.01372315, -3.77171831,  0.32779407])
    >>> z_values[-5:]
    array([-1.52156265, -0.29615119, -0.62615832,  1.10287609, -2.34134437])
    """
    z_values = np.zeros_like(u_values)
    if thread_num <= 1:
        for i in range(u_values.shape[0]):
            z_values[i] = grid_optim_function(
                i=i,
                theta=theta,
                grid=grid,
                u_values=u_values
            )
    else:
        q = mp.JoinableQueue()
        shared_z_values = mp.Array('f', [0.0] * len(u_values), lock=False)
        list(map(lambda x: q.put(x), range(len(u_values))))
        worker = map(
            lambda x: mp.Process(
                target=z_from_u_worker,
                args=(q, theta, grid, u_values,
                      shared_z_values),
                name="z_from_u_" + str(x),
                daemon=True
            ),
            range(thread_num)
        )
        list(map(lambda x: x.start(), worker))
        q.join()
        list(map(lambda x: x.join(), worker))
        z_values = list(shared_z_values)
    return z_values


def compute_z_from_u(u_values, theta, thread_num=mp.cpu_count()):
    """
    compute u_ij from z_ij via the G_j function

    >>> r = compute_rank(np.array([[0.0,0.0],[10.0,30.0],\
        [20.0,20.0],[30.0,10.0]]))
    >>> u = compute_empirical_marginal_cdf(r, gaussian=True)
    >>> theta = {'mu': -1., 'rho': 0.5, 'sigma': 1., 'pi': 0.5}
    >>> a_val = norm.ppf(
    ...        np.amin(u),
    ...        loc=np.min([theta['mu'], 0.]),
    ...        scale=np.max([theta['sigma'], 1.])
    ...    )
    >>> b_val = norm.ppf(
    ...        np.amax(u),
    ...        loc=0.,
    ...        scale=np.max([theta['sigma'], 1.])
    ...    )
    >>> ( np.min(u),  np.amax(u))
    (0.17999999999999997, 0.7200000000000001)
    >>> (a_val, b_val)
    (-1.9153650878428143, 0.5828415072712165)
    >>> (g_function(a_val, theta), g_function(b_val, theta))
    (0.10386149006018075, 0.8316356016305612)
    >>> compute_z_from_u(u, theta, 0)
    array([[ 0.15910461,  0.15910461],
           [-0.38620075, -1.53226449],
           [-0.90586907, -0.90586907],
           [-1.53226449, -0.38620075]])
    >>> THETA_TEST_0 = {'pi': None, 'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> THETA_TEST_1 = {'pi': 0.8, 'mu': -4.0, 'sigma': 1.0, 'rho': 0.75}
    >>> np.random.seed(123)
    >>> r = compute_rank(sim_m_samples(n_value=1000,
    ...                      m_sample=3,
    ...                      theta_0=THETA_TEST_0,
    ...                      theta_1=THETA_TEST_1)['X'])
    >>> u = compute_empirical_marginal_cdf(r, gaussian=True)
    >>> compute_z_from_u(u, THETA_INIT, 0)
    array([[ 0.42207767,  0.79792502, -0.34918235],
           [-0.19279405,  0.38038396, -0.59488065],
           [-1.54845198, -1.58387401, -1.54845198],
           ...,
           [-1.39491792, -1.29129009, -1.33059224],
           [-0.66685913, -0.67718836, -1.21533348],
           [ 0.60311139,  0.02555373, -0.36976484]])
    """
    grid = compute_grid(
        theta=theta,
        size=np.min([1000, u_values.shape[0]]),
        z_start=norm.ppf(
           np.amin(u_values),
           loc=np.min(np.array([theta['mu'], 0.], dtype='float64')),
           scale=np.max(np.array([theta['sigma'], 1.], dtype='float64'))
        ),
        z_stop=6.
    )
    z_values = np.empty_like(u_values)
    for j in range(u_values.shape[1]):
        z_values[:, j] = z_from_u(
            u_values=u_values[:, j],
            theta=theta,
            grid=grid,
            thread_num=thread_num
        )
    return z_values


def h_function(z_values, theta):
    """
    compute the pdf of h0 or h1
    >>> THETA_TEST = {'pi': 1., 'mu': -2., 'sigma': .8, 'rho': 1.}
    >>> THETA_0 = {'mu': 0., 'sigma': 1., 'rho': 0.}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=5,
    ...                      m_sample=2,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> h_function(DATA["X"], THETA_TEST)
    array([0.23458101, 0.31287712, 0.02758982, 0.28298741, 0.10303476])
    """
    try:
        x_values = multivariate_normal.pdf(
            x=z_values,
            mean=np.repeat(theta['mu'], z_values.shape[1]),
            cov=cov_matrix(m_sample=z_values.shape[1], theta=theta),
            allow_singular=True
        )
        return x_values
    except ValueError as err:
        log.logging.exception("%s", "error: h_function: " + str(err))
        log.logging.exception("%s", str(theta))


def e_step_k(z_values, theta):
    """
    compute expectation of Ki
    >>> THETA_TEST = {'pi': 0.45, 'mu': 2.0, 'sigma': 1.0, 'rho': 0.65}
    >>> THETA_0 = {'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> np.random.seed(125)
    >>> DATA = sim_m_samples(n_value=1000,
    ...                      m_sample=4,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> np.mean(e_step_k(DATA["X"], THETA_TEST))
    0.459918592433911
    """
    h0_x = h_function(
        z_values=z_values,
        theta={'mu': 0., 'sigma': 1., 'rho': 0.}
    )
    h1_x = h_function(
        z_values=z_values,
        theta=theta
    )
    return (theta['pi'] * h1_x) / (
            theta['pi'] * h1_x + (1. - theta['pi']) * h0_x)


def local_idr(z_values, theta):
    """
    compute local IDR
    >>> THETA_TEST = {'pi': 0.2, 'mu': 2.0, 'sigma': 3.0, 'rho': 0.65}
    >>> THETA_0 = {'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> np.random.seed(124)
    >>> DATA = sim_m_samples(n_value=1000,
    ...                      m_sample=4,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> np.mean(local_idr(DATA["X"], THETA_TEST))
    0.811613378958856
    """
    return 1.0 - e_step_k(z_values=z_values, theta=theta)


def m_step_pi(k_state, threshold):
    """
    compute maximization of pi
    >>> THETA_TEST = {'pi': 0.35, 'mu': 2.0, 'sigma': 1.0, 'rho': 1.0}
    >>> THETA_0 = {'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=10000,
    ...                      m_sample=2,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> m_step_pi(DATA['K'], 0.001)
    0.3489
    """
    pi = np.sum(k_state, axis=0) / np.float(k_state.shape[0])
    if pi <= threshold:
        log.logging.error(
            "%s %f %s",
            "warning: pi (=",
            pi,
            ") maximization, empty reproducible group"
        )
        return threshold
    if pi >= 1. - threshold:
        log.logging.error(
            "%s %f %s",
            "warning: pi (=",
            pi,
            ") maximization, empty non-reproducible group"
        )
        return 1. - threshold
    return pi


def m_step_mu(z_values, k_state):
    """
    compute maximization of mu
    0 < mu
    >>> THETA_TEST = {'pi': 0.5, 'mu': 2.0, 'sigma': 1.0, 'rho': 1.0}
    >>> THETA_0 = {'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=10000,
    ...                      m_sample=2,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> m_step_mu(DATA["X"], DATA['K'])
    2.0046228298266615
    """
    denominator = np.float(z_values.shape[1]) * np.sum(k_state)
    numerator = np.multiply(
            k_state,
            np.sum(z_values, axis=1)
        )
    mu = np.divide(np.sum(numerator, axis=0), denominator)
    if mu <= 0.:
        log.logging.error(
            "%s %f %s",
            "warning: mu (=",
            mu,
            ") invalid mu value (mu > 0.)"
        )
        return 1.
    return mu


def m_step_sigma(z_values, k_state, theta):
    """
    compute maximization of sigma
    >>> THETA_TEST = {'pi': 0.5, 'mu': 2.0, 'sigma': 2.0, 'rho': 0.5}
    >>> THETA_0 = {'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=10000,
    ...                      m_sample=5,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> m_step_sigma(DATA["X"], DATA["K"], THETA_TEST)
    2.004740224529242
    """
    denominator = np.float(z_values.shape[1]) * np.sum(k_state)
    numerator = np.power(z_values - theta['mu'], 2.)
    numerator = np.multiply(
        k_state,
        np.sum(numerator, axis=1)
    )
    return np.divide(np.sum(numerator, axis=0), denominator)


def m_step_rho(z_values, k_state, theta):
    """
    compute maximization of rho
    0 < rho <= 1
    >>> THETA_TEST = {'pi': 1.0, 'mu': 2.0, 'sigma': 2.0, 'rho': 0.5}
    >>> THETA_0 = {'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=1000,
    ...                      m_sample=4,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> m_step_rho(DATA["X"], DATA["K"], THETA_TEST)
    0.49927437775263406
    """
    denominator = np.float(z_values.shape[1]) ** 2.
    denominator -= np.float(z_values.shape[1])
    denominator *= theta['sigma'] * np.sum(k_state)
    s_numerator = z_values - theta['mu']
    numerator = np.zeros_like(s_numerator)
    for j in range(z_values.shape[1]):
        for k in range(z_values.shape[1]):
            if k != j:
                numerator[:, j] += np.multiply(
                    s_numerator[:, j],
                    s_numerator[:, k]
                )
    numerator = np.multiply(np.sum(numerator, axis=1), k_state)
    rho = np.divide(
        np.sum(numerator, axis=0),
        denominator
    )
    if rho < 0. or rho > 1.:
        log.logging.error(
            "%s %f %s",
            "warning: rho (=",
            rho,
            ") invalid rho value (rho in [0., 1.])"
        )
        return 1.
    return rho


def loglikelihood(z_values, k_state, theta):
    """
    Compute logLikelihood of the pseudo-data
    >>> THETA_TEST = {'pi': 0.2, 'mu': 2.0, 'sigma': 3.0, 'rho': 0.65}
    >>> THETA_0 = {'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=10,
    ...                      m_sample=2,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> loglikelihood(DATA["X"], np.random.rand(10, 1), THETA_TEST)
    array([-53.48393122])
    """
    i = 0
    try:
        h0_x = np.log(1. - theta['pi']) + np.log(h_function(
            z_values=z_values,
            theta={'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
        ))
        h1_x = np.log(theta['pi']) + np.log(h_function(
            z_values=z_values,
            theta=theta
        ))
        logl = 0.0
        for i in range(z_values.shape[0]):
            logl += k_state[i] * h1_x[i]
            logl += (1. - k_state[i]) * h0_x[i]
        return logl
    except ValueError as err:
        log.logging.exception("%s", "error: logLikelihood: " + str(err))
        log.logging.exception("%f", h1_x[i])
        log.logging.exception("%f", theta)
        quit(-1)
    except TypeError as err:
        log.logging.exception("%s", "error: logLikelihood: " + str(err))
        log.logging.exception("%f", h1_x[i])
        log.logging.exception("%f", theta)
        quit(-1)


def delta(theta_t0, theta_t1, threshold, logl):
    """
    compute the maximal variation between t0 and t1 for the estimated
    parameters
    """
    if logl == -np.inf:
        return True
    return any(
        abs(theta_t0[parameters] - theta_t1[parameters]) > threshold
        for parameters in theta_t0
    )


def em_pseudo_data(z_values,
                   logger,
                   theta,
                   k_state,
                   threshold=0.001):
    """
    EM optimization of theta for pseudo-data
    >>> THETA_TEST = {'pi': 0.9, 'mu': 4.0, 'sigma': 3.0, 'rho': 0.65}
    >>> THETA_0 = {'pi': None, 'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=10000,
    ...                      m_sample=5,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> (THETA_RES, KSTATE, LIDR) = em_pseudo_data(
    ...    z_values=DATA["X"],
    ...    logger={
    ...        'logl': list(),
    ...        'pi': list(),
    ...        'mu': list(),
    ...        'sigma': list(),
    ...        'rho': list(),
    ...        'pseudo_data': list()
    ...    },
    ...    theta=THETA_INIT,
    ...    k_state=DATA['K']
    ... )
    >>> THETA_RES
    {'pi': 0.9075182908224244, 'mu': 4.0089860342084265, \
'sigma': 3.066096064021097, 'rho': 0.6594029615984741}
    """
    theta_t0 = deepcopy(theta)
    theta_t1 = deepcopy(theta)
    logl_t1 = -np.inf
    while delta(theta_t0, theta_t1, threshold, logl_t1):
        del theta_t0
        theta_t0 = deepcopy(theta_t1)
        logl_t0 = logl_t1
        k_state = e_step_k(
            z_values=z_values,
            theta=theta_t1
        )
        theta_t1['pi'] = m_step_pi(
            k_state=k_state,
            threshold=threshold
        )
        theta_t1['mu'] = m_step_mu(
            z_values=z_values,
            k_state=k_state
        )
        theta_t1['sigma'] = m_step_sigma(
            z_values=z_values,
            k_state=k_state,
            theta=theta_t1
        )
        theta_t1['rho'] = m_step_rho(
            z_values=z_values,
            k_state=k_state,
            theta=theta_t1
        )
        logl_t1 = loglikelihood(
            z_values=z_values,
            k_state=k_state,
            theta=theta_t1
        )
        if logl_t1 - logl_t0 < 0.0:
            log.logging.debug(
                "%s %f",
                "warning: EM decreassing logLikelihood rho: ",
                logl_t1 - logl_t0
            )
            log.logging.debug("%s", str(theta_t1))
            return theta_t0, k_state, logger
        logger = log.add_log(
            log=logger,
            theta=theta_t1,
            logl=logl_t1,
            pseudo=False
        )
    return theta_t1, k_state, logger


def variational_em_pseudo_data(z_values,
                   logger,
                   theta,
                   k_state,
                   threshold=0.001,
                   frac=0.1):
    """
    run em_pseudo_data on frac of the data 1./frac time then average the
    theta of the 1./frac run to get the final theta
    :param z_values:
    :param logger:
    :param theta:
    :param k_state:
    :param threshold:
    :param frac:
    :return:
    >>> THETA_TEST = {'pi': 0.9, 'mu': 4.0, 'sigma': 3.0, 'rho': 0.65}
    >>> THETA_0 = {'pi': None, 'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=10000,
    ...                      m_sample=5,
    ...                      theta_0=THETA_0,
    ...                      theta_1=THETA_TEST)
    >>> (THETA_RES, KSTATE, LIDR) = variational_em_pseudo_data(
    ...    z_values=DATA["X"],
    ...    logger={
    ...        'logl': list(),
    ...        'pi': list(),
    ...        'mu': list(),
    ...        'sigma': list(),
    ...        'rho': list(),
    ...        'pseudo_data': list()
    ...    },
    ...    theta=THETA_INIT,
    ...    k_state=DATA['K']
    ... )
    >>> THETA_RES
    {'pi': 0.9070306403336345, 'mu': 4.022654642685084, \
'sigma': 3.0504173082273316, 'rho': 0.6577123392779007}
    """
    theta_t1 = deepcopy(theta)
    for param in theta_t1.keys():
        theta_t1[param] = 0.
    for run in range(np.int(np.round(1. / frac))):
        sample = np.random.choice(
            range(z_values.shape[0]),
            size=np.int(np.round(np.float(z_values.shape[0]) * frac)),
            replace=False)
        run_theta, run_k_state, logger = em_pseudo_data(
            z_values=z_values[sample, :],
            logger=logger,
            theta=theta,
            k_state=k_state[sample],
            threshold=threshold
        )
        k_state[sample] = run_k_state
        for param in theta_t1.keys():
            theta_t1[param] += run_theta[param]

    for param in theta_t1.keys():
        theta_t1[param] /= np.round(1. / frac)

    return theta_t1, k_state, logger


def pseudo_likelihood(x_score, threshold=None, missing=None, cpu=1,
                      outdir=None, randomize_equality=True):
    """
    pseudo likelhood optimization for the copula model parameters
    :param x_score np.array of score (measures x samples)
    :param threshold float min delta between every parameters between two
    iterations
    :return (theta: dict, lidr: list) with thata the model parameters and
    lidr the local idr values for each measures
    >>> THETA_TEST_0 = {'mu': 0., 'sigma': 1., 'rho': 0.}
    >>> THETA_TEST_1 = {'pi': .3, 'mu': 2., 'sigma': 1.5, 'rho': .6}
    >>> np.random.seed(123)
    >>> DATA = sim_m_samples(n_value=1000,
    ...                      m_sample=4,
    ...                      theta_0=THETA_TEST_0,
    ...                      theta_1=THETA_TEST_1)
    >>> lidr = pseudo_likelihood(DATA["X"])
    >>> np.sum((np.array(lidr) > 0.5).all() == DATA["K"]) / len(lidr)
    0.714
    >>> abs(np.sum((np.array(lidr) > 0.5).all() == DATA["K"]) / len(lidr) -
    ... (1. - THETA_TEST_1['pi'])) <= 0.1
    True
    """
    log.logging.info("%s", "computing idr")
    theta_t0 = deepcopy(THETA_INIT)
    theta_t1 = deepcopy(THETA_INIT)
    k_state = np.repeat(THETA_INIT['pi'], x_score.shape[0])
    logger = {
        'logl': list(),
        'pi': list(),
        'mu': list(),
        'sigma': list(),
        'rho': list(),
        'pseudo_data': list()
    }
    logl_t1 = -np.inf
    u_values = compute_empirical_marginal_cdf(
        compute_rank(
            x_score=x_score,
            missing=missing,
            randomize_equality=randomize_equality
        ),
        missing=missing,
    )
    if threshold is None:
        threshold = 10**-(len(str(u_values.shape[0])) - 1)
    z_values = np.zeros(u_values.shape)
    while delta(theta_t0, theta_t1, threshold, logl_t1):
        del theta_t0
        theta_t0 = deepcopy(theta_t1)
        z_values = compute_z_from_u(u_values=u_values,
                                    theta=theta_t1,
                                    thread_num=cpu)
        (theta_t1, k_state, logger) = em_pseudo_data(
            z_values=z_values,
            logger=logger,
            k_state=k_state,
            theta=theta_t1,
            threshold=threshold
        )
        logl_t1 = loglikelihood(
            z_values=z_values,
            k_state=k_state,
            theta=theta_t1
        )
        logger = log.add_log(
            log=logger,
            theta=theta_t1,
            logl=logl_t1,
            pseudo=True
        )
        log.logging.info("%s", log_idr(theta_t1))
    return local_idr(
        z_values=z_values,
        theta=theta_t1
    )


def log_idr(theta):
    """
    return str of pseudo_likelihood parameter estimate
    :param theta:
    :return:
    """
    return str(
        '{' +
        '"pi": ' + str(theta['pi']) + ', ' +
        '"mu": ' + str(theta['mu']) + ', ' +
        '"sigma": ' + str(theta['sigma']) + ', ' +
        '"rho": ' + str(theta['rho']) +
        '}'
    )


THETA_INIT = {
    'pi': .5,
    'mu': 1.,
    'sigma': .8,
    'rho': .5
}

if __name__ == "__main__":
    import doctest
    np.warnings.filterwarnings('error', category=np.VisibleDeprecationWarning)
    np.warnings.filterwarnings('error', category=np.RuntimeWarning)
    doctest.testmod()
