class Cache():
    data = {}

    def put(self, key, data):
        self.data[key] = data
        pass

    def delete(self, key):
        del self.data[key]
        pass

    def get(self, key):
        return self.data[key] if self.check(key) else {}

    def check(self, key):
        return True if key in self.data else False
