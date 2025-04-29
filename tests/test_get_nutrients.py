# tests/test_get_nutrients.py
import pytest
import respx
from httpx import Response
from nutritionix_mcp.tools.get_nutrients import get_nutrients

@respx.mock
@pytest.mark.asyncio
async def test_get_nutrients_structured_and_picks_region():
    mock_resp = {
        "foods": [
            {
                "food_name": "banana",
                "serving_weight_grams": 118,
                "nf_calories": 105,
                "nf_protein": 1.3,
                "nf_total_fat": 0.4,
                "nf_total_carbohydrate": 27,
                "alt_measures": [
                    {"measure": "cup", "serving_weight": 225, "seq": 1},
                    {"measure": "oz",  "serving_weight": 28.35, "seq": 2}
                ]
            }
        ]
    }
    respx.post("https://trackapi.nutritionix.com/v2/natural/nutrients").mock(
        return_value=Response(200, json=mock_resp)
    )

    out_us = await get_nutrients("1 banana", region="US")
    assert out_us["calories"] == 105
    assert out_us["protein"]  == 1.3
    assert out_us["measure"]  == "oz"
    assert pytest.approx(out_us["serving_weight"], rel=1e-3) == 28.35

    out_in = await get_nutrients("1 banana", region="IN")
    # region IN prefers "ml", but since no "ml" entry, falls back to first
    assert out_in["measure"] in {"cup", "oz"}
