# nutritionix_mcp/tools/get_nutrients.py
import re
from fractions import Fraction
from typing import Any, Dict, Optional
from nutritionix_mcp.main import mcp
from nutritionix_mcp.utils.http_client import http_client
from nutritionix_mcp.config import ENDPOINT_NATURAL_NUTRIENTS
from nutritionix_mcp.utils.units import parse_fraction, pick_alt_measure

# Matches leading “1 1/2 cup” or “3/4oz” style inputs
_QTY_UNIT_RE = re.compile(
    r'^(?P<qty>\d+(?:\s+\d+/\d+)?)(?:\s*(?P<unit>\w+))?\s+(?P<food>.+)$'
)

@mcp.tool(name="get_nutrients")
async def get_nutrients(
    query: str,
    region: str = "US"
) -> Optional[Dict[str, Any]]:
    # 1. parse quantity, unit, and food description
    qty = 1.0
    input_unit = ""
    food_desc = query
    m = _QTY_UNIT_RE.match(query.strip())
    if m:
        qty = parse_fraction(m.group("qty"))
        input_unit = m.group("unit") or ""
        food_desc = m.group("food")

    # 2. fetch base data
    payload = {"query": f"{qty} {input_unit} {food_desc}".strip()}
    result = await http_client.post(ENDPOINT_NATURAL_NUTRIENTS, payload)
    if not result:
        return None

    food = result["foods"][0]
    base_wt = food.get("serving_weight_grams", 1.0)
    # 3. compute per-gram densities
    cal_per_g = food.get("nf_calories", 0.0) / base_wt
    pro_per_g = food.get("nf_protein", 0.0)   / base_wt
    fat_per_g = food.get("nf_total_fat", 0.0)  / base_wt
    carb_per_g= food.get("nf_total_carbohydrate", 0.0) / base_wt

    # 4. select alt measure
    alt_list = food.get("alt_measures", [])
    chosen = pick_alt_measure(
        alt_list,
        locale=region,
        input_unit=input_unit,
        ingredient=food_desc
    )
    alt_wt = chosen.get("serving_weight", base_wt)

    # 5. scale to user quantity
    total_cal = cal_per_g  * alt_wt * qty
    total_pro = pro_per_g  * alt_wt * qty
    total_fat = fat_per_g  * alt_wt * qty
    total_car = carb_per_g * alt_wt * qty

    return {
        "food":           food_desc,
        "quantity":       qty,
        "measure":        chosen.get("measure"),
        "serving_weight": alt_wt,
        "calories":       round(total_cal, 2),
        "protein":        round(total_pro, 2),
        "fat":            round(total_fat, 2),
        "carbs":          round(total_car, 2),
        "alt_measures":   alt_list
    }
