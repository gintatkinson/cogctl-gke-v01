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

import csv
from typing import Dict, List, Tuple
from .HistogramData import HistogramData

def results_to_histograms(
    results : List[Dict], key_labels : List[str], extra_labels : List[str] = []
) -> Dict[Tuple, HistogramData]:
    histograms : Dict[Tuple, HistogramData] = dict()
    for result in results:
        metric : Dict = result['metric']
        labels = [metric[l] for l in key_labels]
        if len(extra_labels) > 0: labels.extend(extra_labels)
        histogram_key = tuple(labels)
        histogram = histograms.get(histogram_key)
        if histogram is None:
            histogram = histograms.setdefault(
                histogram_key, HistogramData(timestamps=set(), bins=set(), data=dict()))
        bin_ = float(metric['le'])
        histogram.bins.add(bin_)
    
        values : List[Tuple[int, str]] = result['values']
        for timestamp,count in values:
            histogram.timestamps.add(timestamp)
            histogram.data.setdefault(timestamp, dict())[bin_] = int(count)
    return histograms

def unaccumulate_histogram(
    histogram : HistogramData, process_bins : bool = True, process_timestamps : bool = True
) -> None:
    timestamps = sorted(histogram.timestamps)
    bins = sorted(histogram.bins)
    accumulated_over_time = {b:0 for b in bins}
    for timestamp in timestamps:
        bin_to_count = histogram.data.get(timestamp)
        if bin_to_count is None: continue

        accumulated_over_bins = 0
        for bin_ in bins:
            count = bin_to_count[bin_]

            if process_bins:
                count -= accumulated_over_bins
                accumulated_over_bins += count

            if process_timestamps:
                count -= accumulated_over_time[bin_]
                accumulated_over_time[bin_] += count

            bin_to_count[bin_] = count

def unaccumulate_histograms(
    histograms : Dict[Tuple, HistogramData], process_bins : bool = True, process_timestamps : bool = True
) -> None:
    for histogram in histograms.values():
        unaccumulate_histogram(histogram, process_bins=process_bins, process_timestamps=process_timestamps)

def save_histogram(filepath : str, histogram : HistogramData) -> None:
    timestamps = sorted(histogram.timestamps)
    bins = sorted(histogram.bins)
    header = [''] + [str(b) for b in bins]
    with open(filepath, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for timestamp in timestamps:
            bin_to_count = histogram.data.get(timestamp, {})
            writer.writerow([timestamp] + [
                str(bin_to_count.get(bin_, 0))
                for bin_ in bins
            ])

def save_histograms(histograms : Dict[Tuple, HistogramData], data_folder : str) -> None:
    for histogram_keys, histogram_data in histograms.items():
        filepath = '{:s}/{:s}.csv'.format(data_folder, '__'.join(histogram_keys))
        save_histogram(filepath, histogram_data)
