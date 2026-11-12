import sys
import json
from datetime import datetime
from airflow import DAG
import nbformat
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

sys.path.append("/opt/airflow")

def run_cell(cell_number):
    notebook = nbformat.read("/opt/airflow/main.ipynb", as_version=4)
    exec(notebook.cells[cell_number].source)

def generate_json_file(student_mental_health_data):
    file_path = "/opt/airflow/data/data.json"
    with open(file_path, "w") as f:
        json.dump(student_mental_health_data, f)

with DAG(
    dag_id="student_mental_health_data_extraction",
    start_date=datetime(2026, 11, 12),
    schedule="@hourly",
    catchup=False
) as dag:
    
    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=run_cell,
        op_args=[0]
    )

    generate_json_task = PythonOperator(
        task_id="generate_json",
        python_callable=generate_json_file,
        op_args=[extract_task.output]
    )

    trigger_dag_2 = TriggerDagRunOperator(
        task_id="trigger_dw_update",
        trigger_dag_id="preproccessing"
    )

    extract_task >> generate_json_task >> trigger_dag_2
