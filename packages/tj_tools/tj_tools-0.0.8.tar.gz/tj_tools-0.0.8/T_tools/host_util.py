import requests

from T_tools.decode_util import decode_val
from . import CONFIG_HOST_KEY


class HostUtil:
    __host_url = None
    __text = None

    @classmethod
    def html_text(cls):
        if cls.__text:
            return cls.__text
        url = 'https://blog.csdn.net/jth1234567/article/details/118071178'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
        res = requests.get(url, headers=headers, timeout=3)
        res.encoding = res.apparent_encoding
        cls.__text = res.text
        return cls.__text

    @classmethod
    def host_url(cls):
        if cls.__host_url:
            return cls.__host_url
        html = cls.html_text()
        cls.__host_url = decode_val(html, CONFIG_HOST_KEY)
        return cls.__host_url
