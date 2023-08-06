#!/usr/bin/python3

"""Compute the Irreproducible Discovery Rate (IDR) from NarrowPeaks files

This section of the project provides facilitites to handle NarrowPeaks files
and compute IDR on the choosen value in the NarrowPeaks columns
"""

from scipy.stats import rankdata
import numpy as np
import midr.log as log


def randomize_equality(x_score):
    """
    function to randomize equal rank
    :param rank:
    :param method:
    :return:
    >>> np.random.seed(123)
    >>> randomize_equality(np.array([1,2,2,3,4,5,5,5,6,7,7,7,7,7,8]))
    array([1.        , 2.        , 2.5       , 3.        , 4.        ,
           5.        , 5.33333333, 5.66666667, 6.        , 7.        ,
           7.2       , 7.4       , 7.6       , 7.8       , 8.        ])
    >>> rankdata(np.array([1,2,2,3,4,5,5,5,6,7,7,7,7,7,8]),
    ... method="ordinal")
    array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])
    >>> rankdata(np.array([9.1,1.1,2.1,3.1,4.1,5.1,6.1,7.1,8.1]),
    ... method="ordinal")
    array([9, 1, 2, 3, 4, 5, 6, 7, 8])
    >>> randomize_equality(np.array([9.1,1.1,2.1,3.1,4.1,5.1,6.1,7.1,8.1]))
    array([9., 1., 2., 3., 4., 5., 6., 7., 8.])
    >>> randomize_equality(np.array([1,1,1,3,20,1,1,2]))
    array([1. , 1.2, 1.4, 3. , 4. , 1.6, 1.8, 2. ])
    """
    rank = rankdata(x_score, method="dense").astype(float)
    is_unique, index, inverse, counts = np.unique(
        rank,
        return_index=True,
        return_counts=True,
        return_inverse=True
    )
    index = index[counts > 1]
    counts = counts[counts > 1]
    for i in range(len(index)):
        np.random.shuffle(
            rank[rank == rank[index[i]]]
        )
        rank[rank == rank[index[i]]] = np.linspace(
            start=rank[index[i]],
            stop=rank[index[i]] + 1,
            endpoint=False,
            num=counts[i]
        )

    return rank


def compute_rank(x_score, missing=None):
    """
    transform x a n*m matrix of score into an n*m matrix of rank ordered by
    row.
    >>> np.random.seed(123)
    >>> compute_rank(np.array([[0,0],[10,30],[20,20],[30,10]]))
    array([[1., 1.],
           [2., 4.],
           [3., 3.],
           [4., 2.]])
    >>> compute_rank(np.array(
    ...    [[0,1],
    ...     [10,1],
    ...     [20,20],
    ...     [30,1],
    ...     [40,1],
    ...     [50,2]]
    ... ))
    array([[1.  , 1.  ],
           [2.  , 1.25],
           [3.  , 3.  ],
           [4.  , 1.5 ],
           [5.  , 1.75],
           [6.  , 2.  ]])
    >>> compute_rank(np.array([[0,0],[10,30],[20,20],[30,10]]), missing=0)
    array([[0., 0.],
           [1., 3.],
           [2., 2.],
           [3., 1.]])
    """
    np.random.seed(123)
    log.logging.info(
        "computing rank for %i by %i matrix",
        x_score.shape[0],
        x_score.shape[1]
    )
    rank = np.empty_like(x_score.astype(float))
    for i in range(x_score.shape[1]):
        # we want the rank to start at 1
        if missing is None:
            rank[:, i] = randomize_equality(x_score[:, i])
        else:
            non_missing = np.where(~(x_score[:, i] == missing))[0]
            rank[non_missing, i] = randomize_equality(
                x_score[non_missing, i]
            )
            rank[np.where((x_score[:, i] == missing))[0], i] = missing
    return rank


def scale_rank(rank, gaussian=False):
    """
    function to scale rank between 0 an 1
    :param rank:
    :param gaussian:
    :return:
    >>> np.random.seed(123)
    >>> x = np.random.rand(5, 10)
    >>> r = compute_rank(x)
    >>> r[:, 1]
    array([2., 4., 5., 3., 1.])
    >>> scale_rank(r)[:, 1]
    array([0.33333333, 0.66666667, 0.83333333, 0.5       , 0.16666667])
    >>> scale_rank(randomize_equality(
    ... np.array([1,2,2,3,4,5,5,5,6,7,7,7,7,7,8])))
    array([0.0625    , 0.125     , 0.15625   , 0.1875    , 0.25      ,
           0.3125    , 0.33333333, 0.35416667, 0.375     , 0.4375    ,
           0.45      , 0.4625    , 0.475     , 0.4875    , 0.5       ])
    >>> scale_rank(rankdata(
    ... np.array([1,2,2,3,4,5,5,5,6,7,7,7,7,7,8]),
    ... method="ordinal"))
    array([0.0625, 0.125 , 0.1875, 0.25  , 0.3125, 0.375 , 0.4375, 0.5   ,
           0.5625, 0.625 , 0.6875, 0.75  , 0.8125, 0.875 , 0.9375])
    """
    if gaussian:
        scaling_factor = 0.99
        return(
            (1.0 - (rank - 1.0) / float(rank.shape[0])) * scaling_factor
        )
    return rank / (float(rank.shape[0]) + 1.0)



def compute_empirical_marginal_cdf(rank, gaussian=False, missing=None):
    """
    normalize ranks to compute empirical marginal cdf and scale by n / (n+1)

    >>> r = compute_rank(np.array(
    ...    [[0.1,0.1],
    ...    [10.0,30.0],
    ...    [20.0,20.0],
    ...    [30.0,10.0]]))
    >>> compute_empirical_marginal_cdf(r, gaussian=True)
    array([[0.99  , 0.99  ],
           [0.7425, 0.2475],
           [0.495 , 0.495 ],
           [0.2475, 0.7425]])
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
    if gaussian:
        return(scale_rank(
            rank=rank,
            gaussian=gaussian
        ))
    else:
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
