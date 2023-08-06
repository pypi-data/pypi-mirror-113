from datetime import datetime
from typing import Dict, List, Union

from ..config import PARAMS_LOADING, PATH_CONFIG_FILES_IPC, WF_NAME_PRP
from ..libs.models.resource_state import SourceDt, Source
from ..libs.ipc.parameters.parameters import IPCParams
from ..libs.clients.ceh_resource_client import CehResourse
from ..libs.exceptions.exception import (
    NotValidStatusCode,
    SomeVersionException,
    ResourceStateException
)
from .utils import create_unique_folder


class VersionOld:
    def __init__(
            self,
            resources: List[Dict],
            param_file_create: bool = False
    ):
        self.params_for_streams: Dict = dict()  # Список с параметрами для запуска потоков в IPC
        self.resources: List = resources
        self.param_file_create: bool = param_file_create
        self.folder_ipc_params: Union[str, None] = None

    @staticmethod
    def __get_resource_state(resource_name):
        """Get the state of the resource"""
        cur_res = CehResourse.get_resourse(resource_cd=resource_name)
        if cur_res.state:
            return CehResourse.get_resource_state(resource_cd=resource_name)
        return

    @staticmethod
    def __get_resource(resource_name):
        """Get the resource"""

        try:
            resource = CehResourse.get_resourse(resource_name)
        except NotValidStatusCode:
            resource = None

        return resource

    @staticmethod
    def __is_current_src(sources, src_resource_name):
        for src in sources:
            if isinstance(src, Source):
                if src.resource_cd == src_resource_name:
                    return True
        return False

    def __filter_version(self, operation, src_resource_name):
        """Filter by commented operations"""

        return operation.status.is_committed and self.__is_current_src(operation.sources, src_resource_name)

    @staticmethod
    def __get_version(operation):
        """We get a valid version from the operation"""

        for elem in operation.sources:
            if isinstance(elem, SourceDt):
                continue
            return elem.state.version.version_id

    @staticmethod
    def __get_dt_operations(operation):
        return operation.status.start_dttm

    def __get_max_operations(self, target_state, src_resource_name):
        """We get a max version"""

        flt_operations = list(filter(
            lambda operation: self.__filter_version(
                operation,
                src_resource_name
            ),
            target_state.version.operations
        ))

        if flt_operations:
            max_vrs_operation = max(
                flt_operations,
                key=self.__get_version
            )
        else:
            raise RuntimeError('There is no data for the resource, check the data')

        return max_vrs_operation

    def __get_tgt_info(self, target_state, src_resource_name):
        """Get info about target"""
        operation = self.__get_max_operations(target_state, src_resource_name)

        max_vrs_tgt = self.__get_version(operation)
        dt_tgt = self.__get_dt_operations(operation)

        return max_vrs_tgt, dt_tgt

    def get_params_for_streams(self):
        return self.params_for_streams

    def __provide_params_wf(
            self,
            resource: Dict[str, str],
            max_vrs_tgt: int,
            vrs_source: int,
            ips_params: IPCParams,
            folder: str = None
    ) -> dict:
        params = None

        if PARAMS_LOADING == 'all':
            params = ips_params.get_params_prepare()

            if self.param_file_create:
                params = ips_params.add_conf_file(
                    params=params,
                    wf_name=WF_NAME_PRP,
                    folder=folder,
                    template_name='ipc_pattern_prepare.PARAM',
                    prefix='param_path'
                )

        elif PARAMS_LOADING == 'only_new':
            if max_vrs_tgt != vrs_source:
                params = ips_params.get_params_prepare()

                if self.param_file_create:
                    params = ips_params.add_conf_file(
                        params=params,
                        wf_name=WF_NAME_PRP,
                        folder=folder,
                        template_name='ipc_pattern_prepare.PARAM',
                        prefix='param_path'
                    )

        elif PARAMS_LOADING == 'wait_all':
            if max_vrs_tgt == vrs_source:
                raise SomeVersionException(
                    'The selected parameter {} source {} and target {} resource have the same version.'.format(
                        PARAMS_LOADING,
                        resource['src_resource_name'],
                        resource['tgt_resource_name']
                    )
                )

            params = ips_params.get_params_prepare()

            if self.param_file_create:
                params = ips_params.add_conf_file(
                    params=params,
                    wf_name=WF_NAME_PRP,
                    folder=folder,
                    template_name='ipc_pattern_prepare.PARAM',
                    prefix='param_path'
                )
        params['folder'] = folder
        return params

    def check_version(self):
        for i, resource in enumerate(self.resources):
            target_state = self.__get_resource_state(
                resource['tgt_resource_name']
            )  # Получаем состояние таргета

            source_state = self.__get_resource_state(
                resource['src_resource_name']
            )  # Получаем состояние сурса
            if not source_state:
                raise ResourceStateException(
                    'Source {} has no state.'.format(resource['src_resource_name'])
                )

            source = self.__get_resource(resource['src_resource_name'])
            vrs_source = source.state.version.version_id

            if target_state:
                max_vrs_tgt, dt_tgt = self.__get_tgt_info(
                    target_state, resource['src_resource_name']
                )
                dt_tgt = dt_tgt.strftime("%d.%m.%Y")
            else:
                max_vrs_tgt, dt_tgt = 0, datetime.now().strftime("%d.%m.%Y")

            if self.param_file_create:
                self.folder_ipc_params = create_unique_folder(prefix='Workflow', domain=PATH_CONFIG_FILES_IPC)

            ips_params = IPCParams(
                wf_name=resource['slv_wf_name'],
                resource_version=vrs_source,
                pref_data_load_dt=dt_tgt,
            )

            params = self.__provide_params_wf(
                resource=resource,
                max_vrs_tgt=max_vrs_tgt,
                vrs_source=vrs_source,
                ips_params=ips_params,
                folder=self.folder_ipc_params
            )

            if params:
                resource['prepare_param'] = params

                self.params_for_streams[i] = resource
            elif not params and PARAMS_LOADING != 'only_new':
                raise ValueError('The parameter list cannot be empty')


class Version:
    def __init__(
            self,
            resources: List[Dict],
            param_file_create: bool = False
    ):
        self.params_for_streams: Dict = dict()  # Список с параметрами для запуска потоков в IPC
        self.resources: List = resources
        self.param_file_create: bool = param_file_create
        self.folder_ipc_params: Union[str, None] = None

    @staticmethod
    def __get_resource_state(resource_name):
        """Get the state of the resource"""
        cur_res = CehResourse.get_resourse(resource_cd=resource_name)
        if cur_res.state:
            return CehResourse.get_resource_state(resource_cd=resource_name)
        return

    @staticmethod
    def __get_resource(resource_name):
        """Get the resource"""

        try:
            resource = CehResourse.get_resourse(resource_name)
        except NotValidStatusCode:
            resource = None

        return resource

    @staticmethod
    def __is_current_src(sources, src_resource_name):
        for src in sources:
            if isinstance(src, Source):
                if src.resource_cd == src_resource_name:
                    return True
        return False

    def __filter_version(self, operation, src_resource_name):
        """Filter by commented operations"""

        return operation.status.is_committed and self.__is_current_src(operation.sources, src_resource_name)

    @staticmethod
    def __get_version(operation):
        """We get a valid version from the operation"""

        for elem in operation.sources:
            if isinstance(elem, SourceDt):
                continue
            return elem.state.version.version_id

    @staticmethod
    def __get_dt_operations(operation):
        return operation.status.start_dttm

    def __get_max_operations(self, target_state, src_resource_name):
        """We get a max version"""

        flt_operations = list(filter(
            lambda operation: self.__filter_version(
                operation,
                src_resource_name
            ),
            target_state.version.operations
        ))
        if flt_operations:
            max_vrs_operation = max(
                flt_operations,
                key=self.__get_version
            )
        else:
            raise RuntimeError('There is no data for the resource, check the data')

        return max_vrs_operation

    def __get_tgt_info(self, target_state, src_resource_name):
        """Get info about target"""
        operation = self.__get_max_operations(target_state, src_resource_name)

        max_vrs_tgt = self.__get_version(operation)
        dt_tgt = self.__get_dt_operations(operation)

        return max_vrs_tgt, dt_tgt

    def get_params_for_streams(self):
        return self.params_for_streams

    def __provide_params_wf(
            self,
            resource: Dict[str, str],
            max_vrs_tgt: int,
            vrs_source: int,
            ips_params: IPCParams,
            folder: str = None
    ) -> dict:
        params = None

        if PARAMS_LOADING == 'all':
            params = ips_params.get_params_prepare()

            if self.param_file_create:
                params = ips_params.add_conf_file(
                    params=params,
                    wf_name=WF_NAME_PRP,
                    folder=folder,
                    template_name='ipc_pattern_prepare.PARAM',
                    prefix='param_path'
                )

        elif PARAMS_LOADING == 'only_new':
            if max_vrs_tgt != vrs_source:
                params = ips_params.get_params_prepare()

                if self.param_file_create:
                    params = ips_params.add_conf_file(
                        params=params,
                        wf_name=WF_NAME_PRP,
                        folder=folder,
                        template_name='ipc_pattern_prepare.PARAM',
                        prefix='param_path'
                    )

        elif PARAMS_LOADING == 'wait_all':
            if max_vrs_tgt == vrs_source:
                raise SomeVersionException(
                    'The selected parameter {} source {} and target {} resource have the same version.'.format(
                        PARAMS_LOADING,
                        resource['src_resource_name'],
                        resource['tgt_resource_name']
                    )
                )

            params = ips_params.get_params_prepare()

            if self.param_file_create:
                params = ips_params.add_conf_file(
                    params=params,
                    wf_name=WF_NAME_PRP,
                    folder=folder,
                    template_name='ipc_pattern_prepare.PARAM',
                    prefix='param_path'
                )
        params['folder'] = folder
        return params

    def _get_set_main_wf(self):
        tmp = set()
        for resource in self.resources:
            tmp.add(resource['main_wf_name'])

        return tmp

    def check_version(self):
        for i, resource in enumerate(self.resources):
            target_state = self.__get_resource_state(
                resource['tgt_resource_name']
            )  # Получаем состояние таргета

            source_state = self.__get_resource_state(
                resource['src_resource_name']
            )  # Получаем состояние сурса
            if not source_state:
                raise ResourceStateException(
                    'Source {} has no state.'.format(resource['src_resource_name'])
                )

            source = self.__get_resource(resource['src_resource_name'])
            vrs_source = source.state.version.version_id

            if target_state:
                max_vrs_tgt, dt_tgt = self.__get_tgt_info(
                    target_state, resource['src_resource_name']
                )
                dt_tgt = dt_tgt.strftime("%d.%m.%Y")
            else:
                max_vrs_tgt, dt_tgt = 0, datetime.now().strftime("%d.%m.%Y")

            if self.param_file_create:
                self.folder_ipc_params = create_unique_folder(prefix='Workflow', domain=PATH_CONFIG_FILES_IPC)

            ips_params = IPCParams(
                wf_name=resource['slv_wf_name'],
                resource_version=vrs_source,
                pref_data_load_dt=dt_tgt,

            )

            params = self.__provide_params_wf(
                resource=resource,
                max_vrs_tgt=max_vrs_tgt,
                vrs_source=vrs_source,
                ips_params=ips_params,
                folder=self.folder_ipc_params
            )

            if params:
                resource['prepare_param'] = params

                self.params_for_streams[i] = resource
            elif not params and PARAMS_LOADING != 'only_new':
                raise ValueError('The parameter list cannot be empty')
