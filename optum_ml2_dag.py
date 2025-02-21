from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import psycopg2
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Default arguments for DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'catchup': False
}

# PostgreSQL Connection details
DB_PARAMS = {
    "dbname": "your_db",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": 5432
}

# Define DAG
dag = DAG(
    dag_id="optum_ml_pipeline_2_dag",
    default_args=default_args,
    schedule_interval="@daily"  # Runs daily
)

# Step 1: Extract Data from PostgreSQL
def extract():
    conn = psycopg2.connect(**DB_PARAMS)
    query = "SELECT feature1, feature2, feature3, target FROM ml_data;"
    df = pd.read_sql(query, conn)
    conn.close()
    df.to_csv("/tmp/data.csv", index=False)
    print("Data Extracted")

# Step 2: Preprocess Data
def transform():
    df = pd.read_csv("/tmp/data.csv")
    df.fillna(df.mean(), inplace=True)  # Fill missing values
    df.to_csv("/tmp/clean_data.csv", index=False)
    print("Data Transformed")

# Step 3: Train Model
def train():
    df = pd.read_csv("/tmp/clean_data.csv")
    X = df.drop(columns=["target"])
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Save model
    with open("/tmp/model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Model Trained")

# Step 4: Evaluate Model
def evaluate():
    df = pd.read_csv("/tmp/clean_data.csv")
    X = df.drop(columns=["target"])
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with open("/tmp/model.pkl", "rb") as f:
        model = pickle.load(f)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy:.2f}")

# Define Airflow Tasks
extract_task = PythonOperator(
    task_id="extract_task",
    python_callable=extract,
    dag=dag
)

transform_task = PythonOperator(
    task_id="transform_task",
    python_callable=transform,
    dag=dag
)

train_task = PythonOperator(
    task_id="train_task",
    python_callable=train,
    dag=dag
)

evaluate_task = PythonOperator(
    task_id="evaluate_task",
    python_callable=evaluate,
    dag=dag
)

# Task Dependencies
extract_task >> transform_task >> train_task >> evaluate_task
