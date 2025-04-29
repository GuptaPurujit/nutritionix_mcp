# nutritionix_mcp/main.py
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("nutrition-server")

# Import tools so they register themselves with `mcp`
from nutritionix_mcp.tools.search_food    import search_food    # noqa: F401
from nutritionix_mcp.tools.get_nutrients  import get_nutrients  # noqa: F401
