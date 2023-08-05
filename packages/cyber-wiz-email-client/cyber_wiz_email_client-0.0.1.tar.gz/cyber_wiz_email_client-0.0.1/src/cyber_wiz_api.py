import requests
import json
from urllib.parse import urljoin

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from exception import CyberWizEmailClientError


class EmailClient(object):
    _domain = 'https://mail.cyber-wiz.com/'
    # _domain = 'http://127.0.0.1:8000/'
    _status_forcelist = tuple(x for x in requests.status_codes._codes if x not in range(200, 300))

    _client_username = 'cyber_wiz_email_client'
    _client_password = 'email@client'
    _access_token = None
    _refresh_token = None
    _UN_AUTHORISED_REQUEST_STATUS_CODE = 401
    _token_auth_enabled = False

    def __init__(self):
        self._session = requests.Session()

    def _get_base_url(self):
        return self._domain

    def _get_api_token_url(self):
        return urljoin(self._get_base_url(), 'token/')

    def _get_url_for_token_refresh(self):
        return urljoin(self._get_base_url(), 'token/refresh')

    def _get_base_url_for_client(self):
        return urljoin(self._get_base_url(), 'es/')

    def _get_search_url(self):
        return urljoin(self._get_base_url_for_client(), 'search/')

    def _get_headers_dict(self):
        if not self._access_token:
            self._get_api_token()
        return {'Authorization': 'Bearer {}'.format(self._access_token),
                'content-type': 'application/json'}

    def _update_retry_logic(self, total_retries=1, backoff_factor=1):
        retries = Retry(total=total_retries, backoff_factor=backoff_factor, status_forcelist=self._status_forcelist,
                        raise_on_status=False)
        self._session.mount('http://', HTTPAdapter(max_retries=retries))
        self._session.mount('http://', HTTPAdapter(max_retries=retries))

    def _get_api_token(self):
        result = self._post(url=self._get_api_token_url(),
                            json={'username': self._client_username, 'password': self._client_password},
                            add_header_dict=False)
        self._access_token = result._get('access')
        self._refresh_token = result._get('refresh')

    def _update_api_token(self):
        params = {
            "url": self._get_url_for_token_refresh(),
            "json": {'refresh': self._refresh_token}
        }
        response = self._session.post(**params)
        if response.status_code == self._UN_AUTHORISED_REQUEST_STATUS_CODE:
            self._get_api_token()
        else:
            self._access_token = response.json()._get('access')

    def _post(self, url, json, total_retries=1, backoff_factor=1, **kwarg):
        self._update_retry_logic(total_retries, backoff_factor)
        params = {
            "url": url,
            "json": json
        }
        if self._token_auth_enabled:
            params["headers"] = self._get_headers_dict()
        response = self._session.post(**params)
        if not response.ok:
            if response.status_code == self._UN_AUTHORISED_REQUEST_STATUS_CODE:
                self._update_api_token()
                return self._post(url, json)
            else:
                raise CyberWizEmailClientError(url, response.status_code)
        return response.json()

    def _get(self, url, total_retries=3, backoff_factor=1, **kwargs):
        self._update_retry_logic()
        params = {
            "url": url,
            "params": kwargs
        }
        if self._token_auth_enabled:
            if not self._access_token:
                self._get_api_token()
            params["headers"] = self._get_headers_dict()
        response = self._session.get(**params)
        if not response.ok:
            if response.status_code == self._UN_AUTHORISED_REQUEST_STATUS_CODE:
                self._update_api_token()
                return self._get(url, **kwargs)
            else:
                raise CyberWizEmailClientError(url, response.status_code)
        return response.json()

    def get_generic_search_results(self, search_term, limit=None, total_retries=3, backoff_factor=1, **kwargs):
        return self._get(self._get_search_url(), total_retries=total_retries, backoff_factor=backoff_factor,
                         q_term=search_term, q_type='generic', limit=limit)

    def get_domain_search_results(self, search_term, limit=None, total_retries=3, backoff_factor=1, **kwargs):
        return self._get(self._get_search_url(), total_retries=total_retries, backoff_factor=backoff_factor,
                         q_term=search_term, q_type='domain_name', limit=limit)

    def get_user_name_search_results(self, search_term, limit=None, total_retries=3, backoff_factor=1, **kwargs):
        return self._get(self._get_search_url(), total_retries=total_retries, backoff_factor=backoff_factor,
                         q_term=search_term, q_type='user_name', limit=limit)
