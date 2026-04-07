
class SessionStore:
    def __init__(self):
        self.state = {}
    def set(self, k,v): self.state[k]=v
    def get(self,k): return self.state.get(k)
    def clear(self): self.state={}
