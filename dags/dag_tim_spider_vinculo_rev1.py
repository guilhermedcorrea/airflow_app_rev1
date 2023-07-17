import os
from datetime import datetime
from airflow.decorators import dag, task
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.empty import EmptyOperator
from pendulum import datetime, duration
import pandas as pd


"""Em construção"""

"""Teste spider tim"""



import sys

try:
    sys.path.append(r'/home/guilherme/airflow_app_rev1')
except ImportError:
    ...


path = "/home/guilherme/airflow_app_rev1/tab_004.csv"


@task
def downstream_login_branch_1():
    
    print("Upstream DAG 1 has completed. Starting tasks of branch 1.")
    
    return "executado"

@task
def downstream_checando_informacoes_branch_2():
    
    dados = pd.read_csv(path,sep=";")
    
    print("Upstream DAG 2 has completed. Starting tasks of branch 2.")
    return "Upstream DAG 2"


@task
def downstream_segmentando_branch_3():
    
    print("Upstream DAG 3 has completed. Starting tasks of branch 3.")
    
    return "Upstream DAG 3"


@task
def downstream_finalizando_entrando_espera_branch_4():
    
    print("Upstream DAG 4 has completed. Starting tasks of branch 4.")
    
    return "Upstream DAG 4"



default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": duration(minutes=3),
}


@dag(
    start_date=datetime(2023, 7, 1),
    max_active_runs=3,
    schedule="*/1 * * * *",
    catchup=False,
)
def spider_tim_vinculacao_sensor_taskflow_dag():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    ets_branch_1 = ExternalTaskSensor(
        task_id="ets_spider_login_branch_1",
        external_dag_id="upstream_dag_1",
        external_task_id="my_task",
        allowed_states=["success"],
        failed_states=["failed", "skipped"],
    )

    task_spider_login_branch_1 = downstream_login_branch_1()

    ets_branch_2 = ExternalTaskSensor(
        task_id="ets_checando_informacoe_branch_2",
        external_dag_id="upstream_dag_2",
        external_task_id="my_task",
        allowed_states=["success"],
        failed_states=["failed", "skipped"],
    )

    task_checando_informacoes_branch_2 = downstream_checando_informacoes_branch_2()

    ets_branch_3 = ExternalTaskSensor(
        task_id="ets_segmentando_branch_3",
        external_dag_id="upstream_dag_3",
        external_task_id="my_task",
        allowed_states=["success"],
        failed_states=["failed", "skipped"],
    )

    task_segmentando_branch_3 = downstream_segmentando_branch_3()
    
    ets_branch_4 = ExternalTaskSensor(
        task_id="ets_finalizando_branch_4",
        external_dag_id="upstream_finalizando_entrando_dag_4",
        external_task_id="my_task",
        allowed_states=["success"],
        failed_states=["failed", "skipped"],
    )

    task_finalizando_branch_4 = downstream_finalizando_entrando_espera_branch_4()

    start >> [ets_branch_1, ets_branch_2, ets_branch_3,ets_branch_4]

    ets_branch_1 >> task_spider_login_branch_1
    ets_branch_2 >> task_checando_informacoes_branch_2
    ets_branch_3 >> task_segmentando_branch_3
    ets_branch_4 >> task_finalizando_branch_4

    [task_spider_login_branch_1, task_checando_informacoes_branch_2, task_segmentando_branch_3,task_finalizando_branch_4] >> end


spider_tim_vinculacao_sensor_taskflow_dag()


"""
ets_branch_1espera que a my_tasktarefa de upstream_dag_1seja concluída antes de passar para a execução task_branch_1.
ets_branch_2espera que a my_tasktarefa de upstream_dag_2seja concluída antes de passar para a execução task_branch_2.
ets_branch_3espera que a my_tasktarefa de upstream_dag_3seja concluída antes de passar para a execução task_branch_3.


"""