
from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import (
    SQLColumnCheckOperator,
    SQLTableCheckOperator,
    SQLCheckOperator,
)
import os
from datetime import datetime

import pytest

from airflow import DAG

try:
    from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
    from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
except ImportError:
    pytest.skip("MSSQL provider not available", allow_module_level=True)


from pendulum import datetime

_CONN_ID = "MSSQL_segmentacao"
_TABLE_NAME = "comercial.ranking_atendimento_tim"


@dag(
    start_date=datetime(2023, 7, 1),
    schedule=None,
    catchup=False,
    template_searchpath=["/home/guilherme/airflow_app_rev1/dags/include/"],
)
def sql_data_quality():
    create_table = MsSqlOperator(
        task_id="create_table",
        sqlite_conn_id=_CONN_ID,
        sql=f"""
        {_TABLE_NAME}(
            IF NOT EXISTS CREATE TABLE  {_TABLE_NAME} PRIMARY KEY,
            id_agente INT,
            horas_logado INT,
            horas_falando FLOAT,
            tempo_falando FLOAT,
            qtde_venda INT,
            qtde_linha INT,
            qtde_ligacoes INT,
            conversao_venda FLOAT,
            fim_ultimo_alo DATETIME,
            ultima_atualizacao DATETIME DEFAULT GETDATE(),
            ranking INT,
            grupo INT)
        """,
    )

    populate_data = MsSqlOperator(
        task_id="insert_tabela",
        sqlite_conn_id=_CONN_ID,
        sql=f"""
            IF NOT EXISTS (SELECT * FROM {_TABLE_NAME}
            WHERE IDAGENTE IN (SELECT idagente FROM {_TABLE_NAME}))
            BEGIN

                INSERT INTO {_TABLE_NAME} (idagente,tipo_campanha,qtd_deriv,qtd_venda,qtd_manual,conversao_derivada,linhas,data_cadastro)
                SELECT IDAGENTE,TIPO_CAMPANHA,QTD_DERIV,QTD_VENDA,QTDE_MANUAL,CONV_DERIVADA,linhas,DATACADASTRO
                FROM BANCO_TESTE.dbo.SEGMENTACAO_atendimento_tim
            END

        ELSE
            BEGIN
                UPDATE seg
                    SET 
                    seg.idagente = satendimento.IDAGENTE
                    ,seg.tipo_campanha =satendimento.TIPO_CAMPANHA
                    ,seg.qtd_deriv =satendimento.QTD_DERIV
                    ,seg.qtd_venda =satendimento.QTD_VENDA
                    ,seg.qtd_manual =satendimento.QTDE_MANUAL
                    ,seg.conversao_derivada =satendimento.CONV_DERIVADA
                    ,seg.linhas =satendimento.linhas
                    ,seg.data_cadastro = satendimento.DATACADASTRO

                FROM comercial.segmentacao_tim as seg
                LEFT JOIN BANCO_TESTE.dbo.SEGMENTACAO_atendimento_tim as satendimento ON seg.idagente = satendimento.IDAGENTE

            END
        """,
    )

    column_checks = SQLColumnCheckOperator(
        task_id="checkando_valores",
        conn_id=_CONN_ID,
        table=_TABLE_NAME,
        partition_clause="bird_name IS NOT NULL",
        column_mapping={
            "bird_name": {
                "null_check": {"equal_to": 0},
                "distinct_check": {"geq_to": 2},
            },
            "observation_year": {"max": {"less_than": 2023}},
            "bird_happiness": {"min": {"greater_than": 0}, "max": {"leq_to": 10}},
        },
    )

    table_checks = SQLTableCheckOperator(
        task_id="checando_tabela",
        conn_id=_CONN_ID,
        table=_TABLE_NAME,
        checks={
            "row_count_check": {"check_statement": "COUNT(*) >= 3"},
            "average_happiness_check": {
                "check_statement": "AVG(bird_happiness) >= 9",
                "partition_clause": "observation_year >= 2021",
            },
        },
    )

    custom_check = SQLCheckOperator(
        task_id="cusmotizando",
        conn_id=_CONN_ID,
        sql="custom_check.sql",
        params={"table_name": _TABLE_NAME},
    )

    create_table >> populate_data >> [column_checks, table_checks, custom_check]


sql_data_quality()