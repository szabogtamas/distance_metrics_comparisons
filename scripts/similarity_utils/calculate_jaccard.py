#!/usr/bin/python3

import argparse
import pandas as pd
from scipy.spatial import distance as scd
from sklearn import metrics as skm
from . import input_parser

parser = argparse.ArgumentParser(
    description = "Calculate Jaccard distances with different approches."
)
parser.add_argument(  
    "input_path"
    type = str,
    help = "Path to input data"
)
parser.add_argument(
    "--output_path",
    default = sys.stdout,
    type = argparse.FileType('w'),
    help = "Path to output file"
)
args = parser.parse_args()


def jaccard_scikit(
    binarized_martix: pd.DataFrame
) -> pd.DataFrame:
    """
    The native scikit function to calculate Jaccard similarity.
    ----------
    binarized_martix
        A binarized matrix with category labels in columns and entities in rows.
    Returns
    -------
    The similarity matrix.
    """

    sim_mat = skm.pairwise.pairwise_distances(
        binarized_martix.to_numpy(), metric="jaccard"
    )
    sim_mat = pd.DataFrame(sim_mat)

    return 1 - sim_mat


def jaccard_pandas(
    binarized_martix: pd.DataFrame
) -> pd.DataFrame:
    """
    Hijacking the pairwise correlation tool of pandas to calculate jaccard score.
    ----------
    binarized_martix
        A binarized matrix with category labels in columns and entities in rows.
    Returns
    -------
    The similarity matrix.
    """

    sim_mat = binarized_martix.corr(method=skm.pairwise.distance.jaccard)
    sim_mat = pd.DataFrame(sim_mat)

    return 1 - sim_mat


def jaccard_loop(
    binarized_martix: pd.DataFrame
) -> pd.DataFrame:
    """
    A simple and non-efficient function calculating Jaccard similarity using for loops.
    ----------
    binarized_martix
        A binarized matrix with category labels in columns and entities in rows.
    Returns
    -------
    The similarity matrix.
    """

    sim_mat = list()
    instances = list(binarized_martix.columns)

    for n1 in instances:
        for n2 in instances:
            ds = scd.jaccard(binarized_martix[n1], binarized_martix[n2])
            distances.append((n1, n2, ds))

    sim_mat = pd.DataFrame(sim_mat)

    return 1 - sim_mat


def calculate_jaccard(
    binarized_martix: pd.DataFrame,
    approach: str = "scikit"
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
    The similarity matrix.
    """

    fun_router = dict(
        scikit = jaccard_scikit,
        pandas = jaccard_pandas,
        loop = jaccard_loop
    )

    if approach not in fun_router:
        approach = "scikit"

    sim_mat = fun_router[aproach](binarized_martix)

    return sim_mat


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

    scores = input_parser.read_input(input_path, format_spec=format_spec)
    sim_mat = calculate_jaccard(scores, approach=approach)
    sim_mat.write_csv(output_path)
    return


if __name__ == '__main__':
    main()