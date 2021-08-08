#!/usr/bin/python3

import argparse
import pandas as pd

parser = argparse.ArgumentParser(
    description = "Calculate Jaccard distances with different approches"
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

    sim_mat = list()
    instances = list(binarized_martix.columns)

    for n1 in instances:
        for n2 in instances:
            ds = skm.pairwise.distance.jaccard(binarized_martix[n1], binarized_martix[n2])
            distances.append((n1, n2, ds))

    sim_mat = pd.DataFrame(sim_mat)
    sim_mat.head()

    return sim_mat


def main(
    input_path: str,
    output_path: str = "jaccard_similarity_matrix.csv",
    approach: str = "scikit"
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
    Returns
    -------
    None
    """

    scores = pd.read_csv(input_path)
    sim_mat = calculate_jaccard(scores, approach=approach)
    sim_mat.write_csv(output_path)
    return


if __name__ == '__main__':
    main()