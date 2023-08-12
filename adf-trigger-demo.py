from datetime import datetime
from airflow.models import DAG
from kubernetes.client import models as k8s
from airflow.operators.bash import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

with DAG('adf-pipeline-trigger',
	description='MPH Airflow-ADF Integration demo.',
	start_date=datetime(2021, 1, 1),
	catchup=False
	) as dag:

	t0 = BashOperator(
        task_id = 'print_date',
        bash_command='date'
    	)

	t1 = KubernetesPodOperator(
		task_id='adf_pipeline',
		namespace='unicron-airflow',
		image='unicronacr.azurecr.io/rl/adf-pipeline',
		image_pull_secrets=[k8s.V1LocalObjectReference('unicronacr-secret')],
		name="adf_pipeline",
		is_delete_operator_pod=True,
		in_cluster=True,
		get_logs=True
		)
	t0 >> t1