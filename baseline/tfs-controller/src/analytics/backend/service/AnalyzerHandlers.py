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

import logging
from enum import Enum
import pandas as pd
from collections import defaultdict

logger = logging.getLogger(__name__)


class Handlers(Enum):
    AGGREGATION_HANDLER = "AggregationHandler"
    AGGREGATION_HANDLER_THREE_TO_ONE = "AggregationHandlerThreeToOne"
    UNSUPPORTED_HANDLER = "UnsupportedHandler"

    @classmethod
    def is_valid_handler(cls, handler_name):
        return handler_name in cls._value2member_map_

def select_handler(handler_name):
    if handler_name == "AggregationHandler":
        return aggregation_handler
    elif handler_name == "AggregationHandlerThreeToOne":
        return aggregation_handler_three_to_one
    else:
        return "UnsupportedHandler"

# This method is top-level and should not be part of the class due to serialization issues.
def threshold_handler(key, aggregated_df, thresholds):
    """
    Apply thresholds (TH-Fall and TH-Raise) based on the thresholds dictionary
    on the aggregated DataFrame.

    Args:
        key (str): Key for the aggregated DataFrame.
        aggregated_df (pd.DataFrame): DataFrame with aggregated metrics.
        thresholds (dict): Thresholds dictionary with keys in the format '<metricName>' and values as (fail_th, raise_th).

    Returns:
        pd.DataFrame: DataFrame with additional threshold columns.
    """
    for metric_name, threshold_values in thresholds.items():
        # Ensure the metric column exists in the DataFrame
        if metric_name not in aggregated_df.columns:
            logger.warning(f"Metric '{metric_name}' does not exist in the DataFrame for key: {key}. Skipping threshold application.")
            continue
        
        # Ensure the threshold values are valid (check for tuple specifically)
        if isinstance(threshold_values, list) and len(threshold_values) == 2:
            fail_th, raise_th = threshold_values
            
            # Add threshold columns with updated naming
            aggregated_df[f"{metric_name}_TH_RAISE"] = aggregated_df[metric_name] > raise_th
            aggregated_df[f"{metric_name}_TH_FALL"]  = aggregated_df[metric_name] < fail_th
        else:
            logger.warning(f"Threshold values for '{metric_name}' ({threshold_values}) are not a list of length 2. Skipping threshold application.")
    return aggregated_df

def aggregation_handler(
        batch_type_name, key, batch, input_kpi_list, output_kpi_list, thresholds
    ):
    """
      Process a batch of data and calculate aggregated values for each input KPI
      and maps them to the output KPIs. """

    logger.info(f"({batch_type_name}) Processing batch for key: {key}")
    if not batch:
        logger.info("Empty batch received. Skipping processing.")
        return []
    else:
        logger.info(f" >>>>> Processing {len(batch)} records for key: {key}")
        
        # Convert data into a DataFrame
        df = pd.DataFrame(batch)

        # Filter the DataFrame to retain rows where kpi_id is in the input list (subscribed endpoints only)
        df = df[df['kpi_id'].isin(input_kpi_list)].copy()

        if df.empty:
            logger.warning(f"No data available for KPIs: {input_kpi_list}. Skipping processing.")
            return []

        # Define all possible aggregation methods
        aggregation_methods = {
            "min"     : ('kpi_value', 'min'),
            "max"     : ('kpi_value', 'max'),
            "avg"     : ('kpi_value', 'mean'),
            "first"   : ('kpi_value', lambda x: x.iloc[0]),
            "last"    : ('kpi_value', lambda x: x.iloc[-1]),
            "variance": ('kpi_value', 'var'),
            "count"   : ('kpi_value', 'count'),
            "range"   : ('kpi_value', lambda x: x.max() - x.min()),
            "sum"     : ('kpi_value', 'sum'),
        }

        results = []
        
        # Process each KPI-specific task parameter
        for kpi_index, kpi_id in enumerate(input_kpi_list):

            # logger.info(f"1.Processing KPI: {kpi_id}")
            kpi_task_parameters = thresholds["task_parameter"][kpi_index]
            
            # Get valid task parameters for this KPI
            valid_task_parameters = [
                method for method in kpi_task_parameters.keys() 
                if method in aggregation_methods
            ]

            # Select the aggregation methods based on valid task parameters
            selected_methods = {method: aggregation_methods[method] for method in valid_task_parameters}

            # logger.info(f"2. Processing KPI: {kpi_id} with task parameters: {kpi_task_parameters}")
            kpi_df = df[df['kpi_id'] == kpi_id]

            # Check if kpi_df is not empty before applying the aggregation methods
            if not kpi_df.empty:
                agg_df = kpi_df.groupby('kpi_id').agg(**selected_methods).reset_index()

                # logger.info(f"3. Aggregated DataFrame for KPI: {kpi_id}: {agg_df}")

                agg_df['kpi_id'] = output_kpi_list[kpi_index]

                # logger.info(f"4. Applying thresholds for df: {agg_df['kpi_id']}")
                record = threshold_handler(key, agg_df, kpi_task_parameters)

                results.extend(record.to_dict(orient='records'))
            else:
                logger.warning(f"No data available for KPIs: {kpi_id}. Skipping aggregation.")
                continue
        if results:
            return results
        else:
            return []

def find(data , type , value):
    return next((item for item in data if item[type] == value), None)


def aggregation_handler_three_to_one(
        batch_type_name, key, batch, input_kpi_list, output_kpi_list, thresholds
):

    # Group and sum
    # Track sum and count
    sum_dict = defaultdict(int)
    count_dict = defaultdict(int)

    for item in batch:
        kpi_id = item["kpi_id"]
        if kpi_id in input_kpi_list:
            sum_dict[kpi_id] += item["kpi_value"]
            count_dict[kpi_id] += 1

    # Compute average
    avg_dict = {kpi_id: sum_dict[kpi_id] / count_dict[kpi_id] for kpi_id in sum_dict}

    total_kpi_metric = 0
    for kpi_id, total_value in avg_dict.items():
        total_kpi_metric += total_value

    result = {
        "kpi_id": output_kpi_list[0],
        "avg": total_kpi_metric,
        "THRESHOLD_RAISE": bool(total_kpi_metric > 2600),
        "THRESHOLD_FALL": bool(total_kpi_metric < 699)
    }
    results = []

    results.append(result)
    logger.warning(f"result : {result}.")

    return results
