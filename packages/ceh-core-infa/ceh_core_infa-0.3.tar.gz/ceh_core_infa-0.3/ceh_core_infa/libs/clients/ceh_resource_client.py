from typing import List

from requests.models import Response

from .base_client import BaseClient
from ..models.resource import Resource, ResourceResourceUpdate
from ..models.health import Health
from ..models.resource_state import ResourceState, ResourceStateUpdate
from ...config import BASE_URL_CEH_PROVIDER, VERSION_CEH_PROVIDER

from yarl import URL


class CehResourse(BaseClient):
    base_url = URL(BASE_URL_CEH_PROVIDER)

    @classmethod
    def get_resources(cls) -> List[Resource]:
        """ Get all resources """
        resource = cls()

        response = resource._get(
            f'api/{VERSION_CEH_PROVIDER}/resources'
        )
        return [Resource(**i) for i in response]

    @classmethod
    def create_resource(cls, data) -> Resource:
        """ Create Resource """
        resource = cls()

        json = ResourceResourceUpdate(**data).json()

        response = resource._post(
            f'api/{VERSION_CEH_PROVIDER}/resources', json=json
        )
        return Resource(**response)

    @classmethod
    def get_resourse(cls, resource_cd) -> Resource:
        """ Get one resource by resource_cd """
        resource = cls()

        response = resource._get(
            f'api/{VERSION_CEH_PROVIDER}/resources/{resource_cd}'
        )
        return Resource(**response)

    @classmethod
    def update_resource(cls, resource_cd, data) -> Resource:
        """ Update resource """
        resource = cls()

        json = ResourceResourceUpdate(**data).json()

        response = resource._put(
            f'api/{VERSION_CEH_PROVIDER}/resources/{resource_cd}', json=json
        )
        return Resource(**response)

    @classmethod
    def get_resource_state(cls, resource_cd) -> ResourceState:
        """ Get one resource state by resource_cd """
        resource = cls()

        response = resource._get(
            f'api/{VERSION_CEH_PROVIDER}/resources/{resource_cd}/state'
        )
        return ResourceState(**response)

    @classmethod
    def update_resource_state(cls, resource_cd, operation, tx_uid) -> ResourceState:
        """ Update resource state by resource_cd """
        resource = cls()

        json = ResourceStateUpdate(tx_uid=tx_uid, operation=operation).json()

        response = resource._put(
            f'api/{VERSION_CEH_PROVIDER}/resources/{resource_cd}/state', json=json
        )

        return ResourceState(**response)

    @classmethod
    def get_health_service(cls) -> Health:
        """ Get health api """
        resource = cls()

        response = resource._get('health')
        return Health(**response)
