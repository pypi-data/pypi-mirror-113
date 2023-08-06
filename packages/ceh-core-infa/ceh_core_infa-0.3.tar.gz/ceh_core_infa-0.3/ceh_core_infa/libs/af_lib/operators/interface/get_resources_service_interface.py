from .....libs.clients.ceh_resource_client import CehResourse
from .....libs.exceptions.exception import ResourceNotFound
from .base_interface import BaseInterface


class GetResourcesServiceInterface(BaseInterface):
    def __init__(self, table, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.table = table

    @staticmethod
    def __get_resources():
        return CehResourse.get_resources()

    @staticmethod
    def __check_resources_srv(table, resources):
        for resource in table:
            source = resource['src_resource_name']
            if source not in resources:
                raise ResourceNotFound(
                    f'Service {source} not found in CEH Resource Provider.'
                )

            target = resource['tgt_resource_name']
            if target not in resources:
                raise ResourceNotFound(
                    f'Service {target} not found in CEH Resource Provider.'
                )

    def execute(self):
        self.log.info(
            'Searching for resources in the CEH Resource Provider.'
        )

        resources = self.__get_resources()

        self.log.info(
            'The list of resources available'
            ' in the CEH Resource Provider is obtained'
        )

        executor = self.dynamic_executor(
            ex_func=self.__check_resources_srv,
            op_kwargs={'table': self.table, 'resources': resources},
            timer=self.timer
        )
        result = executor.executor()

        self.log.info('Successfully. All resources have been found.')

        return result
