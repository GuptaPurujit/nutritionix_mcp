# nutritionix_mcp/tools/search_food.py
from typing import List
from nutritionix_mcp.main import mcp
from nutritionix_mcp.utils.http_client import http_client
from nutritionix_mcp.config import ENDPOINT_SEARCH_INSTANT

@mcp.tool(name="search_food")
async def search_food(query: str) -> List[str]:
    """Search for food items in the Nutritionix database.

    This MCP tool queries the Nutritionix API's instant search endpoint to find matching food items
    for a given search term. It returns a list of standardized food names from both common and
    branded food databases.

    Args:
        query (str): Search term to look up food items (e.g. "banana", "chicken breast")

    Returns:
        List[str]: List of matching food names. Returns empty list if no matches found or if
                    the API request fails.
    """
    payload = {"query": query}
    result = await http_client.post(ENDPOINT_SEARCH_INSTANT, payload)
    if not result:
        return []
    names = [f.get("food_name") for f in result.get("common", []) if f.get("food_name")]
    names += [f.get("food_name") for f in result.get("branded", []) if f.get("food_name")]
    return names
