# nutritionix_mcp/utils/units.py
from typing import List, Dict, Optional
from fractions import Fraction
from nutritionix_mcp.config import (
    WEIGHT_UNITS, VOLUME_UNITS,
    LOCALE_FAMILY_MAP, DENSITY_MAP
)

def parse_fraction(qty_str: str) -> float:
    """Convert a string like '1 1/2' or '3/4' into a float safely."""
    try:
        return float(Fraction(qty_str))
    except Exception:
        return 1.0

def is_weight_unit(u: str) -> bool:
    return u.lower() in WEIGHT_UNITS

def is_volume_unit(u: str) -> bool:
    return u.lower() in VOLUME_UNITS

def pick_alt_measure(
    alt_measures: List[Dict],
    locale: str,
    input_unit: Optional[str] = None,
    ingredient: Optional[str] = None
) -> Dict:
    """
    Choose the best alt_measure entry given:
      - input_unit hint (e.g. 'cup' vs 'g')
      - locale fallback (volume vs weight)
      - seq priority
    Falls back to cross-family using density if needed.
    """
    # 1. classify by family
    preferred_family = None
    if input_unit:
        if is_volume_unit(input_unit):
            preferred_family = "volume"
        elif is_weight_unit(input_unit):
            preferred_family = "weight"
    if not preferred_family:
        preferred_family = LOCALE_FAMILY_MAP.get(locale.upper(), "weight")

    # 2. filter by family
    family_matches = []
    for m in alt_measures:
        measure = m.get("measure", "").lower()
        if preferred_family == "volume" and measure in VOLUME_UNITS:
            family_matches.append(m)
        elif preferred_family == "weight" and measure in WEIGHT_UNITS:
            family_matches.append(m)

    # 3. choose lowest seq among matches
    if family_matches:
        return min(family_matches, key=lambda m: m.get("seq", 999))

    # 4. cross-family fallback via density if possible
    if preferred_family == "volume" and input_unit and is_volume_unit(input_unit) and ingredient:
        # e.g. convert vol → weight using density
        dens = DENSITY_MAP.get(ingredient.lower(), None)
        if dens:
            # find any weight entry to use its ratio
            for m in alt_measures:
                if m.get("measure", "").lower() in WEIGHT_UNITS:
                    return m
    # 5. last-resort fallback
    return alt_measures[0] if alt_measures else {"measure": "g", "serving_weight": 1.0, "seq": 1}
