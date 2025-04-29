# nutritionix_mcp/utils/http_client.py
import httpx
from typing import Any, Dict, Optional
from nutritionix_mcp.config import API_BASE_URL, HEADERS

class HTTPClient:
    def __init__(self,
                 base_url: str    = API_BASE_URL,
                 headers: Dict[str, str] = HEADERS,
                 timeout: float   = 30.0):
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout
        )

    async def post(self,
                   path: str,
                   payload: Dict[str, Any],
                   retries: int = 3
    ) -> Optional[Dict[str, Any]]:
        for attempt in range(1, retries + 1):
            try:
                resp = await self._client.post(path, json=payload)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < retries:
                    continue
                return None
            except Exception:
                return None

    async def close(self):
        await self._client.aclose()

# singleton instance
http_client = HTTPClient()
