import json
import nbformat
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


def run_cell(cell_number):
    notebook = nbformat.read(
        "/opt/airflow/notebooks/model.ipynb",
        as_version=4
    )
    exec(notebook.cells[cell_number].source)


def read_json_file():
    file_path = "/opt/airflow/data/data.json"
    with open(file_path, "r") as f:
        return json.load(f)


with DAG(
    dag_id="student_mental_health_data_preproccessing",
    start_date=datetime(2026, 9, 16),
    schedule=None,
    catchup=False
) as dag:

    read_json_task = PythonOperator(
        task_id="read_json",
        python_callable=read_json_file
    )

    encoding = PythonOperator(
        task_id="encoding",
        python_callable=run_cell,
        op_args=[1]
    )

    exploring = PythonOperator(
        task_id="exploring",
        python_callable=run_cell,
        op_args=[2]
    )

    trigger_dag_2 = TriggerDagRunOperator(
        task_id="trigger_dw_update",
        trigger_dag_id="predict"
    )

    read_json_task >> encoding >> exploring >> trigger_dag_2