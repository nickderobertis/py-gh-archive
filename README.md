
[![](https://codecov.io/gh/nickderobertis/py-gh-archive/branch/master/graph/badge.svg)](https://codecov.io/gh/nickderobertis/py-gh-archive)

# py-gh-archive

## Overview

Python SDK to access Github Archive

## Getting Started

Install `gharchive`:

```
pip install gharchive
```

Or, for multi-processing in extracting archives:

```
pip install gharchive[mgzip]
```

A simple example:

```python
from gharchive import GHArchive
gh = GHArchive()

data = gh.get('6/8/2020', '6/10/2020', filters=[
    ('repo.name', 'bitcoin/bitcoin'),
    ('type', 'WatchEvent')
])


```

## Links

See the
[documentation here.](
https://nickderobertis.github.io/py-gh-archive/
)

## Author

Created by Nick DeRobertis. MIT License.