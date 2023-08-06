from typing import List

from .base_client import BaseClient
from ..models.increment import Increment, CreateIncrement
from ..models.health import Health
from ...config import BASE_URL_SEQ_GENERATOR, VERSION_CEH_SEQ_GENERATOR

from yarl import URL


class Sequence(BaseClient):
    base_url = URL(BASE_URL_SEQ_GENERATOR)

    @classmethod
    def create_increment(cls, key, value) -> Increment:
        """ Create increment by key and value """
        resource = cls()

        data = {'increment': value}
        json = CreateIncrement(**data).json()
        response = resource._post(f'api/{VERSION_CEH_SEQ_GENERATOR}/sequences/{key}/incr', json=json)
        return Increment(**response)

    @classmethod
    def get_increment(cls, key) -> Increment:
        """ Get one increment by key """
        resource = cls()

        response = resource._get(f'api/{VERSION_CEH_SEQ_GENERATOR}/sequences/{key}')
        return Increment(**response)

    @classmethod
    def get_health_service(cls) -> Health:
        """ Get health api """
        resource = cls()

        response = resource._get('health')
        return Health(**response)
