import requests
import ssl

from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager


class HTTPtimeoutAdapter(HTTPAdapter):
    """ Adds timeout to requests HTTP adapter """

    def __init__(self, timeout: int = 5, max_retries: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs, max_retries=max_retries)
        self.timeout = timeout

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        """Initializes a urllib3 PoolManager.

        This method should not be called from user code, and is only
        exposed for use when subclassing the
        :class:`HTTPAdapter <requests.adapters.HTTPAdapter>`.

        :param connections: The number of urllib3 connection pools to cache.
        :param maxsize: The maximum number of connections to save in the pool.
        :param block: Block when no free connections are available.
        :param pool_kwargs: Extra keyword arguments used to initialize the Pool Manager.
        """
        # save these values for pickling
        self._pool_connections = connections
        self._pool_maxsize = maxsize
        self._pool_block = block

        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize,
                                       block=block, strict=True, ssl_version=ssl.PROTOCOL_TLSv1_2,
                                       **pool_kwargs)

    def send(self, *args, **kwargs):
        if kwargs.get('timeout') is None:
            kwargs['timeout'] = self.timeout
        return super(HTTPtimeoutAdapter, self).send(*args, **kwargs)


class SunshineBase:
    _OBJECTS_ROOT = 'api/sunshine/objects'

    _RELATIONSHIPS_ROOT = 'api/sunshine/relationships'

    _PROFILES_ROOT = 'api/v2/user_profiles'

    _EVENTS_ROOT = 'api/v2/user_profiles'

    _USERS_ROOT = 'api/v2/users'

    _HEADERS = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, subdomain: str, email: str, key: str, global_timeout: int = 5, max_retries: int = 0):
        """
        Creates and manages objects on zendesk sunshine

        :param subdomain: Your zendesk subdomain
        :param email: Sunshine user email ID. Used for token based authentication
        :param key: Sunshine token.
        :param global_timeout: Request timeout in seconds for every request within the session
        :param max_retries: The maximum number of retries each connection
            should attempt. Note, this applies only to failed DNS lookups, socket
            connections and connection timeouts, never to requests where data has
            made it to the server. By default, Requests does not retry failed
            connections. If you need granular control over the conditions under
            which we retry a request, import urllib3's ``Retry`` class and pass
            that instead.
        """

        self.subdomain = subdomain
        self._objects_base_url = f'https://{self.subdomain}.zendesk.com/{self._OBJECTS_ROOT}'
        self._relationships_base_url = f'https://{self.subdomain}.zendesk.com/{self._RELATIONSHIPS_ROOT}'
        self._profiles_base_url = f'https://{self.subdomain}.zendesk.com/{self._PROFILES_ROOT}'
        self._events_base_url = f'https://{self.subdomain}.zendesk.com/{self._EVENTS_ROOT}'
        self._users_base_url = f'https://{self.subdomain}.zendesk.com/{self._USERS_ROOT}'

        self._session = requests.Session()

        self._adapter = HTTPtimeoutAdapter(global_timeout, max_retries=max_retries)
        self._session.mount('http://', self._adapter)
        self._session.mount('https://', self._adapter)

        self._session.headers.update(self._HEADERS)

        self._session.auth = (f'{email}/token', f'{key}')

    def __repr__(self):
        return f'{self.__class__.__name__}(subdomain="{self.subdomain}")'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def close_session(self):
        """ Closes requests session """

        self._session.close()
