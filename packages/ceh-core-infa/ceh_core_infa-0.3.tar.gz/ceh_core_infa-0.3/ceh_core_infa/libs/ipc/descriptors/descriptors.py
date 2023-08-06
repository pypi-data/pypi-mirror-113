import os


class ValidatePathIPCClient:
    """A descriptor for validating path to IPC client"""

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not value:
            raise ValueError(
                'Fill in the file path in the config file (config.py)'
            )

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class ValidateIPCParam:
    """A descriptor for validating IPC params"""

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not value:
            raise ValueError(
                'Fill in the config username/password '
                '(core_config.yml or config.py)'
            )

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class ValidatePathParams:
    """A descriptor for checking the file in the specified folder"""

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value is not None:
            if not os.path.exists(value):
                raise ValueError(
                    f'There is no such file at the specified path {value}'
                )

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
