#!/usr/bin/python3

import argparse
import pandas as pd

parser = argparse.ArgumentParser(
    description = "Parse and preprocess input data for Jaccard calculation."
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


def binarize_tabular(
    in_tab: pd.DataFrame
) -> pd.DataFrame:
    """
    Take a pseudo-tabular input of category labels and convert it to a binarized matrix.
    ----------
    in_tab
        Pseudo-tabular data with entity names in the first row and categies in columns.
    Returns
    -------
    The binarized matrix.
    """

    # Convert input to a dictionary to enable removing NA links
    d = in_tab.to_dict(orient="series")
    d = {k: v.dropna().tolist() for k, v in d.items()}
    # d = {k: v.dropna().apply(lambda x: "HP:" + str(x).split(".")[0]).tolist() for k, v in d.items()}

    # To find out the desired shape of the new matrix, we need all unique items
    all_items = set()
    for k, v in d.items():
        all_items = all_items | set(v)
    all_items = pd.Series(list(all_items))

    # One-hot-encode categories to create binarized matrix
    binarized_data = dict()
    for k, v in d.items():
        binarized_data[k] = [1 if e in v else 0 for e in all_items]
    binarized_data = pd.DataFrame(binarized_data)

    return binarized_data


def binarize_long(
    in_tab: pd.DataFrame
) -> pd.DataFrame:
    """
    Take a long format input of category labels and convert it to a binarized matrix.
    ----------
    in_tab
        Long foormat data with two colums: entity and its category.
    Returns
    -------
    The binarized matrix.
    """

    in_tab = in_tab.iloc[:,0:2]
    in_tab.columns = ["Entity", "Label"]
    in_tab["val"] = 1
    in_tab.pivot(index="Entity", columns="Label").fillna(0)

    return in_tab


def read_input(
    input_martix: pd.DataFrame,
    format_spec: str = "pseudo_tab"
) -> pd.DataFrame:
    """
    A wrapper around Jaccard calculator functions helping to use the appropriate approach.
    ----------
    input_martix
        Pseudo-tabular, long or binarized matrix format.
    format_spec
        Specifies the format of input data. One of ["pseudo_tab", "long", "binary"]
    Returns
    -------
    The binarized matrix.
    """

    if format_spec == "binary":
        return input_martix
    
    else:
        if format_spec in ["pseudo_tab", "long"]:
            if format_spec == "pseudo_tab":
                bin_mat = binarize_tabular(input_martix)
            else:
                bin_mat = binarize_long(input_martix)
            return bin_mat
        else:
            return None


def main(
    input_path: str,
    output_path: str = "binarized_matrix.csv",
    format_spec: str = "pseudo_tab"
) -> None:
    """
    A high-level wrapper around input parsing functions.
    ----------
    input_path
        Path to input data in pseudo-tabular, long or binarized matrix format.
    output_path
        Path to save output to.
    format_spec
        Specifies the format of input data. One of ["pseudo_tab", "long", "binary"]
    Returns
    -------
    None
    """

    category_links = pd.read_csv(input_path)
    category_mat = read_input(category_links, format_spec=format_spec)
    category_mat.write_csv(output_path)
    return


if __name__ == '__main__':
    main()