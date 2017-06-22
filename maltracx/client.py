import requests
from functools import wraps
from confutil import Config


CONFIG = Config('maltracx')


def _raise_status(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        response = func(*args, **kwargs)
        status = response.status_code
        if status // 100 == 2:
            try:
                return response.json()
            except:
                raise ValueError(response.text)
        else:
            raise ValueError(response.text)

    return decorated


class Client:

    def __init__(self, apikey_id=None, apikey_secret=None, root_url=None):
        apikey_id = apikey_id or CONFIG.get('APIKEY_ID')
        apikey_secret = apikey_secret or CONFIG.get('APIKEY_SECRET')
        self.auth = (apikey_id, apikey_secret)
        self.root_url = (
            root_url or
            CONFIG.get('ROOT_URL') or
            'https://maltra.cx'
        ).rstrip('/')

    def set_auth(self, apikey_id, apikey_secret):
        self.auth = (apikey_id, apikey_secret)

    def _url_to(self, path, api_root_path='/api', **kwargs):
        return '{}{}{}'.format(self.root_url, api_root_path, path)

    def get(self, path, params=None, data=None, **kwargs):
        url = self._url_to(path, **kwargs)
        response = requests.get(url, params=params or {}, json=data or {},
                                auth=self.auth)
        return response

    def post(self, path, params=None, data=None, **kwargs):
        url = self._url_to(path, **kwargs)
        response = requests.post(url, params=params or {}, json=data or {},
                                 auth=self.auth)
        return response

    def put(self, path, params=None, data=None, **kwargs):
        url = self._url_to(path, **kwargs)
        response = requests.put(url, params=params or {}, json=data or {},
                                auth=self.auth)
        return response

    def delete(self, path, params=None, data=None, **kwargs):
        url = self._url_to(path, **kwargs)
        response = requests.delete(url, params=params or {}, json=data or {},
                                   auth=self.auth)
        return response

    @_raise_status
    def create_apikey(self, username, password, expires_at=None):
        url = self._url_to('/user/create-apikey')
        response = requests.post(url, json={
            'username': username,
            'password': password,
            'expires_at': expires_at,
        })
        return response

    @_raise_status
    def get_news(self):
        return self.get('/news')

    @_raise_status
    def get_user(self):
        return self.get('/user')

    @_raise_status
    def get_report(self):
        return self.get('/report')

    @_raise_status
    def create_report(self, name, description=None, tlp='white'):
        data = {
            'name': name,
            'description': description,
            'tlp': tlp,
        }
        return self.put('/report', data=data)

    @_raise_status
    def get_url_monitor(self):
        return self.get('/monitor/url')

    @_raise_status
    def create_url_monitor(self, url, tlp='white'):
        data = {
            'url': url,
            'tlp': tlp,
        }
        return self.put('/monitor/url', data=data)
