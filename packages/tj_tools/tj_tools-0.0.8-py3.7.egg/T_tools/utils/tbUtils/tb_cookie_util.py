from requests import get
from T_tools.host_util import HostUtil


def tb_cookie(uuid: str) -> str:
    return get(
        url=HostUtil.host_url() + 'API/cookie/?uuid=%s' % uuid + '&tp=tb'
    ).json().get("cookies")
