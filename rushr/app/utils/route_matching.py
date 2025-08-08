# app/utils/matching.py
import math
from typing import List, Tuple
import polyline as polyline_decoder

Coord = Tuple[float, float]  # (lat, lon)

def haversine_km(a: Coord, b: Coord) -> float:
    """Return distance in kilometers between two (lat, lon) points."""
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    R = 6371.0  # km
    h = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    return 2 * R * math.asin(math.sqrt(h))

def decode_polyline(poly: str) -> List[Coord]:
    """Decode Google encoded polyline to list of (lat, lon)."""
    return polyline_decoder.decode(poly)

def nearest_point_index(point: Coord, coords: List[Coord]) -> Tuple[int, float]:
    """Return (index_of_nearest_point, distance_km_to_nearest)."""
    best_idx = -1
    best_d = float("inf")
    for i, c in enumerate(coords):
        d = haversine_km(point, c)
        if d < best_d:
            best_d = d
            best_idx = i
    return best_idx, best_d

def route_matches(pass_start: Coord, pass_end: Coord, driver_polyline: str, tolerance_km: float = 2.0) -> bool:
    """
    Returns True if driver's route (polyline) passes near both pass_start and pass_end
    AND the pickup on the route occurs before the dropoff (start index < end index).
    """
    try:
        coords = decode_polyline(driver_polyline)
        if not coords:
            return False

        start_idx, start_dist = nearest_point_index(pass_start, coords)
        end_idx, end_dist = nearest_point_index(pass_end, coords)

        # Debug prints (remove or change to logging in production)
        print(f"DEBUG route_matches: start_dist={start_dist:.2f}km, end_dist={end_dist:.2f}km, start_idx={start_idx}, end_idx={end_idx}")

        if start_dist <= tolerance_km and end_dist <= tolerance_km and start_idx < end_idx:
            return True
        return False
    except Exception as e:
        print("DEBUG route_matches exception:", e)
        return False
