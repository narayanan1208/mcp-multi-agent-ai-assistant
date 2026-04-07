class MCPClient:
 def __init__(self,s): self.server=s
 def call(self,t,a,p): return self.server.call_tool(t,a,p)