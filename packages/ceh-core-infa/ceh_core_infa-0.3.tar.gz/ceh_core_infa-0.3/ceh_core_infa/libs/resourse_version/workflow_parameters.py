from typing import Dict

from ...config import PARAMS_LOADING, PATH_CONFIG_FILES_IPC, WF_NAME_PRP
from ..ipc.parameters.parameters import IPCParams
from ..exceptions.exception import SomeVersionException

from ...utils.utils import create_unique_folder


class WorkFlowParam:
    """
    :param resource: параметры потока
    :type resource: Dict
    :param vrs_source: версия текущего источника
    :type vrs_source: str
    :param ips_params: параметры информатики
    :type ips_params: IPCParams спецаиальный класс
        с атрибутами необходимыми для потоков информатики
    """

    def __init__(
            self,
            resource: Dict,
            vrs_source: str,
            ips_params: IPCParams
    ):
        self.resource = resource
        self.vrs_source = vrs_source
        self.ips_params = ips_params

    @staticmethod
    def _add_ips_params_conf_file(
            ips_params,
            params: Dict,
            folder_ipc_params: str
    ):
        return ips_params.add_conf_file(
            params=params,
            wf_name=WF_NAME_PRP,
            folder=folder_ipc_params,
            template_name='ipc_pattern_prepare.PARAM',
            prefix='param_path'
        )

    @staticmethod
    def _check_params_loading():
        params_loading = ('all', 'wait_all', 'only_new')
        if PARAMS_LOADING in params_loading:
            return True
        else:
            return False

    def __provide_params_wf(
            self,
            max_vrs_tgt: int,
            param_file_create: bool,
            folder_ipc_params: str = None

    ) -> dict:
        """Generate WF params from ips_params"""
        params = dict()

        if max_vrs_tgt == self.vrs_source:
            if PARAMS_LOADING == 'only_new':
                params['folder'] = folder_ipc_params
                return params

            if PARAMS_LOADING == 'wait_all':
                raise SomeVersionException(
                    'The selected parameter {} source {} and target {} resource have the same version.'.format(
                        PARAMS_LOADING,
                        self.resource['src_resource_name'],
                        self.resource['tgt_resource_name']
                    )
                )

        if self._check_params_loading():
            params = self.ips_params.get_params_prepare()

            if param_file_create:
                params = self._add_ips_params_conf_file(
                    self.ips_params,
                    params,
                    folder_ipc_params
                )

        params['folder'] = folder_ipc_params
        return params

    def get_wf_params(self, max_vrs_tgt: int, param_file_create: bool = False) -> Dict:
        """Main method - return WF params"""
        if param_file_create:
            folder_ipc_params = create_unique_folder(
                prefix='Workflow',
                domain=PATH_CONFIG_FILES_IPC
            )
        else:
            folder_ipc_params = None

        params = self.__provide_params_wf(
            max_vrs_tgt=max_vrs_tgt,
            param_file_create=param_file_create,
            folder_ipc_params=folder_ipc_params
        )
        return params
