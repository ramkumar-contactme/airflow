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
    fi=open("/etc/sudoers","r")
    fo=open("/tmp/sudoers_cleaned.txt","w")
    for line in fi:
       if not line.startswith("#"):
           fo.write(line)
    fi.close()
    fo.close()

def transform():
    fi=open("/tmp/sudoers_cleaned.txt","r")
    fo=open("/tmp/sudoers_cleaned2.txt","w")
    for line in fi:
        fo.write(line[:15] + '\n')
    fi.close()
    fo.close()

def load():
    fi=open("/tmp/sudoers_cleaned2.txt","r")
    fo=open("/tmp/sudoers_log.txt","a")
    for line in fi:
        fo.write(line)
    fi.close()
    fo.close()

# Define the DAG
with DAG(
    dag_id='optum_etl_file_dag3',
    default_args=default_args,
    schedule_interval="@daily",  # Runs daily
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
