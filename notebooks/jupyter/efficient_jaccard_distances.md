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

from sklearn import metrics as skm
import sklearn as sk
```

```python
#sys.path.append("/usr/local/dev_scripts")

#import parallel_jaccard
```

```python
from scipy.spatial import distance as scd
```