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

import csv, prettytable
from typing import Dict, List, Tuple
from .Enums import ActionEnum, RecordTypeEnum
from .PerfPoint import PerfPoint

class PerfData:
    def __init__(self) -> None:
        self._total_count : int = 0
        self._operation_counters : Dict[Tuple[ActionEnum, RecordTypeEnum], int] = dict()
        self._points : Dict[Tuple[ActionEnum, RecordTypeEnum, str], Tuple[List[PerfPoint], List[float]]] = dict()
        self.clear_operation_counters()

    @property
    def operation_counters(self): return self._operation_counters

    def clear_operation_counters(self) -> None:
        self._points.clear()
        self._total_count = 0
        for action in ActionEnum.__members__.values():
            for record_type in RecordTypeEnum.__members__.values():
                type_key = (action, record_type)
                self._operation_counters[type_key] = 0

    def add_point(self, action : ActionEnum, record_type : RecordTypeEnum, record_uuid : str) -> PerfPoint:
        point = PerfPoint(action, record_type, record_uuid)

        point_key = (action, record_type, record_uuid)
        self._points.setdefault(point_key, (list(), list()))[0].append(point)

        type_key = (action, record_type)
        self._operation_counters[type_key] = self._operation_counters.get(type_key, 0) + 1
        self._total_count += 1
        return point

    def add_notif_time(
        self, action : ActionEnum, record_type : RecordTypeEnum, record_uuid : str, notif_time : float
    ) -> None:
        point_key = (action, record_type, record_uuid)
        self._points.setdefault(point_key, (list(), list()))[1].append(notif_time)

    def to_csv(self, filepath : str) -> None:
        points = []
        for points_key,(perf_points,notif_times) in self._points.items():
            if points_key[0] == ActionEnum.GET:
                points.extend([pp.to_dict() for pp in perf_points])
            elif len(perf_points) != len(notif_times):
                points.extend([pp.to_dict() for pp in perf_points])
            else:
                for pp,nt in zip(perf_points,notif_times):
                    pp.set_time_notified(nt)
                    points.append(pp.to_dict())

        keys = points[0].keys()
        with open(filepath, 'w', newline='', encoding='UTF-8') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(points)

    def stats_to_str(self) -> str:
        field_names = ['action', 'record_type', 'count']
        pt_stats = prettytable.PrettyTable(field_names=field_names, sortby='count', reversesort=True)
        for f in field_names[0:2]: pt_stats.align[f] = 'l'
        for f in field_names[2:3]: pt_stats.align[f] = 'r'
        for (action,record_type),count in self._operation_counters.items():
            pt_stats.add_row([action.value, record_type.value, count])
        pt_stats.add_row(['*', '*', self._total_count])
        return pt_stats.get_string()
