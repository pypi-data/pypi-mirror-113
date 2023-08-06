#!/usr/bin/python3

"""Compute the Irreproducible Discovery Rate (IDR) from NarrowPeaks files

This section of the project provides facilitites to handle NarrowPeaks files
and compute IDR on the choosen value in the NarrowPeaks columns
"""

from scipy.stats import rankdata
from scipy.spatial.distance import pdist, squareform
import numpy as np
import midr.log as log


def randomize_rank_equality(rank, delta=0.4):
    """
    detect equality in a vector or rank and randomize them between the rank
    and the rank + delta
    >>> randomize_rank_equality(np.array([9.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0]))
    array([9., 1., 2., 3., 4., 5., 6., 7., 8.])
    >>> randomize_rank_equality(np.array([1.0,1.0,1.0,3.0,20.0,1.0,1.0,2.0]))
    array([ 1.32,  1.  ,  1.16,  3.  , 20.  ,  1.24,  1.08,  2.  ])
    >>> randomize_rank_equality(np.array([1.0,2.0,2.0,2.0,20.0,1.0,1.0,2.0]))
    array([ 1.        ,  2.1       ,  2.        ,  2.2       , 20.        ,
            1.26666667,  1.13333333,  2.3       ])
    """
    rng = np.random.default_rng(seed=123)
    unique, unique_index, unique_counts = np.unique(
        rank,
        return_index=True,
        return_counts=True,
    )
    unique_index = unique_index[unique_counts > 1]
    unique_counts = unique_counts[unique_counts > 1]
    for i in range(len(unique_index)):
        distinct_rank = np.linspace(
            start=rank[unique_index[i]],
            stop=rank[unique_index[i]] + delta,
            endpoint=False,
            num=unique_counts[i]
        )
        rng.shuffle(distinct_rank)
        rank[rank == rank[unique_index[i]]] = distinct_rank
    return rank


def compute_rank(x_score, missing=None, randomize_equality=True):
    """
    transform x a n*m matrix of score into an n*m matrix of rank ordered by
    row.
    >>> np.random.seed(123)
    >>> compute_rank(np.array(
    ...    [[0,0,3],
    ...     [10,30,5],
    ...     [20,20,3],
    ...     [30,10,2]]
    ... ))
    array([[1. , 1. , 2. ],
           [2. , 4. , 3. ],
           [3. , 3. , 2.2],
           [4. , 2. , 1. ]])
    >>> compute_rank(np.array(
    ...    [[0,1,3],
    ...     [10,1,1],
    ...     [20,20,6],
    ...     [30,1,8],
    ...     [40,1,3],
    ...     [50,2,7]]
    ... ))
    array([[1. , 1. , 2. ],
           [2. , 1.2, 1. ],
           [3. , 3. , 3. ],
           [4. , 1.3, 5. ],
           [5. , 1.1, 2.2],
           [6. , 2. , 4. ]])
    >>> compute_rank(np.array(
    ...    [[0,1,3],
    ...     [10,1,0],
    ...     [20,0,6],
    ...     [0,1,8],
    ...     [40,1,3],
    ...     [50,2,7]]
    ...     ),
    ...     missing=0.0
    ... )
    array([[0. , 1. , 1. ],
           [1. , 1.2, 0. ],
           [2. , 0. , 2. ],
           [0. , 1.3, 4. ],
           [3. , 1.1, 1.2],
           [4. , 2. , 3. ]])
    """
    log.logging.info(
        "computing rank for %i by %i matrix",
        x_score.shape[0],
        x_score.shape[1]
    )
    if missing is None:
        rank = rankdata(
            x_score,
            method="dense",
            axis=0
        ).astype(float)
        if randomize_equality:
            return np.apply_along_axis(
                func1d=randomize_rank_equality,
                axis=0,
                arr=rank
            )
        return rank

    rank = np.empty_like(x_score, dtype="float64")
    for i in range(x_score.shape[1]):
        non_missing = np.where(~(x_score[:, i] == missing))[0]
        rank[non_missing, i] = rankdata(
            x_score[non_missing, i],
            method="dense",
            axis=0
        )
        if randomize_equality:
            rank[non_missing, i] = randomize_rank_equality(
                rank[non_missing, i]
            )
        rank[np.where((x_score[:, i] == missing))[0], i] = missing
    return rank


def scale_rank(rank):
    """
    function to scale rank between 0 an 1
    :param rank:
    :return
    >>> np.random.seed(123)
    >>> x = np.random.rand(5, 10)
    >>> r = compute_rank(x)
    >>> r[:, 1]
    array([2., 4., 5., 3., 1.])
    >>> scale_rank(r)[:, 1]
    array([0.33333333, 0.66666667, 0.83333333, 0.5       , 0.16666667])
    >>> scale_rank(rankdata(
    ... np.array([1,2,2,3,4,5,5,5,6,7,7,7,7,7,8]),
    ... method="ordinal"))
    array([0.0625, 0.125 , 0.1875, 0.25  , 0.3125, 0.375 , 0.4375, 0.5   ,
           0.5625, 0.625 , 0.6875, 0.75  , 0.8125, 0.875 , 0.9375])
    """
    return rank / (float(rank.shape[0]) + 1.)



def compute_empirical_marginal_cdf(rank, missing=None):
    """
    normalize ranks to compute empirical marginal cdf and scale by n / (n+1)

    >>> r = compute_rank(np.array(
    ...    [[0.1,0.1],
    ...    [10.0,30.0],
    ...    [20.0,20.0],
    ...    [30.0,10.0]]))
    >>> r = compute_rank(np.array(
    ...    [[0.0,0.0],
    ...    [10.0,30.0],
    ...    [20.0,20.0],
    ...    [30.0,10.0]]))
    >>> compute_empirical_marginal_cdf(r)
    array([[0.2, 0.2],
           [0.4, 0.8],
           [0.6, 0.6],
           [0.8, 0.4]])
    >>> r = compute_rank(np.array(
    ...    [[0.0,0.0],
    ...    [0.1,0.1],
    ...    [10.0,30.0],
    ...    [20.0,20.0],
    ...    [30.0,10.0]]), missing=0.0)
    >>> compute_empirical_marginal_cdf(r, missing=0.0)
    array([[0. , 0. ],
           [0.2, 0.2],
           [0.4, 0.8],
           [0.6, 0.6],
           [0.8, 0.4]])
    """
    log.logging.info(
        "scale rank to ecdf for %i by %i matrix",
        rank.shape[0],
        rank.shape[1]
    )
    if missing is None:
        return(scale_rank(
            rank=rank
        ))
    else:
        log.logging.info(
            "excluding missing values from ecdf computation"
        )
        for i in range(rank.shape[1]):
            non_missing = np.where(~(rank[:, i] == missing))[0]
            rank[non_missing, i] = scale_rank(
                rank=rank[non_missing, i]
            )
            rank[np.where((rank[:, i] == missing))[0], i] = missing
    return rank


def benjamini_hochberg(p_vals):
    """
    compute fdr from pvalues
    :param p_vals:
    :return:
    """
    log.logging.info(
        "ajusting p.values with BH method",
    )
    ranked_p_values = rankdata(p_vals)
    fdr = p_vals * len(p_vals) / ranked_p_values
    fdr[fdr > 1] = 1
    return fdr
