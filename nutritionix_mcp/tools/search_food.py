# nutritionix_mcp/tools/search_food.py
from typing import List
from nutritionix_mcp.main import mcp
from nutritionix_mcp.utils.http_client import http_client
from nutritionix_mcp.config import ENDPOINT_SEARCH_INSTANT

@mcp.tool(name="search_food")
async def search_food(query: str) -> List[str]:
    """
    Autocomplete food names via Nutritionix Instant Search.
    """
    payload = {"query": query}
    result = await http_client.post(ENDPOINT_SEARCH_INSTANT, payload)
    if not result:
        return []
    names = [f.get("food_name") for f in result.get("common", []) if f.get("food_name")]
    names += [f.get("food_name") for f in result.get("branded", []) if f.get("food_name")]
    return names
