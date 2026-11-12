import json
import nbformat
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


def run_cell(cell_number):
    notebook = nbformat.read(
        "/opt/airflow/include/main.ipynb",
        as_version=4
    )
    exec(notebook.cells[cell_number].source)


with DAG(
    dag_id="student_mental_health_data_preproccessing",
    start_date=datetime(2026, 9, 16),
    schedule=None,
    catchup=False
) as dag:

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
        trigger_dag_id="student_mental_health_data_prediction"
    )

    encoding >> exploring >> trigger_dag_2