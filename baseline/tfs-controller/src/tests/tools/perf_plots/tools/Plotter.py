# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Optional, Tuple
from .HistogramData import HistogramData

def plot_histogram(
    histograms : Dict[Tuple, HistogramData], filepath : str,
    title : Optional[str] = None, label_separator : str = ' ', dpi : int = 600,
    legend_loc : str = 'best', grid : bool = True
) -> None:

    # plot the cumulative histogram
    _, ax = plt.subplots(figsize=(8, 8))

    num_series = 0
    for histogram_keys, histogram_data in histograms.items():
        bins = sorted(histogram_data.bins)

        last_timestamp = max(histogram_data.timestamps)
        counts = histogram_data.data.get(last_timestamp)
        counts = [int(counts[bin_]) for bin_ in bins]
        if sum(counts) == 0: continue
        num_series += 1

        bins.insert(0, 0)
        bins = np.array(bins).astype(float)
        counts = np.array(counts).astype(float)

        assert len(bins) == len(counts) + 1
        centroids = (bins[1:] + bins[:-1]) / 2

        label = label_separator.join(histogram_keys)
        ax.hist(centroids, bins=bins, weights=counts, range=(min(bins), max(bins)), density=True,
                histtype='step', cumulative=True, label=label)

    if num_series == 0: return

    ax.grid(grid)
    ax.legend(loc=legend_loc)
    if title is not None: ax.set_title(title)
    ax.set_xlabel('seconds')
    ax.set_ylabel('Likelihood of occurrence')
    plt.xscale('log')
    plt.savefig(filepath, dpi=(dpi))
    plt.show()
