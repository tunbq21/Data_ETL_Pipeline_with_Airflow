from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

# Định nghĩa DAG
with DAG(
    dag_id="spark_simple_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # chạy thủ công
    catchup=False,
    tags=['example', 'spark']
) as dag:

    # Task chạy Spark job
    run_spark = SparkSubmitOperator(
        task_id='run_simple_spark_job',
        application='/opt/airflow/dags/scripts/simple_job.py',  # file Spark
        conn_id='spark_default',  # connection Spark trong Airflow
        verbose=True
    )

    run_spark
