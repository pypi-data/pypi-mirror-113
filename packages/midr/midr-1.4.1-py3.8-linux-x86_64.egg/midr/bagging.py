#!/usr/bin/python3

"""Compute the Irreproducible Discovery Rate (IDR) from NarrowPeaks files

This section of the project provides facilitites to compute bagging statistics
with samics
"""

import numpy as np
import midr.samic as samic
import multiprocessing as mp
from progress.bar import IncrementalBar
import midr.log as log


def sampling(u_values, size=5):
    """
    function to create u_values subset with replacement
    :param size:
    :param u_values:
    :return:
    >>> from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
    >>> np.random.seed(123)
    >>> sample=sampling(
    ...     u_values=compute_empirical_marginal_cdf(
    ...     compute_rank(np.random.rand(10, 30))),
    ...     size=5
    ... )
    >>> sample.shape
    (10, 5)
    >>> np.random.seed(123)
    >>> np.array_equal(sample, sampling(
    ...     u_values=compute_empirical_marginal_cdf(
    ...     compute_rank(np.random.rand(10, 30))),
    ...     size=5
    ... ))
    True
    """
    return u_values[:,
           np.random.choice(
               a=range(u_values.shape[1]),
               replace=True,
               size=size
           )]


def sampling_list(u_values, sample_number=100, size=5):
    """
    return a list of sample from the original data
    :param u_values:
    :param sample_number:
    :param size:
    :return:
    >>> from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
    >>> sample=sampling_list(
    ...     u_values=compute_empirical_marginal_cdf(
    ...     compute_rank(np.random.rand(10, 30))),
    ...     sample_number=2,
    ...     size=5
    ... )
    >>> len(sample)
    2
    >>> sample[0].shape
    (10, 5)
    """
    return list(map(
        lambda x: sampling(u_values=u_values, size=size),
        list(range(sample_number))
    ))


def sample_optim(u_values, threshold=None, missing=None, bar=None):
    """
    run samic optim over a sample list
    :param threshold:
    :param missing:
    :param u_values:
    :param bar:
    :return:
    >>> from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
    >>> np.random.seed(123)
    >>> u_values = compute_empirical_marginal_cdf(
    ...     compute_rank(np.random.rand(10, 30)))
    >>> sample = sampling(
    ...         u_values=u_values,
    ...         size=5
    ...     )
    >>> sample_optim(sample)
    {'order': {'clayton': 0, 'frank': 1, 'gumbel': 2}, 'clayton': {'theta': 2.574646028595966, 'theta_old': 2.574646028595966}, 'frank': {'theta': 4.0, 'theta_old': 4.0}, 'gumbel': {'theta': 4.675600282065307, 'theta_old': 4.675600282065307}, 'threshold': 0.1, 'missing': None, 'k_state': array([-0.12572988, -0.10669844, -0.09403262, -0.08277888, -0.09807342,
           -0.06364165, -0.11937129, -0.21287957, -0.30805684, -0.12903043]), 'l_state': array([[-3.61067412e+01, -9.41508612e+01,  0.00000000e+00],
           [-3.31152190e+01, -9.53364737e+01, -4.44089210e-15],
           [-3.31591700e+01, -9.55656884e+01, -3.55271368e-15],
           [-3.60458362e+01, -9.44459108e+01,  0.00000000e+00],
           [-3.30515748e+01, -9.51990876e+01, -4.44089210e-15],
           [-3.39906306e+01, -9.50652613e+01, -1.77635684e-15],
           [-3.56701740e+01, -9.41345227e+01,  0.00000000e+00],
           [-3.41576266e+01, -9.44936799e+01, -1.77635684e-15],
           [-3.37148634e+01, -9.42639516e+01, -1.77635684e-15],
           [-3.56968201e+01, -9.39807192e+01,  0.00000000e+00]]), 'pi': -0.13171208538051093, 'pi_old': -0.0250533852083632, 'alpha': array([-3.38921958e+01, -9.45293261e+01, -1.77635684e-15]), 'alpha_old': array([-3.32292846e+01, -9.26358452e+01, -3.55271368e-15]), 'dcopula': array([[-31.08536301, -90.36005271,   5.68428941],
           [-27.92001148, -91.37183593,   5.85811866],
           [-27.83115885, -91.46824705,   5.99092228],
           [-30.58464658, -90.21529092,   6.12410082],
           [-27.76769106, -91.14577359,   5.94679494],
           [-28.25685063, -90.56205113,   6.39669112],
           [-30.59365442, -90.28857288,   5.73943072],
           [-29.70764289, -91.27426599,   5.11289485],
           [-29.68408952, -91.46374743,   4.69368502],
           [-30.70303962, -90.21750843,   5.65669163]])}
    """
    if bar is not None:
        bar.next()
    return samic.samic_optim(
            u_values=u_values,
            threshold=threshold,
            missing=missing
        )


def sample_optim_list(sample_list, threshold=None, missing=None, bar=None):
    """
    run samic optim over a sample list
    :param threshold:
    :param missing:
    :param sample_list:
    :param bar:
    :return:
    >>> from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
    >>> u_values = compute_empirical_marginal_cdf(
    ...     compute_rank(np.random.rand(10, 30)))
    >>> sample_list=[
    ...     sampling(
    ...         u_values=u_values,
    ...         size=5
    ...     ),
    ...     sampling(
    ...         u_values=u_values,
    ...         size=5
    ...     )]
    >>> len(list(sample_optim_list(sample_list)))
    2
    """
    return list(map(lambda u_values: sample_optim(
            u_values=u_values,
            threshold=threshold,
            missing=missing,
            bar=bar),
            list(sample_list)))


def sample_idr(u_values, results_list, missing=None):
    """
    compute idr for each sample
    :param missing:
    :param u_values:
    :param results_list:
    :return:
    >>> from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
    >>> np.random.seed(123)
    >>> u_values = compute_empirical_marginal_cdf(
    ...     compute_rank(np.random.rand(10, 30)))
    >>> sample_list = sampling_list(
    ...         u_values=u_values,
    ...         sample_number=2,
    ...         size=3
    ...     )
    >>> results_list = sample_optim_list(sample_list)
    >>> sample_idr(u_values, results_list)
    [array([0.00000000e+00, 0.00000000e+00, 2.13162821e-14, 0.00000000e+00,
           0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
           0.00000000e+00, 0.00000000e+00]), array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])]
    """
    return list(map(
        lambda params_list: samic.local_idr(
            u_values=u_values,
            params_list=params_list,
            missing=missing
        ),
        list(results_list)
    ))


def averaging(idr_list, sample_number=None):
    """
    compute the average idr accross sample
    :param sample_number:
    :param idr_list:
    :return:
    >>> from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
    >>> from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
    >>> np.random.seed(123)
    >>> u_values = compute_empirical_marginal_cdf(
    ...     compute_rank(np.random.rand(10, 30)))
    >>> sample_list = sampling_list(
    ...         u_values=u_values,
    ...         sample_number=2,
    ...         size=3
    ...     )
    >>> results_list = sample_optim_list(sample_list)
    >>> idr_list = sample_idr(u_values, results_list)
    >>> averaging(idr_list)
    array([0.0000000e+00, 0.0000000e+00, 1.0658141e-14, 0.0000000e+00,
           0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
           0.0000000e+00, 0.0000000e+00])
    >>> averaging(np.concatenate(idr_list), sample_number=2)
    array([0.0000000e+00, 0.0000000e+00, 1.0658141e-14, 0.0000000e+00,
           0.0000000e+00, 0.0000000e+00, 0.0000000e+00, 0.0000000e+00,
           0.0000000e+00, 0.0000000e+00])
    """
    if isinstance(idr_list, list):
        return np.mean(np.stack(list(idr_list), axis=1), axis=1)
    else:
        return np.mean(np.reshape(idr_list, (sample_number, -1)), axis=0)


def samic_worker(queue: mp.JoinableQueue, u_values, size,
                 sample_number, results_idr_list,
                 threshold, missing):
    """

    :param sample_number:
    :param queue:
    :param u_values:
    :param size:
    :param results_idr_list:
    :param threshold:
    :param missing:
    :param bar:
    :return:
    """
    bar = IncrementalBar(
        'sampling',
        max=sample_number,
        suffix='%(percent)d%% [%(elapsed_td)s / %(eta_td)s]'
    )
    while not queue.empty():
        sample = queue.get()
        results_idr_list[
            sample * u_values.shape[0]:(sample * u_values.shape[0] +
                                        u_values.shape[0])
        ] = sample_idr(
            u_values=u_values,
            results_list=[sample_optim(
                u_values=sampling(
                    u_values=u_values,
                    size=size
                ),
                threshold=threshold,
                missing=missing,
                bar=bar
            )]
        )[0]
        queue.task_done()
        bar.goto(sample_number - queue.qsize())
    bar.finish()


def samic_bagging_mono(u_values, sample_number=1000, size=5, threshold=None,
                  missing=None):
    """
    baggin procedure for samics
    :param threshold:
    :param missing:
    :param u_values:
    :param sample_number:
    :param size:
    :return:
    >>> from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
    >>> np.random.seed(123)
    >>> u_values = compute_empirical_marginal_cdf(
    ...     compute_rank(np.random.rand(10, 30)))
    >>> res = samic_bagging_mono(
    ...     u_values=u_values,
    ...     sample_number=10,
    ...     size=3
    ... )
    >>> res
    array([2.13162821e-15, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
           0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.21502808e-13,
           0.00000000e+00, 0.00000000e+00])
    """
    bar = IncrementalBar(
        'sampling',
        max=sample_number,
        suffix='%(percent)d%% [%(elapsed_td)s / %(eta_td)s]'
    )
    bar.start()
    res = averaging(
        idr_list=sample_idr(
            u_values=u_values,
            results_list=sample_optim_list(
                sample_list=sampling_list(
                    u_values=u_values,
                    sample_number=sample_number,
                    size=size
                ),
                threshold=threshold,
                missing=missing,
                bar=bar
            )
        )
    )
    bar.finish()
    return res


def samic_bagging_mp(u_values, sample_number=1000, size=5, threshold=None,
                       missing=None, cpu=2):
    """
    baggin procedure for samics
    :param threshold:
    :param missing:
    :param u_values:
    :param sample_number:
    :param size:
    :param cpu:
    :return:
    >>> from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
    >>> np.random.seed(123)
    >>> u_values = compute_empirical_marginal_cdf(
    ...     compute_rank(np.random.rand(10, 30)))
    >>> res = samic_bagging_mp(
    ...     u_values=u_values,
    ...     sample_number=10,
    ...     size=3,
    ...     cpu=2
    ... )
    >>> len(res)
    10
    """
    queue = mp.JoinableQueue()
    shared_idr_list = mp.Array(
        'd',
        [0.0] * len(u_values) * sample_number,
        lock=False
    )
    list(map(lambda x: queue.put(x), range(sample_number)))
    worker = map(
        lambda x: mp.Process(
            target=samic_worker,
            args=(queue, u_values, size, sample_number, shared_idr_list,
                  threshold, missing),
            name="samic_worker_" + str(x),
            daemon=True
        ),
        range(cpu)
    )
    list(map(lambda x: x.start(), worker))
    queue.join()
    list(map(lambda x: x.join(), worker))
    return averaging(
        shared_idr_list,
        sample_number=sample_number
    )


def samic_bagging(u_values, threshold=None,
                  missing=None, cpu=1, sample_number=1000, size=3):
    """
    baggin procedure for samics
    :param threshold:
    :param missing:
    :param u_values:
    :param sample_number:
    :param size:
    :param cpu:
    :return:
    >>> from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
    >>> np.random.seed(123)
    >>> u_values = compute_empirical_marginal_cdf(
    ...     compute_rank(np.random.rand(10, 30)))
    >>> np.random.seed(123)
    >>> res = samic_bagging(
    ...     u_values=u_values,
    ...     sample_number=100,
    ...     size=3,
    ...     cpu=1
    ... )
    >>> res
    array([9.42677048e-13, 2.59348099e-15, 1.30616865e-07, 1.91190134e-07,
           7.98417662e-07, 1.81586991e-07, 9.00605067e-08, 1.51530840e-10,
           5.30687725e-08, 1.98382209e-07])
    >>> np.random.seed(123)
    >>> res3 = samic_bagging(
    ...     u_values=u_values,
    ...     sample_number=100,
    ...     size=3,
    ...     cpu=1
    ... )
    >>> res3
    array([9.42677048e-13, 2.59348099e-15, 1.30616865e-07, 1.91190134e-07,
           7.98417662e-07, 1.81586991e-07, 9.00605067e-08, 1.51530840e-10,
           5.30687725e-08, 1.98382209e-07])
    >>> np.array_equiv(res, res3)
    True
    """
    if cpu == 1:
        return samic_bagging_mono(
            u_values=u_values,
            sample_number=sample_number,
            size=size,
            threshold=threshold,
            missing=missing
        )
    else:
        return samic_bagging_mp(
            u_values=u_values,
            sample_number=sample_number,
            size=size,
            threshold=threshold,
            missing=missing,
            cpu=cpu
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
