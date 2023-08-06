# PythonCache

Simple Library to do Python Caching

## Getting Started

To install, simply use:

```
pip install extensible-cache
```

(Planning to add the library to PyPi in the future).

The library is easy to use, just load a cache and provide it some data.

```python
import pandas as pd
from extensible_cache import PandasFileCache

cache = PandasFileCache("./cache_folder")
df = pd.read_csv("test.csv")

cache["my_cool_data"] = df

# ... somewhere later (even after restart) ...

df_new = cache["my_cool_data"]
```

This allows you to quickly buffer data to files and restore them later on.

## Notes

All contribtions are welcome!
