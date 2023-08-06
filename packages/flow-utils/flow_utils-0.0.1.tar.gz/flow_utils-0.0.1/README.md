# oneflow-utils
Deeplearning Utils base on OneFlow

## Pre-requisites
```bash
$ pip install oneflow-utils==0.0.1
```

## Contents
### 1. Cosine / Linear LR Schedule with Warmup
- Source Code: [Cosine LR](https://github.com/rentainhe/oneflow-utils/blob/main/schedulers/cosine_lr.py) / [Linear LR](https://github.com/rentainhe/oneflow-utils/blob/main/schedulers/linear_lr.py)

- Usage
```python
from oneflow-utils import WarmupLinearSchedule, WarmupCosineSchedule
```