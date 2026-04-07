from mcp.server import MCPServer
from tools.db_tool import DBTool
_server=None
def setup_mcp():
 global _server
 if not _server:
  _server=MCPServer();_server.register_tool('db',DBTool())
 return _server