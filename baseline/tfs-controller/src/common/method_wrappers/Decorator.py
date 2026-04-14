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

import grpc, json, logging, threading
from enum import Enum
from prettytable import PrettyTable
from typing import Any, Dict, List, Optional, Set, Tuple
from prometheus_client import Counter, Histogram
from prometheus_client.metrics import MetricWrapperBase, INF
from common.tools.grpc.Tools import grpc_message_to_json_string
from .ServiceExceptions import ServiceException

class MetricTypeEnum(Enum):
    COUNTER_STARTED    = 'tfs_{component:s}_{sub_module:s}_{method:s}_counter_requests_started'
    COUNTER_COMPLETED  = 'tfs_{component:s}_{sub_module:s}_{method:s}_counter_requests_completed'
    COUNTER_FAILED     = 'tfs_{component:s}_{sub_module:s}_{method:s}_counter_requests_failed'
    COUNTER_BLOCKED    = 'tfs_{component:s}_{sub_module:s}_{method:s}_counter_requests_blocked'
    HISTOGRAM_DURATION = 'tfs_{component:s}_{sub_module:s}_{method:s}_histogram_duration'

METRIC_TO_CLASS_PARAMS = {
    MetricTypeEnum.COUNTER_STARTED   : (Counter,   {}),
    MetricTypeEnum.COUNTER_COMPLETED : (Counter,   {}),
    MetricTypeEnum.COUNTER_FAILED    : (Counter,   {}),
    MetricTypeEnum.COUNTER_BLOCKED   : (Counter,   {}),
    MetricTypeEnum.HISTOGRAM_DURATION: (Histogram, {
        'buckets': (
            # .005, .01, .025, .05, .075, .1, .25, .5, .75, 1.0, INF
            #0.0010, 0.0025, 0.0050, 0.0075,
            #0.0100, 0.0250, 0.0500, 0.0750,
            #0.1000, 0.2500, 0.5000, 0.7500,
            #1.0000, 2.5000, 5.0000, 7.5000,
            0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009,  # 1~9 ms
            0.010, 0.020, 0.030, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090,  # 10~90 ms
            0.100, 0.200, 0.300, 0.400, 0.500, 0.600, 0.700, 0.800, 0.900,  # 100~900 ms
            1.000, 2.000, 3.000, 4.000, 5.000, 6.000, 7.000, 8.000, 9.000,  # 1~9 sec
            10.00, 20.00, 30.00, 40.00, 50.00, 60.00, 70.00, 80.00, 90.00,  # 10~90 sec
            100.0, 110.0, 120.0, INF                                        # 100sec~2min & Infinity
        )
    })
}

class MetricsPool:
    lock = threading.Lock()
    metrics : Dict[str, MetricWrapperBase] = dict()

    def __init__(
        self, component : str, sub_module : str, labels : Dict[str, str] = {},
        default_metric_params : Dict[MetricTypeEnum, Dict] = dict()
    ) -> None:
        self._component = component
        self._sub_module = sub_module
        self._labels = labels
        self._default_metric_params = default_metric_params

    def get_or_create(self, method : str, metric_type : MetricTypeEnum, **metric_params) -> MetricWrapperBase:
        metric_name = str(metric_type.value).format(
            component=self._component, sub_module=self._sub_module, method=method).upper()
        with MetricsPool.lock:
            if metric_name not in MetricsPool.metrics:
                metric_tuple : Tuple[MetricWrapperBase, Dict] = METRIC_TO_CLASS_PARAMS.get(metric_type)
                metric_class, default_metric_params = metric_tuple
                if len(metric_params) == 0: metric_params = self._default_metric_params.get(metric_type, {})
                if len(metric_params) == 0: metric_params = default_metric_params
                labels = sorted(self._labels.keys())
                MetricsPool.metrics[metric_name] = metric_class(metric_name.lower(), '', labels, **metric_params)
            return MetricsPool.metrics[metric_name]

    def get_metrics(
        self, method : str, labels : Optional[Dict[str, str]] = None
    ) -> Tuple[Histogram, Counter, Counter, Counter]:
        histogram_duration : Histogram = self.get_or_create(method, MetricTypeEnum.HISTOGRAM_DURATION)
        counter_started    : Counter   = self.get_or_create(method, MetricTypeEnum.COUNTER_STARTED)
        counter_completed  : Counter   = self.get_or_create(method, MetricTypeEnum.COUNTER_COMPLETED)
        counter_failed     : Counter   = self.get_or_create(method, MetricTypeEnum.COUNTER_FAILED)

        if labels is None and len(self._labels) > 0:
            labels = self._labels

        if labels is not None and len(labels) > 0:
            histogram_duration = histogram_duration.labels(**labels)
            counter_started    = counter_started.labels(**labels)
            counter_completed  = counter_completed.labels(**labels)
            counter_failed     = counter_failed.labels(**labels)

        return histogram_duration, counter_started, counter_completed, counter_failed

    def get_metrics_loadgen(
        self, method : str, labels : Optional[Dict[str, str]] = None
    ) -> Tuple[Histogram, Counter, Counter, Counter, Counter]:
        histogram_duration : Histogram = self.get_or_create(method, MetricTypeEnum.HISTOGRAM_DURATION)
        counter_started    : Counter   = self.get_or_create(method, MetricTypeEnum.COUNTER_STARTED)
        counter_completed  : Counter   = self.get_or_create(method, MetricTypeEnum.COUNTER_COMPLETED)
        counter_failed     : Counter   = self.get_or_create(method, MetricTypeEnum.COUNTER_FAILED)
        counter_blocked    : Counter   = self.get_or_create(method, MetricTypeEnum.COUNTER_BLOCKED)

        if labels is None and len(self._labels) > 0:
            labels = self._labels

        if labels is not None and len(labels) > 0:
            histogram_duration = histogram_duration.labels(**labels)
            counter_started    = counter_started.labels(**labels)
            counter_completed  = counter_completed.labels(**labels)
            counter_failed     = counter_failed.labels(**labels)
            counter_blocked    = counter_blocked.labels(**labels)

        return histogram_duration, counter_started, counter_completed, counter_failed, counter_blocked

    def get_pretty_table(self, remove_empty_buckets : bool = True) -> PrettyTable:
        with MetricsPool.lock:
            method_to_metric_fields : Dict[str, Dict[str, Dict[str, Any]]] = dict()
            bucket_bounds : Set[str] = set()
            for raw_metric_name,raw_metric_data in MetricsPool.metrics.items():
                if '_COUNTER_' in raw_metric_name:
                    method_name,metric_name = raw_metric_name.split('_COUNTER_')
                elif '_HISTOGRAM_' in raw_metric_name:
                    method_name,metric_name = raw_metric_name.split('_HISTOGRAM_')
                else:
                    raise Exception('Unsupported metric: {:s}'.format(raw_metric_name)) # pragma: no cover
                metric_data = method_to_metric_fields.setdefault(method_name, dict()).setdefault(metric_name, dict())
                for values in raw_metric_data._child_samples():
                    field_name = values[0]
                    labels = values[1]
                    value = values[2]
                    if field_name == '_bucket': bucket_bounds.add(labels['le'])
                    if len(labels) > 0: field_name = '{:s}:{:s}'.format(field_name, json.dumps(labels, sort_keys=True))
                    metric_data[field_name] = value
            #print('method_to_metric_fields', method_to_metric_fields)

            def sort_stats_key(item : List) -> float:
                str_duration = str(item[0])
                if str_duration == '---': return 0.0
                return float(str_duration.replace(' ms', ''))

            field_names = ['Method', 'TOT', 'OK', 'ERR', 'avg(Dur)']
            bucket_bounds = sorted(bucket_bounds, key=float) # convert buckets to float to get the key
            bucket_column_names = ['<={:s}'.format(bucket_bound) for bucket_bound in bucket_bounds]
            field_names.extend(bucket_column_names)

            pt_stats = PrettyTable(
                field_names=field_names, sortby='avg(Dur)', sort_key=sort_stats_key, reversesort=True)
            for f in field_names: pt_stats.align[f] = 'r'
            for f in ['Method']: pt_stats.align[f] = 'l'

            for method_name,metrics in method_to_metric_fields.items():
                counter_started_value = int(metrics['REQUESTS_STARTED']['_total'])
                if counter_started_value == 0:
                    #pt_stats.add_row([method_name, '---', '---', '---', '---'])
                    continue
                counter_completed_value = int(metrics['REQUESTS_COMPLETED']['_total'])
                counter_failed_value = int(metrics['REQUESTS_FAILED']['_total'])
                duration_count_value = float(metrics['DURATION']['_count'])
                duration_sum_value = float(metrics['DURATION']['_sum'])
                duration_avg_value = duration_sum_value/duration_count_value

                row = [
                    method_name, str(counter_started_value), str(counter_completed_value), str(counter_failed_value),
                    '{:.3f} ms'.format(1000.0 * duration_avg_value),
                ]

                total_count = 0
                for bucket_bound in bucket_bounds:
                    labels = json.dumps({"le": bucket_bound}, sort_keys=True)
                    bucket_name = '_bucket:{:s}'.format(labels)
                    accumulated_count = int(metrics['DURATION'][bucket_name])
                    bucket_count = accumulated_count - total_count
                    row.append(str(bucket_count) if bucket_count > 0 else '')
                    total_count = accumulated_count

                pt_stats.add_row(row)
            
            if remove_empty_buckets:
                for bucket_column_name in bucket_column_names:
                    col_index = pt_stats._field_names.index(bucket_column_name)
                    num_non_empties = sum([1 for row in pt_stats._rows if len(row[col_index]) > 0])
                    if num_non_empties > 0: continue
                    pt_stats.del_column(bucket_column_name)
            
            return pt_stats

def metered_subclass_method(metrics_pool : MetricsPool):
    def outer_wrapper(func):
        metrics = metrics_pool.get_metrics(func.__name__)
        histogram_duration, counter_started, counter_completed, counter_failed = metrics

        @histogram_duration.time()
        def inner_wrapper(self, *args, **kwargs):
            counter_started.inc()
            try:
                reply = func(self, *args, **kwargs)
                counter_completed.inc()
                return reply
            except KeyboardInterrupt:   # pylint: disable=try-except-raise
                raise
            except Exception:           # pylint: disable=broad-except
                counter_failed.inc()
                raise

        return inner_wrapper
    return outer_wrapper

def safe_and_metered_rpc_method(metrics_pool : MetricsPool, logger : logging.Logger):
    def outer_wrapper(func):
        method_name = func.__name__
        metrics = metrics_pool.get_metrics(method_name)
        histogram_duration, counter_started, counter_completed, counter_failed = metrics

        @histogram_duration.time()
        def inner_wrapper(self, request, grpc_context : grpc.ServicerContext):
            counter_started.inc()
            try:
                logger.debug('{:s} request: {:s}'.format(method_name, grpc_message_to_json_string(request)))
                reply = func(self, request, grpc_context)
                logger.debug('{:s} reply: {:s}'.format(method_name, grpc_message_to_json_string(reply)))
                counter_completed.inc()
                return reply
            except ServiceException as e:   # pragma: no cover (ServiceException not thrown)
                if e.code not in [grpc.StatusCode.NOT_FOUND, grpc.StatusCode.ALREADY_EXISTS]:
                    # Assume not found or already exists is just a condition, not an error
                    logger.exception('{:s} exception'.format(method_name))
                    counter_failed.inc()
                else:
                    counter_completed.inc()
                grpc_context.abort(e.code, e.details)
            except Exception as e:          # pragma: no cover, pylint: disable=broad-except
                logger.exception('{:s} exception'.format(method_name))
                counter_failed.inc()
                grpc_context.abort(grpc.StatusCode.INTERNAL, str(e))
        return inner_wrapper
    return outer_wrapper

def safe_and_metered_rpc_method_async(metrics_pool: MetricsPool, logger: logging.Logger):
    def outer_wrapper(func):
        method_name = func.__name__
        metrics = metrics_pool.get_metrics(method_name)
        histogram_duration, counter_started, counter_completed, counter_failed = metrics

        async def inner_wrapper(self, request, grpc_context: grpc.aio.ServicerContext):
            counter_started.inc()
            try:
                logger.debug('{:s} request: {:s}'.format(method_name, grpc_message_to_json_string(request)))
                reply = await func(self, request, grpc_context)
                logger.debug('{:s} reply: {:s}'.format(method_name, grpc_message_to_json_string(reply)))
                counter_completed.inc()
                return reply
            except ServiceException as e:  # pragma: no cover (ServiceException not thrown)
                if e.code not in [grpc.StatusCode.NOT_FOUND, grpc.StatusCode.ALREADY_EXISTS]:
                    # Assume not found or already exists is just a condition, not an error
                    logger.exception('{:s} exception'.format(method_name))
                    counter_failed.inc()
                else:
                    counter_completed.inc()
                await grpc_context.abort(e.code, e.details)
            except Exception as e:  # pragma: no cover, pylint: disable=broad-except
                logger.exception('{:s} exception'.format(method_name))
                counter_failed.inc()
                await grpc_context.abort(grpc.StatusCode.INTERNAL, str(e))

        return inner_wrapper

    return outer_wrapper

