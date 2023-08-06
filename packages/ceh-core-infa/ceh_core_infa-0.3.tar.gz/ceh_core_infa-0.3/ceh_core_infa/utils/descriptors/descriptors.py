class ValidateAttempts:
    """Descriptor for validating the number of attempts"""

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value <= 0 or value > 100:
            raise ValueError(
                'The number must not be less than 0 or greater than 100'
            )
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class ValidateTimeout:
    """A descriptor for validating the timeout value"""

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value < 1 or value > 3600:
            raise ValueError(
                'The number must not be less than 0 or greater than 3600'
            )
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class IsIterable:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if instance.__dict__['error_if_locked']:
            if not value:
                raise ValueError('No resources to check')

            if isinstance(value, str) or not hasattr(value, '__iter__'):
                raise ValueError(
                    f'The object {self.name} must be iterable'
                )

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
