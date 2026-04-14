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

import re
from typing import Dict, List, Tuple
from .tools.FileSystem import create_folders
from .tools.HistogramData import HistogramData
from .tools.Plotter import plot_histogram
from .tools.Prometheus import get_prometheus_range, get_prometheus_series_names
from .tools.Histogram import results_to_histograms, save_histograms, unaccumulate_histograms

##### EXPERIMENT SETTINGS ##############################################################################################

from .experiments.Experiment import EXPERIMENT_NAME, EXPERIMENT_ID, TIME_START, TIME_END

TIME_STEP       = '1m'
LABEL_FILTERS   = {
    #'driver': 'emulated',
}

##### ENVIRONMENT SETTINGS #############################################################################################

try:
    from .AddressesCredentials import PROM_ADDRESS, PROM_PORT
except ImportError:
    PROM_ADDRESS = '127.0.0.1'
    PROM_PORT    = 9090
OUT_FOLDER   = 'data/perf/'

##### PLOT-SPECIFIC CUSTOMIZATIONS #####################################################################################

EXPERIMENT_ID  += '/dev-drv-methods'
SERIES_MATCH   = 'tfs_device_driver_.+_histogram_duration_bucket'
RE_SERIES_NAME = re.compile(r'^tfs_device_driver_(.+)_histogram_duration_bucket$')
SERIES_LABELS  = ['driver']

def update_keys(driver : str, method : str) -> Tuple[Tuple, Tuple]:
    collection_keys = (driver,)
    histogram_keys = (method,)
    return collection_keys, histogram_keys

def get_plot_specs(folders : Dict[str, str], driver : str) -> Tuple[str, str]:
    title = 'Device Driver - {:s} [{:s}]'.format(driver.title(), EXPERIMENT_NAME)
    filepath = '{:s}/{:s}.png'.format(folders['png'], driver)
    return title, filepath

##### AUTOMATED CODE ###################################################################################################

def get_series_names(folders : Dict[str, str]) -> List[str]:
    series_names = get_prometheus_series_names(
        PROM_ADDRESS, PROM_PORT, SERIES_MATCH, TIME_START, TIME_END,
        raw_json_filepath='{:s}/_series.json'.format(folders['json'])
    )
    return series_names

def get_histogram_data(series_name : str, folders : Dict[str, str]) -> Dict[Tuple, HistogramData]:
    m = RE_SERIES_NAME.match(series_name)
    if m is None:
        # pylint: disable=broad-exception-raised
        raise Exception('Unparsable series name: {:s}'.format(str(series_name)))
    extra_labels = m.groups()
    results = get_prometheus_range(
        PROM_ADDRESS, PROM_PORT, series_name, LABEL_FILTERS, TIME_START, TIME_END, TIME_STEP,
        raw_json_filepath='{:s}/_raw_{:s}.json'.format(folders['json'], series_name)
    )
    histograms = results_to_histograms(results, SERIES_LABELS, extra_labels=extra_labels)
    unaccumulate_histograms(histograms, process_bins=True, process_timestamps=False)
    save_histograms(histograms, folders['csv'])
    return histograms

def main() -> None:
    histograms_collection : Dict[Tuple, Dict[Tuple, HistogramData]] = dict()

    folders = create_folders(OUT_FOLDER, EXPERIMENT_ID)
    series_names = get_series_names(folders)

    for series_name in series_names:
        histograms = get_histogram_data(series_name, folders)
        for histogram_keys, histogram_data in histograms.items():
            collection_keys,histogram_keys = update_keys(*histogram_keys)
            histograms = histograms_collection.setdefault(collection_keys, dict())
            histograms[histogram_keys] = histogram_data

    for histogram_keys,histograms in histograms_collection.items():
        title, filepath = get_plot_specs(folders, *histogram_keys)
        plot_histogram(histograms, filepath, title=title)

if __name__ == '__main__':
    main()
