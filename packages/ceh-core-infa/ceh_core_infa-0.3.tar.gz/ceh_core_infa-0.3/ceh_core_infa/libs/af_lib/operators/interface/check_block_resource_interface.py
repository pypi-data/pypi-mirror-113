from .base_interface import BaseInterface
from .....libs.exceptions.exception import ResourceBlockedException
from .....utils.utils import check_block


class CheckBlockResourceInterface(BaseInterface):
    def __init__(self, resources, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resources = resources

    @staticmethod
    def provide_info(resources, logger):

        for resource in resources:
            tgt = resource['tgt_resource_name']

            if check_block(tgt):
                raise ResourceBlockedException(f'The resource {tgt} is locked.')
            else:
                logger.info(f'The resource {tgt} is available.')

    def execute(self):
        self.log.info('Checking the required resources for blocking.')

        executor = self.dynamic_executor(
            ex_func=self.provide_info,
            op_kwargs={'resources': self.resources, 'logger': self.log},
            timer=self.timer
        )
        executor.executor()

        self.log.info('Successfully. All resources are free. Begin.')
