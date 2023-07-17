#INICIANDO O PROEJETO

#docker-compose build

#docker-compose up -d



DAGS/Funcionamento


DAG ExternalTaskSensor (Trigger)


```Python

import sys

try:
    sys.path.append(r'/home/guilherme/airflow_app_rev1')
except ImportError:
    ...


path = "/home/guilherme/airflow_app_rev1/tab_004.csv"


@task
def downstream_login_branch_1() -> Literal['executado']:
    
    print("Upstream DAG 1 has completed. Starting tasks of branch 1.")
    
    return "executado"

@task
def downstream_checando_informacoes_branch_2() -> Literal['Upstream DAG 2']:
    
    dados = pd.read_csv(path,sep=";")
    
    print("Upstream DAG 2 has completed. Starting tasks of branch 2.")
    return "Upstream DAG 2"


@task
def downstream_segmentando_branch_3() -> Literal['Upstream DAG 3']:
    
    print("Upstream DAG 3 has completed. Starting tasks of branch 3.")
    
    return "Upstream DAG 3"


@task
def downstream_finalizando_entrando_espera_branch_4() -> Literal['Upstream DAG 4']:
    
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


ets_branch_1espera que a my_tasktarefa de upstream_dag_1seja concluída antes de passar para a execução task_branch_1.
ets_branch_2espera que a my_tasktarefa de upstream_dag_2seja concluída antes de passar para a execução task_branch_2.
ets_branch_3espera que a my_tasktarefa de upstream_dag_3seja concluída antes de passar para a execução task_branch_3.


```







DAG SimpleHttpOperator

```Python

@task
def call_python_files(task_type):
    """
    Exemplo Função de chamada antes e depois "Downstream DAG".
    """
    print(f"A ação {task_type} Foi completada!")
    print(request_body)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": duration(minutes=5),
}


@dag(
    start_date=datetime(2023, 7, 1),
    max_active_runs=1,
    schedule="@daily",
    catchup=False,
)
def api_dag_executando_rpa_pyautogui_UI_taskflow():
    start_task = call_python_files("starting")

    api_trigger_dependent_dag = SimpleHttpOperator(
        task_id="api_trigger_dependent_dag",
        http_conn_id="airflow-api",
        endpoint="/api/v1/dags/dependent-dag/dagRuns",
        method="POST",
        headers={"Content-Type": "application/json"},
        data=json_body,
    )

    end_task = call_python_files("ending")

    start_task >> api_trigger_dependent_dag >> end_task


api_dag_executando_rpa_pyautogui_UI_taskflow()



```



"""

Para usar o SimpleHttpOperator para acionar outro DAG, você precisa definir o seguinte:

endpoint: deve estar no formato '/api/v1/dags/<dag-id>/dagRuns'onde <dag-id>está o ID do DAG que você deseja acionar.
data: para acionar uma execução DAG usando esse endpoint, você deve fornecer uma data de execução. No exemplo acima, usamos o execution_dateDAG upstream, mas pode ser qualquer data de sua escolha. Você também pode especificar outras informações sobre a execução do DAG, conforme descrito na documentação da API vinculada acima.
http_conn_id: deve ser uma conexão Airflow do tipo HTTP , com seu domínio Airflow como host. Qualquer autenticação deve ser fornecida como um Login/Senha (se estiver usando a autenticação básica) ou como um Extra no formato JSON. No exemplo abaixo, usamos um token de autorização.

"""



DAG SQLOperator

```Python


```


"""
Os operadores de verificação SQL abstraem consultas SQL para simplificar as verificações de qualidade de dados. Uma diferença entre os operadores de verificação SQL e o padrão BaseSQLOperatoré que os operadores de verificação SQL respondem com um booleano, o que significa que a tarefa falha quando qualquer uma das consultas resultantes falha. Isso é particularmente útil para interromper um pipeline de dados antes que dados inválidos cheguem a um determinado destino. As linhas de código e os valores que falham na verificação são observáveis ​​nos logs do Airflow.

Os seguintes operadores de verificação SQL são recomendados para implementar verificações de qualidade de dados:

SQLColumnCheckOperator: executa uma ou mais verificações de qualidade de dados predefinidas em uma ou mais colunas na mesma tarefa.
SQLTableCheckOperator: executa várias verificações definidas pelo usuário que podem envolver uma ou mais colunas de uma tabela.
SQLCheckOperator: pega qualquer consulta SQL e retorna uma única linha que é avaliada como booleanos. Este operador é útil para verificações mais complicadas que podem abranger várias tabelas do seu banco de dados.
SQLIntervalCheckOperator: compara os dados atuais com os dados históricos.
"""



#Recriando projeto

export AIRFLOW_VERSION=2.6.3

# Extraia a versão do Python que você instalou. Se você estiver usando o Python 3.11, talvez queira definir isso manualmente, conforme observado acima, o Python 3.11 ainda não é compatível.
export PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# Por exemplo, isso instalaria 2.6.3 com python 3.11: https://raw.githubusercontent.com/apache/airflow/constraints-2.6.3/constraints-3.11.txt

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"


#Livy
Livy é uma interface REST de software livre para interagir com o Apache Spark de qualquer lugar. Ele suporta a execução de trechos de código ou programas em um contexto Spark executado localmente ou no Apache Hadoop YARN .

#Construindo Livy Server

git clone https://github.com/apache/incubator-livy.git
cd incubator-livy
docker build -t livy-ci dev/docker/livy-dev-base/
docker run --rm -it -v $(pwd):/workspace -v $HOME/.m2:/root/.m2 livy-ci mvn package# airflow_pipelines_app



Modelo ALS

Alternating Least Square é um algoritmo de fatoração de matriz implementado no Apache Spark ML e construído para problemas de filtragem colaborativa em grande escala.

Fatoração de matrizes (ou decomposição)
A ideia básica é decompor uma matriz em partes menores da mesma forma que podemos fazer para um número. Por exemplo, podemos dizer que o número quatro pode ser decomposto em dois vezes dois (4 = 2 x 2). Da mesma forma, podemos fazer uma decomposição de uma matriz.

Segue um exemplo de como podemos decompor uma matriz que possui avaliações de restaurantes pelos clientes:

numBlocks é o número de blocos nos quais os usuários e itens serão particionados para paralelizar a computação (o padrão é 10).
- classificação é o número de fatores latentes no modelo (o padrão é 10).
- maxIter é o número máximo de iterações a serem executadas (o padrão é 10).
- regParam especifica o parâmetro de regularização em ALS (o padrão é 1.0).
- implicitPrefs especifica se deve usar a variante ALS de feedback explícito ou uma adaptada para dados de feedback implícito (o padrão é falso, o que significa usar feedback explícito).
- alfaé um parâmetro aplicável à variante de feedback implícito do ALS que governa a confiança da linha de base nas observações de preferência (o padrão é 1,0).
- nonnegative especifica se deve ou não usar restrições não negativas para mínimos quadrados (o padrão é falso).




```Python
def run_als():
    als = ALS(maxIter=5,regParam=0.01,userCol='ID_VENDA_index'
              ,itemCol='ID_TICKET_index',ratingCol='QTDE_VENDA')
    
    model = als.fit(training)

    als=ALS(maxIter=5,
        regParam=0.09,
        rank=25,
        userCol="ID_VENDA_index",
        itemCol="ID_TICKET_index",
        ratingCol="QTDE_VENDA",
        coldStartStrategy="drop",
        nonnegative=True)

    predictions=model.transform(test)

```



# airflow_app_rev1
