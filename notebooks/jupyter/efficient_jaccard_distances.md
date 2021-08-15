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
import umap
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
```

```python
sys.path.append("/usr/local/dev_scripts")

import similarity_utils as su
dist_to_sim = su.calculator.dist_to_sim 
```

```python
# Small helper to show source

def print_source(fun):
    lines = inspect.getsource(fun)
    print(lines)
    return
```

```python
main_input = "/home/rstudio/local_files/example_data/pseudo_tabular_format.csv"
```

## Parse input


The key step to making distance calculation more efficient is to convert data into a more machine-friendly format (a one-hot-encoded matrix). An example function that can achieve this looks like the one below:

```python
print_source(su.input_parser.binarize_tabular)
```

```python
main_df = su.input_parser.read_input(main_input)
main_df.head()
```

For the sake of demonstration, limit size of input data to first ten entities.

```python
top_ent = main_df["Entity"].unique().tolist()[:10]
limited_df = main_df.loc[main_df["Entity"].isin(top_ent)]
limited_df.shape
```

## Calculate distances

```python
%%time
loop_distances = su.calculator.calculate_jaccard(limited_df, "loop")
dist_to_sim(loop_distances).head()
```

```python
print_source(su.calculator.jaccard_loop)
```

```python
%%time
pandas_distances = su.calculator.calculate_jaccard(limited_df, "pandas")
dist_to_sim(pandas_distances).head()
```

```python
print_source(su.calculator.jaccard_pandas)
```

```python
%%time
scikit_distances = su.calculator.calculate_jaccard(limited_df)
dist_to_sim(scikit_distances).head()
```

```python
print_source(su.calculator.jaccard_scikit)
```

## Visualize results

```python
U = umap.UMAP(metric="precomputed")
umap_coords = U.fit_transform(scikit_distances)
```

```python
X_embedded = TSNE(n_components=2, metric="precomputed").fit_transform(scikit_distances)
```

```python

```
