import json

import requests
import urllib3

from T_tools.utils.tbUtils.tb_cookie_util import tb_cookie

urllib3.disable_warnings()


def get_data(id, uuid):
    headers = {
        'accept':          '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'Cookie':          tb_cookie(uuid),
        'referer':         'https://uland.taobao.com/semm/tbsearch?refpid=mm_26632258_3504122_32554087&keyword=%E5%A5%B3%E8'
                           '%A3%85 '
                           '&rewriteQuery=1&a=mi={imei}&sms=baidu&idfa={'
                           'idfa}&clk1=abab6283306413775910d4b0b37ca047&upsid=abab6283306413775910d4b0b37ca047',
        'user-agent':      'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/%s Mobile Safari/537.36',
    }
    session = requests.Session()
    url = r'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t=1535083295045' \
          r'&sign=ef22a6dc765bd6ce86d36e2ba9a6cc33&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017' \
          r'%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=%7B%22itemNumId%22%3A%22' + str(
        id) + r'%22%7D '
    r = session.get(url=url, headers=headers, verify=False)
    html = r.text
    start = html.find('(')
    datas = (json.loads(html[start + 1:-1]))['data']
    return datas
