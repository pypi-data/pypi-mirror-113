from typing import Tuple

from .ceh_base_operator import CehBaseOperator
from .interface.check_version_resource_interface import (
    CheckVersionResourceInterfaceOld,
    CheckVersionResourceInterface
)


class CheckVersionResourceOperatorOld(CehBaseOperator):
    def __init__(self, workflows: Tuple[str, ...], *args, **kwargs):
        super(CheckVersionResourceOperatorOld, self).__init__(*args, **kwargs)
        self.workflows = workflows

    def execute(self, context):
        resources = context['ti'].xcom_pull(
            key='resources',
            include_prior_dates=True
        )

        for workflow in self.workflows:
            cls = CheckVersionResourceInterfaceOld(
                resources=resources,
                workflow=workflow,
                timer=self._get_timer_poke()
            )
            params = cls.execute()

            if params:
                context['ti'].xcom_push(key=workflow, value=params)


class CheckVersionResourceOperator(CehBaseOperator):
    def __init__(self, workflows: Tuple[str, ...], *args, **kwargs):
        super(CheckVersionResourceOperator, self).__init__(*args, **kwargs)
        self.workflows = workflows

    def execute(self, context):
        resources = context['ti'].xcom_pull(
            key='resources',
            include_prior_dates=True
        )

        for workflow in self.workflows:
            cls = CheckVersionResourceInterface(
                resources=resources,
                workflow=workflow,
                timer=self._get_timer_poke()
            )
            params = cls.execute()

            if params:
                context['ti'].xcom_push(key=workflow, value=params)
