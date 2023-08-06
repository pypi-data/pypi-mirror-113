from datetime import datetime
from typing import Dict, List, Union, Set, Tuple
from abc import ABCMeta, abstractmethod

from ..models.resource_state import SourceDt, Source
from ..clients.ceh_resource_client import CehResourse
from ..exceptions.exception import (
    NotValidStatusCode,
    ResourceStateException
)


class ResourceVersionBase(metaclass=ABCMeta):
    """
    :param params_streams: параметры потока
    :type params_streams: Dict
    :param map_resources: связь источника к целевому ресурсу с техническими свойствами
    :type map_resources: List[Dict]
    :param param_file_create: флаг показывающий необходимость создания файла
    :type param_file_create: bool
    """

    def __init__(
            self,
            map_resources: List[Dict],
            param_file_create: bool = False
    ):
        self.params_streams: Dict = dict.fromkeys(['workflows'], dict())  # Параметры для запуска потоков в IPC
        self.map_resources: List = map_resources
        self.params_ipc: Dict = dict()
        self.param_file_create: bool = param_file_create

    @staticmethod
    def _get_resource_state(resource_name):
        """Get the state of the resource"""
        cur_res = CehResourse.get_resourse(resource_cd=resource_name)
        if cur_res.state:
            return CehResourse.get_resource_state(resource_cd=resource_name)
        return

    @staticmethod
    def _get_resource(resource_name):
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

        # Из target_state.version.operations выбирам список тех,
        # где указан наш src_resource_name
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
            max_vrs_operation = None
            # raise RuntimeError(f'There is no data for the resource {src_resource_name}, check the data')
        return max_vrs_operation

    def _get_tgt_info(self, target_state, src_resource_name):
        """Get info about target"""
        operation = self.__get_max_operations(target_state, src_resource_name)
        if operation:
            max_vrs_tgt = self.__get_version(operation)
            dt_tgt = self.__get_dt_operations(operation)
        else:
            max_vrs_tgt, dt_tgt = 0, datetime.now()

        return max_vrs_tgt, dt_tgt

    def _get_tgt_attribute(self, target_state, src_resource_name):
        """Get max_vrs_tgt, dt_tgt from target"""
        if target_state:
            max_vrs_tgt, dt_tgt = self._get_tgt_info(
                target_state, src_resource_name
            )
            dt_tgt = dt_tgt.strftime("%d.%m.%Y")
        else:
            max_vrs_tgt, dt_tgt = 0, datetime.now().strftime("%d.%m.%Y")
        return max_vrs_tgt, dt_tgt

    def _get_resources_attribute(self, resource):
        """Get attribute from resources"""
        source_state = self._get_resource_state(
            resource['src_resource_name']
        )  # Получаем состояние сурса

        if not source_state:
            raise ResourceStateException(
                'Source {} has no state.'.format(resource['src_resource_name'])
            )

        target_state = self._get_resource_state(
            resource['tgt_resource_name']
        )  # Получаем состояние таргета

        source = self._get_resource(resource['src_resource_name'])
        vrs_source = source.state.version.version_id

        max_vrs_tgt, dt_tgt = self._get_tgt_attribute(target_state, resource['src_resource_name'])

        return vrs_source, max_vrs_tgt, dt_tgt

    @abstractmethod
    def get_params_streams(self):
        raise NotImplementedError(
            'Define a execute in %s.' % self.__class__.__name__
        )

    @abstractmethod
    def check_map_resources(self):
        raise NotImplementedError(
            'Define a execute in %s.' % self.__class__.__name__
        )
