from urllib.parse import urlparse
import json
import msal


class FileCache(msal.TokenCache):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def load(self):
        self._cache = json.load(open(self.filename))

    def save(self):
        json.dump(self._cache, open(self.filename, 'w'))


def from_url(url):
    parts = urlparse(url)
    if parts.scheme == 'file':
        return FileCache(parts.path)
    raise ValueError('Unknown cache type %s')
