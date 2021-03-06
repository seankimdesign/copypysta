# TODO: Persist through session via DB or filewriting
class CopyCache(object):

    @staticmethod
    def sanitize(value):
        try:
            return str(value)
        except ValueError:
            return ""

    def __init__(self):
        self.cache = []

    def shift(self, value):
        self.cache.insert(0, CopyCache.sanitize(value))
        self.cache = self.cache[:10]

    def retrieve(self, index):
        if index <= 9 and len(self.cache) > index:
            return self.cache[index]
        return ""

    def flush(self):
        self.cache = []

    def __len__(self):
        return len(self.cache)

    def __str__(self):
        return str(self.cache)
