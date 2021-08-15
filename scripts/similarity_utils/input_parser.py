#!/usr/bin/env/python3

import argparse, sys
import pandas as pd

pd.options.mode.chained_assignment = None


parser = argparse.ArgumentParser(
    description = "Parse and preprocess input data for Jaccard calculation."
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
    "--output_path",
    default = sys.stdout,
    type = argparse.FileType('w'),
    help = "Path to output file"
)


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
    binarized_data["Categories"] = all_items
    binarized_data = binarized_data.set_index("Categories").T

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

    tmp_df = in_tab.iloc[:,0:2]
    tmp_df.columns = ["Entity", "Label"]
    tmp_df["val"] = 1
    tmp_df = tmp_df.pivot(index="Entity", columns="Label").fillna(0)

    return tmp_df


def read_input(
    input_path: str,
    format_spec: str = "pseudo_tab"
) -> pd.DataFrame:
    """
    A wrapper around Jaccard calculator functions helping to use the appropriate approach.
    ----------
    input_path
        Pseudo-tabular, long or binarized matrix format input data.
    format_spec
        Specifies the format of input data. One of ["pseudo_tab", "long", "binary"]
    Returns
    -------
    The binarized matrix.
    """
    
    input_martix = pd.read_csv(input_path)

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
    
    category_mat = read_input(input_path, format_spec=format_spec)
    category_mat.to_csv(output_path, index=False)
    return


if __name__ == '__main__':
    args = parser.parse_args()
    main(**args.__dict__)
else:
    del parser
    del argparse