import json

from T_tools.utils.tbUtils.model import DBGood
from T_tools.utils.tbUtils.req_util import get_data


class TBGood:

    @classmethod
    def get_goods(cls, uuid, good_id=None, good_url=None):
        if good_url:
            import re
            good_id = re.search(r"id=(\d+)", good_url).group(1)
        if good_id:
            data = get_data(good_id, uuid)
            return cls.tran_data_to_goods(data, good_id, good_url=good_url)
        return []

    @classmethod
    def tran_data_to_goods(self, data, good_id, good_url) -> list:
        shop_name = data.get('seller').get('shopName')
        title = data.get('item').get('title')
        d2 = json.loads(data.get('apiStack')[0].get('value'))
        skuid_kucun_map = {}
        skuid_logisticsTime = ""
        for skuid, val in d2.get('skuCore').get('sku2info').items():
            skuid_kucun_map[skuid] = val.get('quantity')
            if val.get('logisticsTime') is not None:
                skuid_logisticsTime = val.get('logisticsTime')
        # print(skuid_kucun_map)
        try:
            sku_prop_map = {}
            for item in data.get('skuBase').get('skus'):
                sku_prop_map[item.get('skuId')] = item.get('propPath')
            # print(sku_prop_map)
            prop_vid_map = {}
            for item in data.get('skuBase').get('props'):
                for val in item.get('values'):
                    prop_vid_map[
                        '%s:%s' % (item.get('pid'), val.get('vid'))] = val.get(
                        'name')
        except:
            print('%s  只有一条数据' %good_id)
        result = []
        for skuid in skuid_kucun_map:
            item = DBGood()
            item.good_url = good_url
            item.shop_name = shop_name
            item.good_id = good_id
            item.title = title
            item.sku_id = skuid
            item.kucun = skuid_kucun_map[skuid]
            item.extra_info = skuid_logisticsTime
            if skuid != "0":
                tt = sku_prop_map[skuid].split(';')
                item.type = ' '.join([prop_vid_map[t] for t in tt])
            result.append(item)
        return result
