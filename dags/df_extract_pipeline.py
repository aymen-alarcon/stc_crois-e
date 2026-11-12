import sys
import json
from datetime import datetime
from airflow import DAG
import nbformat
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

sys.path.append("/opt/airflow")

def run_cell(cell_number):
    notebook = nbformat.read("/opt/airflow/include/main.ipynb", as_version=4)

    variables = {}
    exec(notebook.cells[cell_number].source, variables)

    return variables["df"].to_dict(orient="records")

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

    trigger_dag_2 = TriggerDagRunOperator(
        task_id="trigger_dw_update",
        trigger_dag_id="student_mental_health_data_preproccessing"
    )

    extract_task >>  trigger_dag_2
