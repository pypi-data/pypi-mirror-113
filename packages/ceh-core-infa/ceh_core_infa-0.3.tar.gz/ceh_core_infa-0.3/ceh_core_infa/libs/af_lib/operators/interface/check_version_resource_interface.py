from .base_interface import BaseInterface
from .....utils.version import VersionOld
from ....resourse_version.version_main import ResourceVersion
from .....utils.utils import get_current_records


class CheckVersionResourceInterfaceOld(BaseInterface):
    def __init__(self, resources, workflow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resources = resources
        self.workflow = workflow

    @staticmethod
    def __check_version(resources, workflow, logger):
        cur_resources = get_current_records(
            iter_obj=resources,
            key_dict='main_wf_name',
            sought_elem=workflow
        )
        vrs = VersionOld(
            resources=cur_resources,
            param_file_create=True
        )
        vrs.check_version()

        logger.info(
            'Resource versions have been checked. '
            'I start getting all the necessary parameters.'
        )
        params_streams = vrs.params_for_streams
        logger.info(
            'The list of parameters has been successfully generated.'
        )

        return params_streams

    def execute(self):
        executor = self.dynamic_executor(
            ex_func=self.__check_version,
            op_kwargs={
                'resources': self.resources,
                'workflow': self.workflow,
                'logger': self.log
            },
            timer=self.timer
        )

        return executor.executor()


class CheckVersionResourceInterface(BaseInterface):
    def __init__(self, resources, workflow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resources = resources
        self.workflow = workflow

    @staticmethod
    def __check_version(resources, workflow, logger):
        cur_resources = get_current_records(
            iter_obj=resources,
            key_dict='main_wf_name',
            sought_elem=workflow
        )
        vrs = ResourceVersion(
            map_resources=cur_resources,
            param_file_create=True
        )
        vrs.check_map_resources()

        logger.info(
            'Resource versions have been checked. '
            'I start getting all the necessary parameters.'
        )
        params_streams = vrs.get_params_streams()

        logger.info(
            'The list of parameters has been successfully generated.'
        )

        return params_streams

    def execute(self):
        executor = self.dynamic_executor(
            ex_func=self.__check_version,
            op_kwargs={
                'resources': self.resources,
                'workflow': self.workflow,
                'logger': self.log
            },
            timer=self.timer
        )

        return executor.executor()