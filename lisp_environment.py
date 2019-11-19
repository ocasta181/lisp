class environment():
    
    def __init__(self, parent = None):
        self.parent = parent
        self.env = {}

    def insert(self, key, value):
        self.env[key] = value
    
    def find(self, key):
        if key in self.env:
            return self
        elif self.parent:
            return self.parent.find(key)
        else:
            return None
    
    def get(self, key):
        return self.env[key]