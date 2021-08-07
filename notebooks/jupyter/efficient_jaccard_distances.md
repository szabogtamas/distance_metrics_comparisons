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
main_df = pd.read_csv("/home/rstudio/local_files/example_data/pseudo_tabular_format.csv")
main_df.head()
```

Create an intermedier data representation corresponding to a dictionary

```python
d = main_df.to_dict(orient="series")
d = {k: v.dropna().apply(lambda x: "HP:" + str(x).split(".")[0]).tolist() for k, v in d.items()}
```

Convert the data into a binarized (one-hot-encoded) format

```python
binarized_data = dict()
for k, v in d.items():
    binarized_data[k] = [1 if e in v else 0 for e in all_items]
binarized_df = pd.DataFrame(binarized_data)
binarized_df.head()
```

## Calculate distances

```python
distances = list()
instances = list(binarized_df.columns)

for n1 in instances:
    for n2 in instances:
        ds = skm.pairwise.distance.jaccard(binarized_df[n1], binarized_df[n2])
        distances.append((n1, n2, ds))

distances = pd.DataFrame(distances)
distances.head()
```

## Visualize results