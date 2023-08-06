from copy import copy
from datetime import datetime
from typing import Dict, Union

from ceh_core_infa.config import (
    DEFAULT_PARAMS_FOR_LOAD,
    DEFAULT_PARAMS_FOR_PREPARE,
    BASE_URL_SEQ_GENERATOR,
    VERSION_CEH_SEQ_GENERATOR,
    DB_CONNECTION,
    META_VERSION,
    IPC_DEFAULT_ARGS,
)

from ...clients.increment_client import Sequence
from ....utils.utils import generate_files_params


class IPCParams:
    __slots__ = (
        'wf_name',
        'resource_version',
        'pref_data_load_dt'
    )

    def __init__(
            self,
            wf_name: str,
            resource_version: int,
            pref_data_load_dt: Union[str, datetime]
    ):
        self.wf_name = wf_name
        self.resource_version = resource_version
        self.pref_data_load_dt = pref_data_load_dt

    @staticmethod
    def _get_seq_url():
        return f'{BASE_URL_SEQ_GENERATOR}api/' \
               f'{VERSION_CEH_SEQ_GENERATOR}/sequences/'

    def _get_instance_id(self):
        inc = Sequence.create_increment(self.wf_name, 1)
        return inc.value

    @staticmethod
    def _get_meta_version_id():
        inc = Sequence.create_increment('meta_inf', 1)
        return inc.value

    @classmethod
    def add_conf_file(
            cls,
            params: Dict[str, str],
            template_name: str,
            wf_name: str,
            folder: str,
            prefix: str
    ):
        params[prefix] = generate_files_params(
            param=params,
            wf_name=wf_name,
            folder=folder,
            template_name=template_name
        )

        return params

    def get_params_prepare(self):
        """Get parameters for a workflow based on the standard"""

        params = copy(DEFAULT_PARAMS_FOR_PREPARE)

        params['DBConnection_ODBC'] = DB_CONNECTION
        params['INSTANCE_ID'] = self._get_instance_id()
        params['WORKFLOW_NAME'] = self.wf_name
        params['SRC_VERSION_ID'] = self.resource_version
        params['META_VERSION_ID'] = META_VERSION
        params['PREV_DATA_LOAD_DT'] = self.pref_data_load_dt
        params['AUTOINC_SRV_URL'] = self._get_seq_url()

        return params

    @classmethod
    def get_params_load(cls, old_param, tgt_current_vrs):
        """Get parameters for a workflow based on the standard for load"""

        params = copy(DEFAULT_PARAMS_FOR_LOAD)

        params['DBConnection_ODBC'] = old_param['DBConnection_ODBC']
        params['INSTANCE_ID'] = old_param['INSTANCE_ID']
        params['TGT_CUR_VERSION_ID'] = tgt_current_vrs
        params['META_VERSION_ID'] = old_param['META_VERSION_ID']
        params['WORKFLOW_NAME'] = old_param['WORKFLOW_NAME']
        params['AUTOINC_SRV_URL'] = old_param['AUTOINC_SRV_URL']

        return params


class IPCParamsZI(IPCParams):
    def __init__(self, params, *args, **kwargs):
        super(IPCParamsZI, self).__init__(*args, **kwargs)

        self.params = params

    def get_params_prepare(self):
        """Get parameters"""

        params = copy(DEFAULT_PARAMS_FOR_PREPARE)

        params['DBConnection_ODBC'] = self.params['db_connection']
        params['INSTANCE_ID'] = self.params['instance_id']
        params['WORKFLOW_NAME'] = self.params['slv_wf_name']
        params['SRC_VERSION_ID'] = self.params['src_version_id']
        params['META_VERSION_ID'] = self.params['meta_version_id']
        params['PREV_DATA_LOAD_DT'] = self.params['prev_data_load_dt']
        params['AUTOINC_SRV_URL'] = self._get_seq_url()

        return params

    def get_params_load(self, input_params=None, tgt_current_vrs=None):
        """Get parameters for a workflow based on the standard for load"""

        params = copy(DEFAULT_PARAMS_FOR_LOAD)

        params['DBConnection_ODBC'] = self.params['db_connection']
        params['INSTANCE_ID'] = self.params['instance_id']
        params['TGT_CUR_VERSION_ID'] = tgt_current_vrs or self.params[
            'tgt_version_id'
        ]
        params['META_VERSION_ID'] = self.params['meta_version_id']
        params['WORKFLOW_NAME'] = self.params['slv_wf_name']
        params['AUTOINC_SRV_URL'] = self._get_seq_url()

        return params


class LaunchParam:
    _map = {
        'user': 'ipc_login',
        'password': 'ipc_password',
        'service': 'service',
        'domain': 'domain',
        'folder': 'ipc_template',
        'timeout': 'timeout',
        'instance': 'slv_wf_name',
        'wait': 'wf_name',
        'paramfile': 'path_file_conf',
        'local_paramfile': 'param_path',
    }

    args = {
        'user': None,
        'password': None,
        'service': None,
        'domain': None,
        'folder': None,
        'timeout': None,
        'instance': None,
        'wait': None,
        'paramfile': None,
        'local_paramfile': None,
    }

    def __init__(
            self,
            raw_params,
            prefix: str = None,
            is_depth_search: bool = False,
            not_case_dependency: bool = False,
            **kwargs

    ) -> None:
        self.raw_params = raw_params
        self.one_dimen_params = dict()
        self.is_depth_search = is_depth_search
        self.not_case_dependency = not_case_dependency
        self.prefix = prefix
        self.kwargs = kwargs

    def __parse_to_one_dimensional(self, params=None):
        """Превращаем наш словарь в одномерный"""
        if not params:
            params = self.raw_params

        for param in params:
            if isinstance(params[param], dict) and self.prefix == param:
                self.__parse_to_one_dimensional(params=params[param])
            elif isinstance(params[param], dict):
                self.__parse_to_one_dimensional(params=params[param])
            elif isinstance(
                    params[param],
                    (int, str)
            ) or params[param] is None:
                if param in self.one_dimen_params:
                    raise ValueError(
                        'The parameter {} already '
                        'exists with the value {}'.format(
                            param,
                            self.one_dimen_params[param]
                        )
                    )

                self.one_dimen_params[
                    param.lower()
                    if self.not_case_dependency and isinstance(
                        param,
                        str
                    ) else param
                ] = params[param]

            else:
                raise TypeError(
                    'The parameter {} must not be of type {}.'.format(
                        param,
                        type(param)
                    )
                )

    def __search_element(
            self,
            element: Union[int, str],
            params=None,
            glob: bool = False
    ) -> tuple:
        """Ищем элемент по ключу в глубину"""
        if not params:
            params = self.raw_params

        result = None

        for param in params:
            if isinstance(params[param], dict):
                result = self.__search_element(
                    element=element,
                    params=params[param]
                )

            elif isinstance(
                    params[param],
                    dict
            ) and self.prefix is None:  # делаем поиск рекусивно
                result = self.__search_element(
                    element=element,
                    params=params[param]
                )
            elif isinstance(params[param], (int, str)) or glob:
                if (
                        param.lower()
                        if self.not_case_dependency and isinstance(
                            param, str
                        ) else param
                ) == element:
                    return element, params[param]
            else:
                raise TypeError(
                    'The parameter {} must not be of type {}.'.format(
                        param,
                        type(params[param])
                    )
                )

            if result:
                break

        return result

    def __del_extra_dict_params(self, params, result=None):
        if not result:
            result = dict()

        for param in params:
            if param == self.prefix and isinstance(params[param], dict):
                result[param] = params[param]
            elif isinstance(params[param], dict):
                if self.prefix in params[param]:
                    result[param] = {self.prefix: params[param][self.prefix]}
                else:
                    result[param] = self.__del_extra_dict_params(params[param])
            elif isinstance(params[param], (int, str)):
                result[param] = params[param]

        return result

    def get_prarams(self):
        # делаем словарь одномерным если это необходимо
        if not self.is_depth_search:
            self.__parse_to_one_dimensional()

        # выбираем необходимы список параметров
        params = self.one_dimen_params or self.raw_params
        result_params = copy(self.args)

        if self.prefix:
            params = self.__del_extra_dict_params(params=params)

        for elem in self._map:
            tmp = self.__search_element(
                element=self._map[elem],
                params=params
            )

            if tmp:
                result_params[elem] = tmp[1]

        result_params = {**result_params, **IPC_DEFAULT_ARGS, **self.kwargs}

        return result_params
