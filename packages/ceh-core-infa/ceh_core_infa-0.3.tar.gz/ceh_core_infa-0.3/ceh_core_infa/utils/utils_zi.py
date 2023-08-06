from ..libs.ipc.parameters.parameters import IPCParamsZI, LaunchParam
from ..config import PATH_CONFIG_FILES_IPC
from .utils import create_unique_folder


class GeneratorTestingParameters:
    __association = {
        'prepare': {
            'name_param': 'prepare_param',
            'wf_name': 'wf_prepare_name',
            'resource': 'src_version_id',
            'prefix_folder': 'Test_Workflow_Prepare',
            'file_param_template': 'ipc_pattern_prepare.PARAM'
        },
        'load': {
            'name_param': 'load_param',
            'wf_name': 'wf_load_name',
            'resource': 'tgt_version_id',
            'prefix_folder': 'Test_Workflow_Load',
            'file_param_template': 'ipc_pattern_load.PARAM'
        }
    }

    def __init__(self, raw_params, type_wf):
        self.raw_params = raw_params
        self.type_wf = type_wf

    def __get_necessary_parameters(self, name_param):
        param = self.raw_params.get(
            name_param, None
        )

        if not param:
            raise ValueError('Пожалуйста, передайте параметры в даг')

        return param

    @staticmethod
    def __create_folder(prefix):
        return create_unique_folder(
            prefix=prefix,
            domain=PATH_CONFIG_FILES_IPC
        )

    def __get_ipc_params(
            self,
            wf_name_main,
            wf_name,
            resource_version,
            pref_data_load_dt,
            params,
            folder,
            template_name
    ):
        ipc = IPCParamsZI(wf_name=wf_name,
                          resource_version=resource_version,
                          pref_data_load_dt=pref_data_load_dt,
                          params=params
                          )

        if self.type_wf == 'prepare':
            ipc_param = ipc.get_params_prepare()
        elif self.type_wf == 'load':
            ipc_param = ipc.get_params_load()
        else:
            raise ValueError('type_wf won\'t find')

        params['ipc_folder'] = folder
        params['ipc_param'] = ipc.add_conf_file(params=ipc_param,
                                                folder=folder,
                                                wf_name=wf_name_main,
                                                prefix='param_path',
                                                template_name=template_name)
        return params

    @staticmethod
    def __get_launch_param(param, wait):
        l_p = LaunchParam(
            raw_params=param,
            is_depth_search=True,
            not_case_dependency=True,
            wait=wait
        )
        return l_p.get_prarams()

    def __generate_ipc_params(self, param, sys_params):
        wf_name = param['slv_wf_name']
        wf_name_main = param[sys_params['wf_name']]
        resource_version = param[sys_params['resource']]
        pref_data_load_dt = param['prev_data_load_dt']

        folder = self.__create_folder(prefix=sys_params['prefix_folder'])

        param = self.__get_ipc_params(wf_name_main=wf_name_main,
                                      wf_name=wf_name,
                                      resource_version=resource_version,
                                      pref_data_load_dt=pref_data_load_dt,
                                      params=param,
                                      folder=folder,
                                      template_name=sys_params[
                                          'file_param_template',
                                      ]
                                      )

        return self.__get_launch_param(param=param, wait=wf_name_main)

    def generate_parameters(self):
        sys_params = self.__association.get(self.type_wf, None)

        if not sys_params:
            raise ValueError('Check the type_wf parameter')

        param = self.__get_necessary_parameters(
            name_param=sys_params['name_param']
        )

        result = self.__generate_ipc_params(param=param, sys_params=sys_params)

        return result
