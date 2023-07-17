
from __future__ import annotations
import os
from datetime import datetime
import pytest
from airflow import DAG
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib import parse
import urllib

try:
    from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
    from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
except ImportError:
    pytest.skip("MSSQL provider not available", allow_module_level=True)

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "segmentacaotim"


load_dotenv()

query = os.getenv('SQLQuery')


with DAG(
    DAG_ID,
    schedule="@daily",
    start_date=datetime(2023, 6, 1),
    tags=["SegmentacaoTim"],
    catchup=False,
) as dag:



    create_table_mssql_task = MsSqlOperator(
        task_id="create_country_table",
        mssql_conn_id="airflow_mssql",
        sql=f"{query}"

        ,
        dag=dag,
    )

    @dag.task(task_id="insert_mssql_task")
    def insert_mssql_hook():
        mssql_hook = MsSqlHook(mssql_conn_id="airflow_mssql", schema="comercial")

        rows = os.getenv('SQLtable')
        rows = rows[0] =[row for row in rows]
        
        target_fields = ["name", "continent"]
        mssql_hook.insert_rows(table="Country", rows=rows, target_fields=target_fields)

   
    create_table_mssql_from_external_file = MsSqlOperator(
        task_id="create_table_from_external_file",
        mssql_conn_id="airflow_mssql",
        sql="create_table.sql",
        dag=dag,
    )

    populate_user_table = MsSqlOperator(
        task_id="get_all_vendas",
        mssql_conn_id="airflow_mssql",
        sql=os.path
    )

    get_all_countries = MsSqlOperator(
        task_id="create_groups_segmentation_database",
        mssql_conn_id="airflow_mssql",
        sql=r"""SELECT * FROM comercial.view_segmentacao_tim;""",
    )

    get_all_description = MsSqlOperator(
        task_id="get_all_vendas",
        mssql_conn_id="airflow_mssql",
        sql=r"""SELECT description FROM view_segmentacao_tim WHERE status  IN ('Venda');""",
    )

    get_countries_from_continent = MsSqlOperator(
        task_id="tempo_atendimento",
        mssql_conn_id="airflow_mssql",
        sql=r"""SELECT * FROM Country where {{ params.column }}='{{ params.value }}';""",
        params={"column": "(, )", "": ""},
    )
    (
        create_table_mssql_task
        >> insert_mssql_hook()
        >> create_table_mssql_from_external_file
        >> populate_user_table
        >> get_all_countries
        >> get_all_description
        >> get_countries_from_continent
    )
   

    from tests.system.utils.watcher import watcher


    list(dag.tasks) >> watcher()
from tests.system.utils import get_test_run  # noqa: E402


test_run = get_test_run(dag)