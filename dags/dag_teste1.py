from airflow.decorators import dag, task_group, task
from pendulum import datetime



"""Teste Dag"""
@dag(
    start_date=datetime(2022, 12, 1),
    schedule=None,
    catchup=False,
)
def task_group_mapping_example():

    @task_group(group_id="group1")
    def tg1(my_num):
        @task
        def print_num(num):
            return num

        @task
        def add_42(num):
            return num + 42

        print_num(my_num) >> add_42(my_num)

 
    @task
    def pull_xcom(**context):
        pulled_xcom = context["ti"].xcom_pull(
        
            task_ids=["group1.add_42"],
     
            map_indexes=[2, 3],
            key="return_value",
        )

   
        print(pulled_xcom)

    tg1_object = tg1.expand(my_num=[19, 23, 42, 8, 7, 108])


    tg1_object >> pull_xcom()


task_group_mapping_example()