---
jupyter:
  jupytext:
    formats: md,ipynb
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Generating Jacccard distance matrices efficiently

## Setup

```python
from matplotlib import pyplot as plt
import pandas as pd
import scipy
from scipy.spatial import distance as scd

from sklearn import metrics as skm
import sklearn as sk
```

```python
sys.path.append("/usr/local/dev_scripts")

import similarity_utils as su
```

## Parse input

```python
main_df = suinput_parser.read_input("/home/rstudio/local_files/example_data/pseudo_tabular_format.csv")
main_df.head()
```

## Calculate distances

```python
%time loop_distances = calculate_jaccard(main_df, "loop")
loop_distances.head()
```

```python
%time pandas_distances = calculate_jaccard(main_df, "pandas")
pandas_distances.head()
```

```python
%time scikit_distances = calculate_jaccard(main_df)
scikit_distances.head()
```

## Visualize results