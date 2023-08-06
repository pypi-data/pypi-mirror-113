import json


class DBGood:
    def __init__(self):
        self.shop_name = None
        self.good_id = None
        self.title = None
        self.sku_id = None
        self.kucun = None
        self.extra_info = None
        self.type = None
        self.good_url =None
    def __str__(self):
        return str(self.__dict__)