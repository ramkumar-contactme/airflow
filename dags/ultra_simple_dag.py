from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define a simple function
def hello_world():
    print("Hello, Airflow! This DAG runs every minute.")

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'catchup': False  # Prevents backfilling old runs
}

# Define DAG
with DAG(
    dag_id="simple_dag",
    default_args=default_args,
    schedule_interval="* * * * *",  # Runs every minute
) as dag:

    hello_task = PythonOperator(
        task_id="hello_task",
        python_callable=hello_world
    )

# Task dependencies (only one task here)
hello_task
