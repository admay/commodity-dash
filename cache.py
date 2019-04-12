class Cache():
    graph = {}
    table = {}

    def put(self, l, i, d):
        getattr(self, l)[i] = d
        pass

    def get(self, l, i):
        return getattr(self, l)[i]

    def check(self, l, i):
        return i in getattr(self, l)
