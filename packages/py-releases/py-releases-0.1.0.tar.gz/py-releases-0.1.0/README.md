# *py-releases*

This package shows available python versions and your download links.

## Installation

Use the [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install py-releases
```

## Usage

```python
from python_releases import Releases

releases = Releases()
# most recent stable version
stable = releases.last_stable

# version under development
dev = releases.dev

# a dict with all python versions
all_versions = releases.all

# Returns the download link to a specified version
releases.search("3.9.6")
```

## License
[GPL-2.0](https://github.com/kuticoski/python-releases/blob/main/LICENSE)

