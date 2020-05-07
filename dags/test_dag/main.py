"""
This dag only runs some simple tasks to test Airflow's task execution.
"""
from airflow.models.dag import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow import utils

DAG_ID = 'test_dag'

DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': True,
    'start_date': utils.dates.days_ago(2)
}

dag = DAG(**{
    'dag_id': DAG_ID,
    'schedule_interval': '*/10 * * * *',  # https://crontab.guru/#*/10_*_*_*_*
    'default_args': DEFAULT_ARGS,
})


with dag:
    run_this_1 = DummyOperator(task_id='run_this_1')
    run_this_2 = DummyOperator(task_id='run_this_2')
    run_this_2.set_upstream(run_this_1)
    run_this_3 = DummyOperator(task_id='run_this_3')
    run_this_3.set_upstream(run_this_2)
    BashOperator(task_id='say_hi', bash_command='echo hi')
