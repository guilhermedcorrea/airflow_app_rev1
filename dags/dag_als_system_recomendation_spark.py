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
def system_recomendation_als_pyspark():
    @task(multiple_outputs=True)
    def als_system_recomendation():
        appName="Collaborative Filtering with PySpark"

        spark = SparkSession.builder.appName(appName).getOrCreate()
    
    
    def reader_files(spark):
        df = spark.read.csv('PRODUTO.csv',sep=";", inferSchema=True, header=True)
        df.na.drop("all")
            
        df_filtro = df.select('PLANO', 'ID_TICKET', 'ID_VENDA', 'IDPRODUTO', 'CONTAGEM', 'DATA', 'CONVERSAO_VENDA', 'HORAS_LOGADO7', 'HORAS_FALANDO'
                    , 'QTDE_LIGACOES', 'QTDE_LINHA', 'QTDE_VENDA', 'RANKING', 'Quartile', 'TOTVENDA')
        
        
    def convert_columns(df_filtro):
        
            
        df_filtro.withColumn("CONVERSAO_VENDA", regexp_replace(col("CONVERSAO_VENDA"), ",", "."))

        df_filtro.withColumn("IDPRODUTO", df_filtro.IDPRODUTO.cast(IntegerType()))
        df_filtro.withColumn("CONTAGEM", df_filtro.CONTAGEM.cast(IntegerType()))
        df_filtro.withColumn("IDPRODUTO", df_filtro.IDPRODUTO.cast(IntegerType()))


        df_filtro.withColumn("CONTAGEM", df_filtro.CONTAGEM.cast(IntegerType()))
        df_filtro.withColumn("CONVERSAO_VENDA", df_filtro.CONVERSAO_VENDA.cast(IntegerType()))
        df_filtro.withColumn("HORAS_LOGADO7", df_filtro.HORAS_LOGADO7.cast(IntegerType()))

        df_filtro.withColumn("QTDE_LIGACOES", df_filtro.QTDE_LIGACOES.cast(IntegerType()))
            
        df_filtro.withColumn("QTDE_LINHA", df_filtro.QTDE_LINHA.cast(IntegerType()))
        df_filtro.withColumn("QTDE_LIGACOES", df_filtro.QTDE_LIGACOES.cast(IntegerType()))
        df_filtro.withColumn("QTDE_VENDA", df_filtro.QTDE_VENDA.cast(IntegerType()))
        df_filtro.withColumn("RANKING", df_filtro.RANKING.cast(IntegerType()))
        df_filtro.withColumn("Quartile", df_filtro.Quartile.cast(IntegerType()))
        df_filtro.withColumn("TOTVENDA", df_filtro.TOTVENDA.cast(IntegerType()))
    
    def filtra_colunas(df_filtro):
        new_df = df_filtro.select('ID_TICKET','ID_VENDA','IDPRODUTO','CONTAGEM',
            'CONVERSAO_VENDA','HORAS_LOGADO7','HORAS_FALANDO','QTDE_LIGACOES','QTDE_LINHA','QTDE_VENDA','RANKING','Quartile','TOTVENDA')
            
    def string_indexer(new_df):
            
        indexer = [StringIndexer(inputCol=column, outputCol=column+"_index") for column in ['ID_VENDA', 'ID_TICKET','QTDE_VENDA']]
        pipeline = Pipeline(stages=indexer)
        transformed = pipeline.fit(new_df).transform(new_df)
        rankig_df = transformed.select(['ID_VENDA', 'ID_TICKET','ID_VENDA_index', 'ID_TICKET_index','QTDE_VENDA'
                        
                                            ,'CONVERSAO_VENDA','RANKING','Quartile','CONTAGEM'])
    def traino(rankig_df) -> None:
        training, test = rankig_df.randomSplit([0.8, 0.2])

    def run_als(training) -> None:
        
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

        predictions=model.transform(training)
    
    
    def regressor_evaluation(model,training) -> None:
        evaluator=RegressionEvaluator(metricName="rmse",labelCol="QTDE_VENDA",predictionCol="prediction")
        predictions=model.transform(training)
        rmse=evaluator.evaluate(predictions)
        print("RMSE="+str(rmse))
        
        
        allusers = model.recommendForAllUsers(20).filter(col('ID_VENDA_index')==30).select("recommendations").collect()
        
        
    regressor_evaluation(run_als(traino(string_indexer(filtra_colunas(convert_columns(reader_files(als_system_recomendation())))))))
  

task_group_example = system_recomendation_als_pyspark()