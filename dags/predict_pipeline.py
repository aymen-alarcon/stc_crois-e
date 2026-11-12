import json
import nbformat
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def run_cells():
    notebook = nbformat.read(
        "/opt/airflow/notebooks/model.ipynb",
        as_version=4
    )

    variables = {}

    for cell_number in [1, 2, 3]:
        exec(notebook.cells[cell_number].source, variables)


with DAG(
    dag_id="student_mental_health_data_prediction",
    start_date=datetime(2026, 9, 16),
    schedule=None,
    catchup=False
) as dag:

    training = PythonOperator(
        task_id="train_model",
        python_callable=run_cells
    )