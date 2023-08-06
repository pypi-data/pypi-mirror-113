from typing import Optional
from yarl import URL
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError

from requests import Session
from ..exceptions.exception import ConnectionApiError, NotValidStatusCode
# from ...config import AUTH_ENABLE, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, OAUTH_TOKEN_URL


class BaseClient:
    base_url = URL('')

    def _update_token(self) -> None:
        """ Get a new JWT token """
        pass
        # self.session.fetch_token(
        #     token_url=OAUTH_TOKEN_URL,
        #     client_id=OAUTH_CLIENT_ID,
        #     client_secret=OAUTH_CLIENT_SECRET
        # )

    def __get_session(self) -> None:
        """ Generate a new session """
        self.session = Session()
        # TODO: fix circular import
        # if AUTH_ENABLE:
        #     self.session = OAuth2Session(client=BackendApplicationClient(client_id=OAUTH_CLIENT_ID))
        #     self._update_token()
        # else:
        #     self.session = Session()

    def _make_url(self, endpoint: str) -> URL:
        """ Generate URL """
        return self.base_url / endpoint

    def _request(self,
                 method: str, 
                 endpoint: str,
                 params: dict = None, 
                 json: dict = None) -> Optional[dict]:
        """ Send a request """

        self.__get_session()

        url = self._make_url(endpoint)

        for i in range(2):
            try:
                response = self.session.request(method, url, params=params, data=json)
                break
            except TokenExpiredError:
                self._update_token()
                continue
            except:
                raise ConnectionApiError(f'Error connection to url {url}')

        if not response.ok:
            raise NotValidStatusCode(
                f'Invalid response status received. Status code: {response.status_code}. Text: {response.text}'
            )

        return response.json()

    def _get(self, endpoint: str, params: dict = None) -> Optional[dict]:
        """ GET request """
        return self._request('GET', endpoint, params=params)

    def _post(self, endpoint: str, json: dict = None) -> Optional[dict]:
        """ POST request """
        return self._request('POST', endpoint, json=json)

    def _put(self, endpoint: str, json: dict = None) -> Optional[dict]:
        """ PUT request """
        return self._request('PUT', endpoint, json=json)
