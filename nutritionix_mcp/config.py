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

# Unit families
WEIGHT_UNITS = {"g", "gram", "grams", "kg", "kilogram", "kilograms", "oz", "ounce", "ounces", "lb", "pound", "pounds"}
VOLUME_UNITS = {"ml", "milliliter", "milliliters", "l", "liter", "liters",
                "tsp", "teaspoon", "teaspoons", "tbsp", "tablespoon", "tablespoons",
                "cup", "cups", "floz", "fluidounce", "fluidounces"}

# Locale→preferred family (used as fallback when input_unit is absent)
LOCALE_FAMILY_MAP = {
    "US": "volume",
    "IN": "volume",
    "EU": "weight",
    "UK": "weight",
}

# Densities (g per mL) for common ingredients for cross-family conversion
DENSITY_MAP = {
    "water": 1.0,
    "milk": 1.03,
    "olive oil": 0.91,
    # add more as needed
}
