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


import logging, time
from pyspark.sql                  import SparkSession
from pyspark.sql.types            import StructType, StructField, StringType, DoubleType, TimestampType
from pyspark.sql.functions        import from_json, col, window, avg, min, max, first, last, stddev, when, round
from common.tools.kafka.Variables import KafkaConfig, KafkaTopic

LOGGER = logging.getLogger(__name__)

def DefiningSparkSession():
    # Create a Spark session with specific spark verions (3.5.0)
    return SparkSession.builder \
            .appName("Analytics") \
            .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
            .getOrCreate()

def SettingKafkaConsumerParams():   # TODO:  create get_kafka_consumer() in common with inputs (bootstrap server, subscribe, startingOffset and failOnDataLoss with default values)
    return {
            # "kafka.bootstrap.servers": '127.0.0.1:9092',
            "kafka.bootstrap.servers": KafkaConfig.get_kafka_address(),
            "subscribe"              : KafkaTopic.VALUE.value,         # topic should have atleast one message before spark session 
            "startingOffsets"        : 'latest',
            "failOnDataLoss"         : 'false'              # Optional: Set to "true" to fail the query on data loss
        }

def DefiningRequestSchema():
    return StructType([
            StructField("time_stamp" ,  StringType()  , True),
            StructField("kpi_id"     ,  StringType()  , True),
            StructField("kpi_value"  ,  DoubleType()  , True)
        ])

def GetAggregations(oper_list):
    # Define the possible aggregation functions
    agg_functions = {
        'avg'  :  round(avg    ("kpi_value"), 3) .alias("avg_value"),
        'min'  :  round(min    ("kpi_value"), 3) .alias("min_value"),
        'max'  :  round(max    ("kpi_value"), 3) .alias("max_value"),
        'first':  round(first  ("kpi_value"), 3) .alias("first_value"),
        'last' :  round(last   ("kpi_value"), 3) .alias("last_value"),
        'stdev':  round(stddev ("kpi_value"), 3) .alias("stdev_value")
    }
    return [agg_functions[op] for op in oper_list if op in agg_functions]   # Filter and return only the selected aggregations

def ApplyThresholds(aggregated_df, thresholds):
    # Apply thresholds (TH-Fail and TH-RAISE) based on the thresholds dictionary on the aggregated DataFrame.
    
    # Loop through each column name and its associated thresholds
    for col_name, (fail_th, raise_th) in thresholds.items():
        # Apply TH-Fail condition (if column value is less than the fail threshold)
        aggregated_df = aggregated_df.withColumn(
            f"{col_name}_THRESHOLD_FALL", 
            when(col(col_name) < fail_th, True).otherwise(False)
        )
        # Apply TH-RAISE condition (if column value is greater than the raise threshold)
        aggregated_df = aggregated_df.withColumn(
            f"{col_name}_THRESHOLD_RAISE", 
            when(col(col_name) > raise_th, True).otherwise(False)
        )
    return aggregated_df

def SparkStreamer(key, kpi_list, oper_list, thresholds, stop_event,
                  window_size=None, win_slide_duration=None, time_stamp_col=None):
    """
    Method to perform Spark operation Kafka stream.
    NOTE: Kafka topic to be processesd should have atleast one row before initiating the spark session. 
    """
    kafka_consumer_params = SettingKafkaConsumerParams()         # Define the Kafka consumer parameters
    schema                = DefiningRequestSchema()              # Define the schema for the incoming JSON data
    spark                 = DefiningSparkSession()               # Define the spark session with app name and spark version
    
    # extra options default assignment
    if window_size        is None: window_size        = "60 seconds"    # default
    if win_slide_duration is None: win_slide_duration = "30 seconds"    # default
    if time_stamp_col     is None: time_stamp_col     = "time_stamp"    # default
    
    try:
        # Read data from Kafka
        raw_stream_data = spark \
            .readStream \
            .format("kafka") \
            .options(**kafka_consumer_params) \
            .load()

        # Convert the value column from Kafka to a string
        stream_data          = raw_stream_data.selectExpr("CAST(value AS STRING)")
        # Parse the JSON string into a DataFrame with the defined schema
        parsed_stream_data   = stream_data.withColumn("parsed_value", from_json(col("value"), schema))
        # Select the parsed fields
        final_stream_data    = parsed_stream_data.select("parsed_value.*")
        # Convert the time_stamp to proper timestamp (assuming it's in ISO format)
        final_stream_data    = final_stream_data.withColumn(time_stamp_col, col(time_stamp_col).cast(TimestampType()))
        # Filter the stream to only include rows where the kpi_id is in the kpi_list
        filtered_stream_data = final_stream_data.filter(col("kpi_id").isin(kpi_list))
         # Define a window for aggregation
        windowed_stream_data = filtered_stream_data \
                                .groupBy(
                                    window( col(time_stamp_col), 
                                           window_size, slideDuration=win_slide_duration
                                           ),
                                    col("kpi_id")
                                ) \
                                .agg(*GetAggregations(oper_list))
        # Apply thresholds to the aggregated data
        thresholded_stream_data = ApplyThresholds(windowed_stream_data, thresholds)

        # --- This will write output on console: FOR TESTING PURPOSES
        # Start the Spark streaming query
        # query = thresholded_stream_data \
        #     .writeStream \
        #     .outputMode("update") \
        #     .format("console") 

        # --- This will write output to Kafka: ACTUAL IMPLEMENTATION
        query = thresholded_stream_data \
            .selectExpr(f"CAST(kpi_id AS STRING) AS key", "to_json(struct(*)) AS value") \
            .writeStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", KafkaConfig.get_kafka_address()) \
            .option("topic",                   KafkaTopic.ALARMS.value) \
            .option("checkpointLocation",      "analytics/.spark/checkpoint") \
            .outputMode("update")

        # Start the query execution
        queryHandler = query.start()

        # Loop to check for stop event flag. To be set by stop collector method.
        while True:
            if stop_event.is_set():
                LOGGER.debug("Stop Event activated. Terminating in 5 seconds...")
                print       ("Stop Event activated. Terminating in 5 seconds...")
                time.sleep(5)
                queryHandler.stop()
                break
            time.sleep(5)

    except Exception as e:
        print("Error in Spark streaming process: {:}".format(e))
        LOGGER.debug("Error in Spark streaming process: {:}".format(e))
