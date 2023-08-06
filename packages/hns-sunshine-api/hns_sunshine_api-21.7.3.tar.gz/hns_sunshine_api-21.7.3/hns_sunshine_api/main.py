"""
Zendesk sunshine API
API guide: https://developer.zendesk.com/rest_api/docs/sunshine/introduction
"""
from hns_sunshine_api.sunshine.object_records import SunshineObjectRecords
from hns_sunshine_api.sunshine.relationship_records import SunshineRelationshipRecords
from hns_sunshine_api.sunshine.profiles import SunshineProfiles
from hns_sunshine_api.sunshine.events import SunshineEvents
from hns_sunshine_api.sunshine.base import SunshineBase


class Sunshine(SunshineBase):

    def __init__(self, subdomain: str, email: str, key: str, global_timeout: int = 5, max_retries: int = 0):
        """
        Creates and manages objects on zendesk sunshine

        Instantiating creates a requests session. You can call `close` at the end.

        Usage:

        Simple use:

            sunshine = Sunshine(subdomain='mydomain', email='test@example.com', key='test_key')
            objects = sunshine.object_records().list(object_type='sometype')
            relation = sunshine.relationships_records().show(relationship_id='someid')
            sunshine.close_session()

        Using context manager:

            with Sunshine(subdomain='mydomain', email='test@example.com', key='test_key') as sunshine:
                objects = sunshine.object_records().list(object_type='sometype')
                relation = sunshine.relationships_records().show(relationship_id='someid')

        Zendesk API docs: https://developer.zendesk.com/rest_api/docs/sunshine/introduction

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

        super().__init__(subdomain, email, key, global_timeout, max_retries=max_retries)
        self._object_record = SunshineObjectRecords(
            subdomain=subdomain, email=email, key=key, global_timeout=global_timeout, max_retries=max_retries
        )
        self._relationship_record = SunshineRelationshipRecords(
            subdomain=subdomain, email=email, key=key, global_timeout=global_timeout, max_retries=max_retries
        )
        self._profiles = SunshineProfiles(
            subdomain=subdomain, email=email, key=key, global_timeout=global_timeout, max_retries=max_retries
        )
        self._events = SunshineEvents(
            subdomain=subdomain, email=email, key=key, global_timeout=global_timeout, max_retries=max_retries
        )

    def __repr__(self):
        return f'{self.__class__.__name__}(subdomain="{self.subdomain}")'

    def object_records(self):
        return self._object_record

    def relationships_records(self):
        return self._relationship_record

    def object_types(self):
        raise NotImplementedError

    def relationship_types(self):
        raise NotImplementedError

    def events(self):
        return self._events

    def profiles(self):
        return self._profiles

