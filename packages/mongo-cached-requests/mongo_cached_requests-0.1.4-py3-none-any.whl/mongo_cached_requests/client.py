import pymongo
import requests
import datetime
import urllib.parse
from requests.models import Response
from typing import Any, Dict, Union
from pymongo import MongoClient
from pymongo.collection import Collection


class CachedRequestClient:
    __mongoClient: MongoClient
    __time_diff_allowance: datetime.timedelta
    __headers: Dict

    def __init__(self, mongo_client: MongoClient, time_diff_allowance=datetime.timedelta(days=1), headers=None):
        if headers is None:
            headers = dict()
        self.__mongoClient = mongo_client
        self.__time_diff_allowance = time_diff_allowance
        self.__headers = headers

    def get(self, url, params=None, no_cache=False):

        if no_cache:
            self.__get_from_http__(url, params)
            return

        params = {} if params is None else params

        collection = self.__get_collection_from_url__(url)

        now: datetime = datetime.datetime.utcnow()
        most_recent_match: Union[Dict, None] = collection.find_one(
            params, sort=[('time', pymongo.DESCENDING)]
        )

        if most_recent_match is not None:
            time_since_most_recent_request = now - most_recent_match['time']

            if time_since_most_recent_request > self.__time_diff_allowance:
                return self.__get_from_http__(url, params)
            else:
                return most_recent_match['response']

        else:
            return self.__get_from_http__(url, params)

    def __get_collection_from_url__(self, url) -> Collection:
        parsed_url = urllib.parse.urlsplit(url)
        return self.__mongoClient.get_database(parsed_url.hostname.replace('.', '-')).get_collection(parsed_url.path)

    def __get_from_http__(self, url, params=None, **kwargs):
        r: Response = requests.get(url, params, **kwargs, headers=self.__headers)
        doc = {**params, 'time': datetime.datetime.utcnow(), 'response': r.json()}
        collection = self.__get_collection_from_url__(url)
        collection.insert_one(doc)
        return r.json()
