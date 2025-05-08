# nutritionix_mcp/tools/get_nutrients.py
from typing import Any, Dict, Optional
from nutritionix_mcp.main import mcp
from nutritionix_mcp.utils.http_client import http_client
from nutritionix_mcp.config import ENDPOINT_NATURAL_NUTRIENTS

@mcp.tool(name="get_nutrient_summary")
async def get_nutrient_summary(
    query: str
) -> Optional[Dict[str, Any]]:
    """Get a summary of nutritional information for a food item.

    This MCP tool queries the Nutritionix API to fetch basic serving and measurement information
    for a given food query. It returns key details about the food item including serving size,
    weight, and available alternate measurement units.

    Args:
        query (str): Natural language description of the food item (e.g. "1 large banana")

    Returns:
        Optional[Dict[str, Any]]: Dictionary containing:
            - food (str): Standardized food name
            - serving_quantity (float): Default serving quantity
            - serving_unit (str): Default serving unit
            - serving_weight_grams (float): Wealight in grams for default serving
            - calorie (float): Calorie Content of the food item
            - alt_measures (List[str]): Available alternate measurement units to be used to check
                                        if the user query fits the other measure better
            
        Returns "Could not Fetch Food Item Information" if the API request fails.
    """
    payload = {"query": query.lower()}
    result = await http_client.post(ENDPOINT_NATURAL_NUTRIENTS, payload)
    if not result:
        return "Could not Fetch Food Item Information"

    food = result["foods"][0]
    
    alt_list = []
    for measures in food["alt_measures"]:
        alt_list.append(measures["measure"])
    
    return {
        "food":                 food["food_name"],
        "serving_quantity":     food["serving_qty"],
        "serving_unit":         food["serving_unit"],
        "serving_weight_grams": food["serving_weight_grams"],
        "calories"            : food["nf_calories"],
        "alt_measures":         alt_list
    }
