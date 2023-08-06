from ...libs.af_lib.operators.operators import IPCLaunchOperator
from airflow.operators.dummy_operator import DummyOperator

MAPPING_OPERATORS = {
    'IPCLaunchOperator': IPCLaunchOperator,
    'DummyOperator': DummyOperator
}
