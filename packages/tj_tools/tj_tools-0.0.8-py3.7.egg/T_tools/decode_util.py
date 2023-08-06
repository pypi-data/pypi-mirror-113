import re

from T_tools import JOIN_STR
from T_tools.trans_util import base64_decode, md5


def decode_val(html: str, key: str) -> str:
    return base64_decode(re.search(
        r"%s" % (md5(key) + JOIN_STR + "(.*?)" + JOIN_STR),
        html).group(1))
