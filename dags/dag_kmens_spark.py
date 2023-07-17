from airflow.decorators import dag, task, task_group
from airflow.utils.task_group import TaskGroup
import pendulum
import json




@dag(schedule=None, start_date=pendulum.datetime(2023, 7, 1, tz="UTC"), catchup=False)
def algoritmo_kmeans_pyspark():
    @task(task_id="extract", retries=2)
    def extract_data():
        print("Select Query database")

    @task()
    def check_columns():
        print("Check Columns")
        ...
        
    @task() 
    def convert_columns():
        print("convert columns")
        ...
        
        
    @task()
    def call_algoritmo(order_data_dict: dict):
        print("Call algoritmos")
        ...
       
    
    @task()
    def transform_avg(order_data_dict: dict):
        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value
            avg_order_value = total_order_value / len(order_data_dict)

        return {"avg_order_value": avg_order_value}

    @task_group
    def transform_values(order_data_dict):
        return {
            "avg": transform_avg(order_data_dict),
            "total": call_algoritmo(order_data_dict),
        }

    @task()
    def load(order_values: dict):
        print(
            f"""Total order value is: {order_values['total']['total_order_value']:.2f} 
            and average order value is: {order_values['avg']['avg_order_value']:.2f}"""
        )

    load(transform_values(extract_data()))


task_group_example = algoritmo_kmeans_pyspark()