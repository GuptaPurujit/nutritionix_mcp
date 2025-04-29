# server.py

import os
import sys
from dotenv import load_dotenv

# ensure your package path is on PYTHONPATH so main.py can import nutritionix_mcp
sys.path.insert(0, os.path.dirname(__file__))

# load NUTRITIONIX_APP_ID, NUTRITIONIX_API_KEY, etc.
load_dotenv()

from nutritionix_mcp.main import mcp

if __name__ == "__main__":
    # Run the MCP server over stdio for local orchestrator to spawn
    mcp.run(transport="stdio")
