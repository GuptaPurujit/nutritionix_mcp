# nutritionix_mcp/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Nutritionix credentials (default to empty string)
NUTRITIONIX_APP_ID  = os.getenv("NUTRITIONIX_APP_ID", "")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY", "")

# Endpoints
API_BASE_URL               = "https://trackapi.nutritionix.com"
ENDPOINT_SEARCH_INSTANT    = "/v2/search/instant"
ENDPOINT_NATURAL_NUTRIENTS = "/v2/natural/nutrients"

# Shared headers
HEADERS = {
    "accept":           "application/json, text/plain, */*",
    "accept-encoding":  "gzip, deflate, br, zstd",
    "accept-language":  "en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "content-type":     "application/json",
    "user-agent":       "nutrition-app/1.0",
    "x-app-id":         NUTRITIONIX_APP_ID or "",
    "x-app-key":        NUTRITIONIX_API_KEY or "",
    "x-remote-user-id": "0",
}
