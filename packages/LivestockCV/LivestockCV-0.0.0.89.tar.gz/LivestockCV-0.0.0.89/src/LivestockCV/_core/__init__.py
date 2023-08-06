# Versioning
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions



import os
import matplotlib
from LivestockCV._core.show_ import show_
from LivestockCV._core.dimensions_ import dimensions_
from LivestockCV._core.read_ import read_

