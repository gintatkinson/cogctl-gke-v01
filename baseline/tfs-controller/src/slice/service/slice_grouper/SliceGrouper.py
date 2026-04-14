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

import logging, pandas, threading
from typing import Dict, Optional, Tuple
from sklearn.cluster import KMeans
from common.proto.context_pb2 import Slice
from common.tools.grpc.Tools import grpc_message_to_json_string
from .Constants import SLICE_GROUPS
from .MetricsExporter import MetricsExporter
from .Tools import (
    add_slice_to_group, create_slice_groups, get_slice_grouping_parameters, is_slice_grouping_enabled,
    remove_slice_from_group)

LOGGER = logging.getLogger(__name__)

class SliceGrouper:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._is_enabled = is_slice_grouping_enabled()
        LOGGER.info('Slice Grouping: {:s}'.format('ENABLED' if self._is_enabled else 'DISABLED'))
        if not self._is_enabled: return

        metrics_exporter = MetricsExporter()
        metrics_exporter.create_table()

        self._slice_groups = create_slice_groups(SLICE_GROUPS)

        # Initialize and fit K-Means with the pre-defined clusters we want, i.e., one per slice group
        df_groups = pandas.DataFrame(SLICE_GROUPS, columns=['name', 'availability', 'capacity_gbps'])
        k_means = KMeans(n_clusters=df_groups.shape[0])
        k_means.fit(df_groups[['availability', 'capacity_gbps']])
        df_groups['label'] = k_means.predict(df_groups[['availability', 'capacity_gbps']])
        self._k_means = k_means
        self._df_groups = df_groups

        self._group_mapping : Dict[str, Dict] = {
            group['name']:{k:v for k,v in group.items() if k != 'name'}
            for group in list(df_groups.to_dict('records'))
        }

        label_to_group = {}
        for group_name,group_attrs in self._group_mapping.items():
            label = group_attrs['label']
            availability = group_attrs['availability']
            capacity_gbps = group_attrs['capacity_gbps']
            metrics_exporter.export_point(
                group_name, group_name, availability, capacity_gbps, is_center=True)
            label_to_group[label] = group_name
        self._label_to_group = label_to_group

    def _select_group(self, slice_obj : Slice) -> Optional[Tuple[str, float, float]]:
        with self._lock:
            grouping_parameters = get_slice_grouping_parameters(slice_obj)
            LOGGER.debug('[_select_group] grouping_parameters={:s}'.format(str(grouping_parameters)))
            if grouping_parameters is None: return None

            sample = pandas.DataFrame([grouping_parameters], columns=['availability', 'capacity_gbps'])
            sample['label'] = self._k_means.predict(sample)
            sample = sample.to_dict('records')[0]   # pylint: disable=unsubscriptable-object
            LOGGER.debug('[_select_group] sample={:s}'.format(str(sample)))
            label = sample['label']
            availability = sample['availability']
            capacity_gbps = sample['capacity_gbps']
            group_name = self._label_to_group[label]
            LOGGER.debug('[_select_group] group_name={:s}'.format(str(group_name)))
            return group_name, availability, capacity_gbps

    @property
    def is_enabled(self): return self._is_enabled

    def group(self, slice_obj : Slice) -> bool:
        LOGGER.debug('[group] slice_obj={:s}'.format(grpc_message_to_json_string(slice_obj)))
        selected_group = self._select_group(slice_obj)
        LOGGER.debug('[group] selected_group={:s}'.format(str(selected_group)))
        if selected_group is None: return False
        return add_slice_to_group(slice_obj, selected_group)

    def ungroup(self, slice_obj : Slice) -> bool:
        LOGGER.debug('[ungroup] slice_obj={:s}'.format(grpc_message_to_json_string(slice_obj)))
        selected_group = self._select_group(slice_obj)
        LOGGER.debug('[ungroup] selected_group={:s}'.format(str(selected_group)))
        if selected_group is None: return False
        return remove_slice_from_group(slice_obj, selected_group)
