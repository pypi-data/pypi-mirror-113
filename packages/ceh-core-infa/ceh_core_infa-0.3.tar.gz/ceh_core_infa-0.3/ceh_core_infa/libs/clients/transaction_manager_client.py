from typing import List

from .base_client import BaseClient
from ..models.transaction import Transaction, TxCommitTimeout, TxToken, TxUrl, TxChangeCommitTimeout
from ..models.health import Health
from ...config import BASE_URL_TX_MANAGER, VERSION_TX_MANAGER

from yarl import URL


class TxManager(BaseClient):
    base_url = URL(BASE_URL_TX_MANAGER)

    @classmethod
    def get_transaction_list(cls) -> List[Transaction]:
        """ Get active transaction """
        transaction = cls()

        response = transaction._get(
            f'api/{VERSION_TX_MANAGER}/transactions'
        )
        return [Transaction(**i) for i in response]

    @classmethod
    def create_transaction(cls, timeout) -> Transaction:
        """ Create transaction with timeout"""
        transaction = cls()

        data = {'commit_timeout': timeout}
        json = TxCommitTimeout(**data).json()
        response = transaction._post(f'api/{VERSION_TX_MANAGER}/transactions', json=json)
        return Transaction(**response)

    @classmethod
    def get_transaction(cls, tx_uid ) -> Transaction:
        """ Get one transaction by tx_uid """
        transaction = cls()

        response = transaction._get(
            f'api/{VERSION_TX_MANAGER}/transactions/{tx_uid}'
        )
        return Transaction(**response)

    @classmethod
    def get_health_service(cls) -> Health:
        """ Get health api """
        transaction = cls()

        response = transaction._get('health')
        return Health(**response)

    @classmethod
    def change_transaction_timeout(cls, tx_uid, commit_timeout, tx_token) -> Transaction:
        """ Change transaction timeout """
        transaction = cls()

        data = {
            'tx_token': tx_token,
            'commit_timeout': commit_timeout,
        }
        json = TxChangeCommitTimeout(**data).json()
        response = transaction._put(f'api/{VERSION_TX_MANAGER}/transactions/{tx_uid}', json=json)
        return Transaction(**response)

    @classmethod
    def add_transaction_party(cls, tx_uid, url, tx_token) -> Transaction:
        """ Add transaction party """
        transaction = cls()

        data =  {
            'url': url,
            'tx_token': tx_token
        }
        json = TxUrl(**data).json()
        response = transaction._post(f'api/{VERSION_TX_MANAGER}/transactions/{tx_uid}/party', json=json)
        return Transaction(**response)

    @classmethod
    def commit_transaction(cls, tx_uid, tx_token) -> Transaction:
        """ Commit transaction """
        transaction = cls()

        data = {'tx_token': tx_token}
        json = TxToken(**data).json()
        response = transaction._post(f'api/{VERSION_TX_MANAGER}/transactions/{tx_uid}/commit', json=json)
        return response

    @classmethod
    def cancel_transaction(cls, tx_uid, tx_token) -> Transaction:
        """ Cancel transaction """
        transaction = cls()

        data = {'tx_token': tx_token}
        json = TxToken(**data).json()
        response = transaction._post(f'api/{VERSION_TX_MANAGER}/transactions/{tx_uid}/rollback', json=json)
        return response
