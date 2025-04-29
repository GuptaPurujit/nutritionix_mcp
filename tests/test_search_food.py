# tests/test_search_food.py
import pytest
import respx
from httpx import Response
from nutritionix_mcp.tools.search_food import search_food

@respx.mock
@pytest.mark.asyncio
async def test_search_food_combines_common_and_branded():
    mock_payload = {
        "common":  [{"food_name": "banana"}],
        "branded": [{"food_name": "Banana Smoothie"}]
    }
    respx.post("https://trackapi.nutritionix.com/v2/search/instant").mock(
        return_value=Response(200, json=mock_payload)
    )

    out = await search_food("ban")
    assert "banana" in out
    assert "Banana Smoothie" in out
