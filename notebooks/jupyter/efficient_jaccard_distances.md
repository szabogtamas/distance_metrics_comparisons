---
jupyter:
  jupytext:
    formats: md,ipynb
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.4
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Generating Jacccard distance matrices efficiently

## Setup

```python
import sys, inspect

import scipy
import umap
import pandas as pd

from scipy.spatial import distance as scd
from sklearn import metrics as skm
from matplotlib import pyplot as plt
```

```python
sys.path.append("/usr/local/dev_scripts")

import similarity_utils as su
```

## Parse input

```python
import inspect
```

```python
lines = inspect.getsource(su.input_parser.read_input)
print(lines)
```

```python
main_df = su.input_parser.read_input("/home/rstudio/local_files/example_data/pseudo_tabular_format.csv")
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

```python
U = umap.UMAP(metric='precomputed')
umap_coords = U.fit_transform(scikit_distances)
```
