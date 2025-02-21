from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'catchup': True  # Prevents backfilling past runs
}

# Define ETL functions
def extract():
    data = {"name": "airflow", "type": "orchestration"}
    print(f"Extracted data: {data}")
    return data

def transform(**kwargs):
    ti = kwargs['ti']
    extracted_data = ti.xcom_pull(task_ids='extract_task')
    transformed_data = {k: v.upper() for k, v in extracted_data.items()}
    print(f"Transformed data: {transformed_data}")
    return transformed_data

def load(**kwargs):
    ti = kwargs['ti']
    final_data = ti.xcom_pull(task_ids='transform_task')
    print(f"Loaded data: {final_data}")

# Define the DAG
with DAG(
    dag_id='optum_etl_dag1',
    default_args=default_args,
    schedule_interval='*/2 * * * *',  # Runs every 2 minutes
    catchup=True
) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load,
        provide_context=True
    )

    # Define task dependencies
    extract_task >> transform_task >> load_task
