from . import JOIN_STR
from T_tools.trans_util import md5, base64_encode


def encode(key: str, val: str):
    return md5(key) + JOIN_STR + base64_encode(val) + JOIN_STR
