from typing import Dict, Set, List

from ...config import PARAMS_LOADING
from ..ipc.parameters.parameters import IPCParams

from .version_base import ResourceVersionBase
from .workflow_parameters import WorkFlowParam


class ResourceVersion(ResourceVersionBase):
    def get_params_streams(self):
        return self.params_streams

    @staticmethod
    def __get_ips_params(resource_slv_wf_name, vrs_source, dt_tgt):
        return IPCParams(
            wf_name=resource_slv_wf_name,
            resource_version=vrs_source,
            pref_data_load_dt=dt_tgt,
        )

    def __generate_stream_params(
            self,
            resource,
            vrs_source,
            max_vrs_tgt,
            dt_tgt
    ):
        """Get params from new WorkFlow"""
        ips_params = self.__get_ips_params(
            resource_slv_wf_name=resource['slv_wf_name'],
            vrs_source=vrs_source,
            dt_tgt=dt_tgt
        )

        wf_params = WorkFlowParam(
            resource=resource,
            vrs_source=vrs_source,
            ips_params=ips_params
        )

        if not self.params_ipc.get(resource['slv_wf_name'], None):
            self.params_ipc[resource['slv_wf_name']] = wf_params.get_wf_params(
                max_vrs_tgt, self.param_file_create
            )
        return self.params_ipc[resource['slv_wf_name']]

    def __set_params_streams(
            self,
            slv_wf_name: str,
            resource_index: int,
            resource: Dict,
            params: Dict
    ):
        if params:
            self.params_streams['workflows'][slv_wf_name]['resources'][resource_index] = resource
            self.params_streams['workflows'][slv_wf_name]['wf_params']['prepare_param'] = params
            print(self.params_streams, slv_wf_name)
        elif not params and PARAMS_LOADING != 'only_new':
            raise ValueError('The parameter list cannot be empty')

    @staticmethod
    def __get_all_slave(map_resources: List[Dict]) -> Set[str]:
        slv_wf_names = set()

        for elem in map_resources:
            slv_wf_names.add(elem['slv_wf_name'])

        return slv_wf_names

    def __create_struct_slw_wf(self, slv_wf_name: str):
        self.params_streams['workflows'][slv_wf_name] = dict()
        self.params_streams['workflows'][slv_wf_name]['resources'] = dict()
        self.params_streams['workflows'][slv_wf_name]['wf_params'] = dict()

    def check_map_resources(self):
        """Main method"""
        slv_wfs = self.__get_all_slave(map_resources=self.map_resources)

        for slv_wf in slv_wfs:
            self.__create_struct_slw_wf(slv_wf)

            cur_resources = list(
                filter(lambda elem: elem['slv_wf_name'] == slv_wf, self.map_resources)
            )
            for i, resource in enumerate(cur_resources):
                vrs_source, max_vrs_tgt, dt_tgt = self._get_resources_attribute(resource)

                params = self.__generate_stream_params(resource, vrs_source, max_vrs_tgt, dt_tgt)
                self.__set_params_streams(slv_wf, i, resource, params)
