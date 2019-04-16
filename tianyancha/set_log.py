from datetime import datetime
from urllib.parse import quote
import hmac, json
from hashlib import sha1
import requests
import logging
import redis

def compute_signature(token: str, url: str, data: str = None) -> str:
    """
    Computes the signature for eve request.

    :param token: the token for the user to fire the request, which is usually obtained from redis
    :param url: the url of the request
    :param data: the request body in json format
    :return: the computed signature
    """
    token = token.encode('utf-8')
    url = quote(url, safe='?/=%:$').encode('utf-8')
    if isinstance(data, str):
        data = data.encode('utf-8')
    middle = hmac.new(token, url, sha1).hexdigest()
    if isinstance(middle, str):
        middle = middle.encode('utf-8')
    truth = hmac.new(middle, data, sha1).hexdigest()
    return truth


def create_logger(name):
    log = logging.getLogger(name)
    log.handlers = []
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.FileHandler(name))
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    log.addHandler(stream_handler)
    return log
