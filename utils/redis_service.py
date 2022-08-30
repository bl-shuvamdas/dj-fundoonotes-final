import json

import redis.exceptions
from django.conf import settings
from redis import Redis


class Cache:
    __cache = Redis(**settings.REDIS_CONFIG)
    __name = 'fundoo_note_{}'

    @classmethod
    def save(cls, name: int, payload: dict) -> None:
        """
        Redis hashmap set method(hset())

        :param name: keyword for redis server
        :param payload: data, which will get saved
        :return: None
        """
        cls.__cache.hset(name=cls.__name.format(name), key=payload['id'], value=json.dumps(payload))

    @classmethod
    def get_all(cls, name: int) -> list[dict]:
        """
        Redis hashmap get all method(hgetall())

        :param name: keyword for redis server
        :return: list of existing note
        """
        payload = cls.__cache.hgetall(name=cls.__name.format(name))
        return list(map(lambda x: json.loads(x), payload.values()))

    @classmethod
    def get(cls, name: int, key: int):
        """
        Redis hashmap get method(hget())

        :param name: keyword for redis server
        :param key: key for look into the value hashmap
        :return: Union[dict[str, str], None]
        """
        payload = cls.__cache.hget(name=cls.__name.format(name), key=key)
        return json.loads(payload) if payload else {}

    @classmethod
    def drop(cls, name: int, key: int) -> None:
        """
        Redis hashmap delete method(hdel())

        :param name: keyword for redis server
        :param key: key for look into the value hashmap
        :return: Union[dict[str, str], None]
        """
        cls.__cache.hdel(cls.__name.format(name), key)
