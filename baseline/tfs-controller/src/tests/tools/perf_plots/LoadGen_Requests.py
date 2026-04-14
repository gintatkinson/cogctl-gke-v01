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

import datetime, re
from datetime import datetime, timezone
from typing import Dict, List, Tuple
from .tools.FileSystem import create_folders
from .tools.HistogramData import HistogramData
from .tools.Plotter import plot_histogram
from .tools.Prometheus import get_prometheus_range, get_prometheus_series_names
from .tools.Histogram import results_to_histograms, save_histograms, unaccumulate_histograms

##### EXPERIMENT SETTINGS ##############################################################################################

EXPERIMENT_NAME = 'Scalability - Response Time'
EXPERIMENT_ID   = 'scenario_2/scalability/2023-05May-29/loadgen-reqs'

# (tenants,erlangs) => (time_start, time_end)
tz_utc=timezone.utc
EXPERIMENTS = {
    (  1,   5): (datetime(2023, 5, 29,  7, 59, 0, 0, tzinfo=tz_utc), datetime(2023, 5, 29,  8, 46, 0, 0, tzinfo=tz_utc)),
    (  5,  25): (datetime(2023, 5, 29,  8, 47, 0, 0, tzinfo=tz_utc), datetime(2023, 5, 29,  9,  4, 0, 0, tzinfo=tz_utc)),
    ( 10,  50): (datetime(2023, 5, 29,  9, 13, 0, 0, tzinfo=tz_utc), datetime(2023, 5, 29,  9, 30, 0, 0, tzinfo=tz_utc)),
    ( 20, 100): (datetime(2023, 5, 29,  9, 34, 0, 0, tzinfo=tz_utc), datetime(2023, 5, 29,  9, 52, 0, 0, tzinfo=tz_utc)),
    ( 40, 200): (datetime(2023, 5, 29, 10, 18, 0, 0, tzinfo=tz_utc), datetime(2023, 5, 29, 10, 34, 0, 0, tzinfo=tz_utc)),
    ( 60, 300): (datetime(2023, 5, 29, 10, 38, 0, 0, tzinfo=tz_utc), datetime(2023, 5, 29, 10, 54, 0, 0, tzinfo=tz_utc)),
    ( 80, 400): (datetime(2023, 5, 29, 11,  2, 0, 0, tzinfo=tz_utc), datetime(2023, 5, 29, 11, 19, 0, 0, tzinfo=tz_utc)),
    (100, 500): (datetime(2023, 5, 29, 11, 21, 0, 0, tzinfo=tz_utc), datetime(2023, 5, 29, 11, 37, 0, 0, tzinfo=tz_utc)),
    (120, 600): (datetime(2023, 5, 29, 11, 51, 0, 0, tzinfo=tz_utc), datetime(2023, 5, 29, 12,  8, 0, 0, tzinfo=tz_utc)),
}

TIME_STEP       = '1m'
LABEL_FILTERS   = {
    #'operation': 'setup', # 'setup' / 'teardown'
}

##### ENVIRONMENT SETTINGS #############################################################################################

try:
    from .AddressesCredentials import PROM_ADDRESS, PROM_PORT
except ImportError:
    PROM_ADDRESS = '127.0.0.1'
    PROM_PORT    = 9090
OUT_FOLDER   = 'data/perf/'

##### PLOT-SPECIFIC CUSTOMIZATIONS #####################################################################################

SERIES_MATCH   = 'tfs_loadgen_requests_.+_histogram_duration_bucket'
RE_SERIES_NAME = re.compile(r'^tfs_loadgen_requests_(.+)_histogram_duration_bucket$')
SERIES_LABELS  = ['request_type']

def update_keys(tenants : int, erlangs : int, request_type : str, operation : str) -> Tuple[Tuple, Tuple]:
    request_type = request_type.lower().replace('requesttype.', '').replace('_', ' ')
    collection_keys = (operation, request_type)
    histogram_keys = (str(tenants) + ' Tenants / ' + str(erlangs) + ' Erlangs',)
    return collection_keys, histogram_keys

def get_plot_specs(folders : Dict[str, str], operation : str, request_type : str) -> Tuple[str, str]:
    title = 'Load Generator - {:s} - {:s} {:s}'.format(EXPERIMENT_NAME, operation.title(), request_type.title())
    filepath = '{:s}/{:s}-{:s}.png'.format(folders['png'], operation, request_type.replace(' ', '-'))
    return title, filepath

##### AUTOMATED CODE ###################################################################################################

def get_series_names(folders : Dict[str, str], time_start : datetime, time_end : datetime) -> List[str]:
    series_names = get_prometheus_series_names(
        PROM_ADDRESS, PROM_PORT, SERIES_MATCH, time_start, time_end,
        raw_json_filepath='{:s}/_series.json'.format(folders['json'])
    )
    return series_names

def get_histogram_data(
    series_name : str, folders : Dict[str, str], time_start : datetime, time_end : datetime
) -> Dict[Tuple, HistogramData]:
    m = RE_SERIES_NAME.match(series_name)
    if m is None:
        # pylint: disable=broad-exception-raised
        raise Exception('Unparsable series name: {:s}'.format(str(series_name)))
    extra_labels = m.groups()
    results = get_prometheus_range(
        PROM_ADDRESS, PROM_PORT, series_name, LABEL_FILTERS, time_start, time_end, TIME_STEP,
        raw_json_filepath='{:s}/_raw_{:s}.json'.format(folders['json'], series_name)
    )
    histograms = results_to_histograms(results, SERIES_LABELS, extra_labels=extra_labels)
    unaccumulate_histograms(histograms, process_bins=True, process_timestamps=False)
    save_histograms(histograms, folders['csv'])
    return histograms

def main() -> None:
    histograms_collection : Dict[Tuple, Dict[Tuple, HistogramData]] = dict()

    series_names = set()
    folders = create_folders(OUT_FOLDER, EXPERIMENT_ID)
    for (time_start,time_end) in EXPERIMENTS.values():
        series_names.update(get_series_names(folders, time_start, time_end))

    for series_name in series_names:
        for (tenants,erlangs),(time_start,time_end) in EXPERIMENTS.items():
            histograms = get_histogram_data(series_name, folders, time_start, time_end)
            for histogram_keys, histogram_data in histograms.items():
                collection_keys,histogram_keys = update_keys(tenants, erlangs, *histogram_keys)
                histograms = histograms_collection.setdefault(collection_keys, dict())
                histograms[histogram_keys] = histogram_data

    for collection_keys,histograms in histograms_collection.items():
        title, filepath = get_plot_specs(folders, *collection_keys)
        plot_histogram(histograms, filepath, title=title, legend_loc='upper left')

if __name__ == '__main__':
    main()


