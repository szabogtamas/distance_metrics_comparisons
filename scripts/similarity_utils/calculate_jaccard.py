#!/usr/bin/env/python3

import argparse, sys
import numpy as np
import pandas as pd
from typing import Union
from scipy.spatial import distance as scd
from sklearn import metrics as skm
try:
    from input_parser import read_input
except:
    from .input_parser import read_input

parser = argparse.ArgumentParser(
    description = "Calculate Jaccard distances with different approches."
)
parser.add_argument(  
    "-i",
    "--input_path",
    required=True,
    type = str,
    help = "Path to input data"
)
parser.add_argument(  
    "-f",
    "--format_spec",
    default = "pseudo_tab",
    type = str,
    help = "Format of input data"
)
parser.add_argument(  
    "-m",
    "--approach",
    default = "scikit",
    type = str,
    help = "Implementation approach to use"
)
parser.add_argument(
    "-o",
    "--output_path",
    default = sys.stdout,
    type = argparse.FileType('w'),
    help = "Path to output file"
)


def dist_to_sim(
    distance_martix: np.array,
    labels: Union[None, list, tuple, pd.Series] = None
) -> pd.DataFrame:
    """
    Convert distance matrix to similarity dataframe.
    ----------
    distance_martix
        A distance matrix produced by sklearn or scipy.
    labels
        Entity labels to be shown.
    Returns
    -------
    The similarity matrix.
    """
    
    sim_mat = pd.DataFrame(distance_martix)
    N = sim_mat.shape[1]
    
    if labels is None:
        labels = ["e_" + str(x) for x in range(0, N)]
    
    if len(labels) != N:
        raise ValueError("The number of labels given does not match the number of entities in matrix")
    
    sim_mat.columns = labels
    sim_mat["Entity"] = labels
    sim_mat = sim_mat.set_index("Entity")

    return 1 - sim_mat


def jaccard_scikit(
    binarized_martix: pd.DataFrame
) -> np.array:
    """
    The native scikit function to calculate Jaccard similarity.
    ----------
    binarized_martix
        A binarized matrix with category labels in columns and entities in rows.
    Returns
    -------
    The distance matrix.
    """

    dist_mat = skm.pairwise.pairwise_distances(
        binarized_martix.to_numpy(), metric="jaccard"
    )

    return dist_mat


def jaccard_pandas(
    binarized_martix: pd.DataFrame
) -> np.array:
    """
    Hijacking the pairwise correlation tool of pandas to calculate jaccard score.
    ----------
    binarized_martix
        A binarized matrix with category labels in columns and entities in rows.
    Returns
    -------
    The distance matrix.
    """

    dist_mat = binarized_martix.T.corr(method=skm.pairwise.distance.jaccard).to_numpy()
    np.fill_diagonal(dist_mat, 0)

    return dist_mat


def jaccard_loop(
    binarized_martix: pd.DataFrame
) -> np.array:
    """
    A simple and non-efficient function calculating Jaccard similarity using for loops.
    ----------
    binarized_martix
        A binarized matrix with category labels in columns and entities in rows.
    Returns
    -------
    The distance matrix.
    """

    distances = list()
    instances = binarized_martix.index.to_list()
    tm = binarized_martix.T

    for n1 in instances:
        for n2 in instances:
            ds = scd.jaccard(tm[n1], tm[n2])
            distances.append((n1, n2, ds))
    
    dist_mat = pd.DataFrame(distances)
    dist_mat.columns = ["e1", "e2", "val"]
    dist_mat = dist_mat.pivot(index="e1", columns="e2").to_numpy()
    
    return dist_mat


def calculate_jaccard(
    binarized_martix: pd.DataFrame,
    approach: str = "scikit",
    convert_similarity: bool = False
) -> pd.DataFrame:
    """
    A wrapper around Jaccard calculator functions helping to use the appropriate approach.
    ----------
    binarized_martix
        A binarized matrix with category labels in columns and entities in rows.
    approach
        Which approach to use for calculations. One of ["scikit", "loop", "pandas"]
    Returns
    -------
    The distance / similarity matrix.
    """

    fun_router = dict(
        scikit = jaccard_scikit,
        pandas = jaccard_pandas,
        loop = jaccard_loop
    )

    if approach not in fun_router:
        approach = "scikit"

    dist_mat = fun_router[approach](binarized_martix)
    if convert_similarity:
        return(dist_to_sim(dist_mat))
    else:
        return dist_mat


def main(
    input_path: str,
    output_path: str = "jaccard_similarity_matrix.csv",
    approach: str = "scikit",
    format_spec: str = "pseudo_tab"
) -> None:
    """
    A high-level wrapper around Jaccard calculator functions.
    ----------
    input_path
        Path to input data in long or binarized matrix format.
    output_path
        Path to save output to.
    approach
        Which approach to use for calculations. One of ["scikit", "loop", "pandas"]
    format_spec
        Specifies the format of input data. One of ["pseudo_tab", "long", "binary"]
    Returns
    -------
    None
    """

    scores = read_input(input_path, format_spec=format_spec)
    sim_mat = calculate_jaccard(scores, approach=approach, convert_similarity=True)
    sim_mat.to_csv(output_path)
    return


if __name__ == '__main__':
    args = parser.parse_args()
    main(**args.__dict__)
else:
    del parser
    del argparse