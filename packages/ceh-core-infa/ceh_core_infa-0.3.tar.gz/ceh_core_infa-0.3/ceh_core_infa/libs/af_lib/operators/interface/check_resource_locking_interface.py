from .base_interface import BaseInterface
from .....libs.exceptions.exception import ResourceLockedException
from .....libs.clients.ceh_resource_client import CehResourse


class CheckResourceLockingInterfaceOld(BaseInterface):
    def __init__(self, xcom_params, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xcom_params = xcom_params

    @staticmethod
    def __check_if_locked(resource_cd):
        cur_res = CehResourse.get_resourse(resource_cd=resource_cd)
        if not cur_res.state:
            return True

        cur_locked = CehResourse.get_resource_state(
            resource_cd=resource_cd
        ).is_locked

        if cur_locked:
            raise ResourceLockedException(
                f'The resource {resource_cd} is locked.'
            )

        return cur_locked

    def execute(self):
        params = self.xcom_params.value.items()
        cache = set()

        for i, elem in params:
            resource_cd = elem['tgt_resource_name']

            if resource_cd in cache:
                continue
            else:
                cache.add(resource_cd)

            self.log.info(f'Checking if {resource_cd} is locked')

            de = self.dynamic_executor(
                ex_func=self.__check_if_locked,
                op_kwargs={'resource_cd': resource_cd, },
                timer=self.timer
            )

            de.executor()

            self.log.info(
                f'The check is over. The resource {resource_cd} is free.'
            )


class CheckResourceLockingInterface(BaseInterface):
    def __init__(self, resources, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resources = resources

    @staticmethod
    def __check_if_locked(resource_cd):
        cur_res = CehResourse.get_resourse(resource_cd=resource_cd)
        if not cur_res.state:
            return True

        cur_locked = CehResourse.get_resource_state(
            resource_cd=resource_cd
        ).is_locked

        if cur_locked:
            raise ResourceLockedException(
                f'The resource {resource_cd} is locked.'
            )

        return cur_locked

    def execute(self):
        params = self.resources.items()
        cache = set()

        for i, elem in params:
            resource_cd = elem['tgt_resource_name']

            if resource_cd in cache:
                continue
            else:
                cache.add(resource_cd)

            self.log.info(f'Checking if {resource_cd} is locked')

            de = self.dynamic_executor(
                ex_func=self.__check_if_locked,
                op_kwargs={'resource_cd': resource_cd, },
                timer=self.timer
            )

            de.executor()

            self.log.info(
                f'The check is over. The resource {resource_cd} is free.'
            )
