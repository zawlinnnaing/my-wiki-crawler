from requests import get
from requests import RequestException
from contextlib import closing
import os
import logging
from .file import FileUtil
from datetime import date
import json


os.chdir(os.getcwd())


def request_api(url, params):
    try:
        with closing(get(url, params=params)) as res:
            return res.json()
    except RequestException as e:
        raise e


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as res:
            if is_good_response(res):
                return res.content
            else:
                return None

    except RequestException as e:
        raise e


def is_good_response(res, content_type='html'):
    """
    Returns True if the response seems to be Content type (default html), False otherwise.
    """
    content_type = res.headers['Content-Type'].lower()
    return (res.status_code == 200 and content_type is not None and content_type.find(content_type) > -1)


def log_error(e: str, log_dir: str = 'logs'):
    FileUtil.mkdir_if_not_exists(log_dir)
    log_file = os.path.join(log_dir, str(date.today())+'.log')
    logging.basicConfig(filename=log_file, level=logging.WARNING)
    logging.error(e)
