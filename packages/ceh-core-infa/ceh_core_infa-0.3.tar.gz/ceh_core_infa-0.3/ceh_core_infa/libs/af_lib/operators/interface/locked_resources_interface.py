from .base_interface import BaseInterface
from .....libs.clients.ceh_resource_client import CehResourse
from .....libs.exceptions.exception import ResourceBlockedException
from .....utils.utils import check_block


class LockedGroupResourcesInterfaceOld(BaseInterface):
    def __init__(self, xcom_data, check_lock=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xcom_data = xcom_data
        self.cache = set()
        self.check_lock = check_lock

    @staticmethod
    def __check_lock_resource(resource_cd, logger):
        if check_block(resource_cd):
            raise ResourceBlockedException(
                f'The resource {resource_cd} is locked.'
            )
        else:
            logger.info(f'The resource {resource_cd} is available.')

    def _check_lock_resources(self, data):
        """Checking the blocking of all resources"""

        for _, elem in data.items():
            resource_cd = elem['tgt_resource_name']

            if not self._provide_cache(resource_cd=resource_cd):
                continue

            de = self.dynamic_executor(
                ex_func=self.__check_lock_resource,
                op_kwargs={
                    'resource_cd': resource_cd,
                    'logger': self.log
                },
                timer=self.timer
            )

            de.executor()

        self.cache.clear()

    @staticmethod
    def lock_resource(resource_cd, tx_uid, logger):
        logger.info(
            f'Opening a lock for a '
            f'resource {resource_cd} by transaction {tx_uid}'
        )
        operation = None

        CehResourse.update_resource_state(resource_cd, operation, tx_uid)

        logger.info(f'The resource {resource_cd} has been successfully locked')

    def _provide_cache(self, resource_cd):
        if resource_cd in self.cache:
            return False

        self.cache.add(resource_cd)
        return True

    def execute(self):
        data = self.xcom_data.value

        if self.check_lock:
            self._check_lock_resources(data=data)

        for _, elem in data.items():
            resource_cd = elem['tgt_resource_name']
            tx_uid = elem['tx_info']['tx_uid']

            if not self._provide_cache(resource_cd=resource_cd):
                continue

            se = self.static_executor(
                ex_func=self.lock_resource,
                op_kwargs={
                    'resource_cd': resource_cd,
                    'tx_uid': tx_uid,
                    'logger': self.log
                }
            )

            se.executor()


class LockedGroupResourcesInterface(BaseInterface):
    def __init__(self, resources, tx_info, check_lock=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resources = resources
        self.tx_info = tx_info
        self.cache = set()
        self.check_lock = check_lock

    @staticmethod
    def __check_lock_resource(resource_cd, logger):
        if check_block(resource_cd):
            raise ResourceBlockedException(
                f'The resource {resource_cd} is locked.'
            )
        else:
            logger.info(f'The resource {resource_cd} is available.')

    def _check_lock_resources(self, data):
        """Checking the blocking of all resources"""

        for _, elem in data.items():
            resource_cd = elem['tgt_resource_name']

            if not self._provide_cache(resource_cd=resource_cd):
                continue

            de = self.dynamic_executor(
                ex_func=self.__check_lock_resource,
                op_kwargs={
                    'resource_cd': resource_cd,
                    'logger': self.log
                },
                timer=self.timer
            )

            de.executor()

        self.cache.clear()

    @staticmethod
    def lock_resource(resource_cd, tx_uid, logger):
        logger.info(
            f'Opening a lock for a '
            f'resource {resource_cd} by transaction {tx_uid}'
        )
        operation = None

        CehResourse.update_resource_state(resource_cd, operation, tx_uid)

        logger.info(f'The resource {resource_cd} has been successfully locked')

    def _provide_cache(self, resource_cd):
        if resource_cd in self.cache:
            return False

        self.cache.add(resource_cd)
        return True

    def execute(self):
        if self.check_lock:
            self._check_lock_resources(data=self.resources)

        for _, elem in self.resources.items():
            resource_cd = elem['tgt_resource_name']
            tx_uid = self.tx_info['tx_uid']

            if not self._provide_cache(resource_cd=resource_cd):
                continue

            se = self.static_executor(
                ex_func=self.lock_resource,
                op_kwargs={
                    'resource_cd': resource_cd,
                    'tx_uid': tx_uid,
                    'logger': self.log
                }
            )

            se.executor()
