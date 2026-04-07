class MCPServer:
 def __init__(self): self.tools={}
 def register_tool(self,n,t): self.tools[n]=t
 def call_tool(self,n,a,p): return self.tools[n].execute(a,p)