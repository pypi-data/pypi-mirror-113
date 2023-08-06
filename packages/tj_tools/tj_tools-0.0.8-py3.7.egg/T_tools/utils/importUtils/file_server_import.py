import sys
import importlib
import urllib.request as urllib2


class UrlMetaFinder(importlib.abc.MetaPathFinder):
    def __init__(self, baseurl):
        self._baseurl = baseurl

    def find_module(self, fullname, path=None):
        if path is None:
            baseurl = self._baseurl
        else:
            if isinstance(path, list):
                return None
            # 不是原定义的url就直接返回不存在
            if not path.startswith(self._baseurl):
                return None
            baseurl = path

        try:
            loader = UrlMetaLoader(baseurl)
            return loader
        except Exception:
            return None


class UrlMetaLoader(importlib.abc.SourceLoader):
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get_code(self, fullname):
        try:
            f = urllib2.urlopen(self.get_filename(fullname))
            return f.read()
        except Exception as e:
            raise ImportError("No Package")

    def get_data(self):
        pass

    def get_filename(self, fullname):
        return self.baseurl + fullname + '.py'


def install_meta(address):
    finder = UrlMetaFinder(address)
    sys.meta_path.append(finder)
