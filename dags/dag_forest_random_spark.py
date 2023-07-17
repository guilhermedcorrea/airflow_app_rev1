from airflow.decorators import dag, task, task_group
from airflow.utils.task_group import TaskGroup
import pendulum
import json
from airflow.decorators import dag, task, task_group
from airflow.utils.task_group import TaskGroup
import pendulum
import json
import findspark
import os

findspark.init(r'/home/guilherme/airflow_pipelines_app/jdk-20.0.1')

os.environ["SPARK_HOME"] =r'/home/guilherme/airflow_pipelines_app/spark/spark'
os.environ["JAVA_HOME"]=r'/home/guilherme/airflow_pipelines_app/jdk-20.0.1'
os.environ["LIVY_CONF_DIR"]=r'/home/guilherme/airflow_pipelines_app/livy_server/apache-livy'

from pyspark import SparkContext
from pyspark.ml.recommendation import ALS
from pyspark.sql import SparkSession ,Row
from pyspark.sql.functions import col, regexp_replace
from pyspark.sql import SQLContext
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.types import StructType,StructField,IntegerType
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.types import StructType,StructField,IntegerType
import pyspark.sql.functions as F
import pyspark.sql.types as T




@dag(schedule=None, start_date=pendulum.datetime(2023, 7, 1, tz="UTC"), catchup=False)
def algoritmo_forest_random_pyspark():
    @task(task_id="extract", retries=2)
    def extract_data():
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        order_data_dict = json.loads(data_string)
        return order_data_dict

    @task()
    def leitura_e_checagem(order_data_dict: dict):
        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value": total_order_value}

    @task()
    def conversao_tipos_dados(order_data_dict: dict):
        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value
            avg_order_value = total_order_value / len(order_data_dict)

        return {"avg_order_value": avg_order_value}

    @task_group
    def transform_values(order_data_dict):
        return {
            "avg": conversao_tipos_dados(order_data_dict),
            "total": leitura_e_checagem(order_data_dict),
        }

    @task()
    def load(order_values: dict):
        print(
            f"""Total: {order_values['total']['total valor']:.2f} 
            Clusters: {order_values['avg']['clusters']:.2f}"""
        )

    load(transform_values(extract_data()))


task_group_example = algoritmo_forest_random_pyspark()