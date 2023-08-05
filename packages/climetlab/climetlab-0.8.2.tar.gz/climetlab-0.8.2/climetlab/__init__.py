# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

from .core.caching import CACHE as cache
from .core.metadata import init_metadata
from .core.settings import SETTINGS as settings
from .datasets import Dataset, dataset, load_dataset, register_dataset
from .normalize import ALL
from .plotting import interactive_map, new_plot
from .plotting import options as plotting_options
from .plotting import plot_map
from .readers import Reader
from .sources import Source, load_source, register_source, source
from .wrappers import Wrapper

__version__ = "0.8.2"


__all__ = [
    "ALL",
    "cache",
    "dataset",
    "Dataset",
    "Wrapper",
    "interactive_map",
    "load_dataset",
    "load_source",
    "new_plot",
    "plot_map",
    "plotting_options",
    "Reader",
    "settings",
    "source",
    "Source",
    "register_dataset",
    "register_source",
]

init_metadata()
