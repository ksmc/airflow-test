from datetime import datetime
from airflow.models import DAG
from kubernetes.client import models as k8s
from airflow.operators.bash import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

with DAG('remote-logging',
	description='test-remote-logging',
	start_date=datetime(2021, 1, 1),
	catchup=False
	) as dag:

	t0 = BashOperator(
        task_id = 'print_date',
        bash_command='date'
    	)

	t1 = KubernetesPodOperator(
		task_id='do-something',
		namespace='airflow',
		image='busybox',
		cmds=["bash", "-cx"],
        	arguments=["echo", "10", "echo pwd"],
		name="do_this",
		is_delete_operator_pod=True,
		in_cluster=True,
		get_logs=True
		)
	t0 >> t1
