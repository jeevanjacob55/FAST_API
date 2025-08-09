# app/utils/matching.py
import math
from typing import List, Tuple
import polyline as polyline_decoder
from shapely.geometry import LineString, Point # ✅ Import shapely

Coord = Tuple[float, float]  # (lat, lon)

def decode_polyline(poly: str) -> List[Coord]:
    """Decode Google encoded polyline to list of (lat, lon)."""
    try:
        return polyline_decoder.decode(poly)
    except:
        return []

def get_nearest_point_on_route(point: Coord, route_coords: List[Coord]) -> Tuple[int, float]:
    """
    Finds the index of the vertex on the route that is closest to a given point
    and calculates the accurate distance from the point to the route line itself.
    """
    if not route_coords:
        return -1, float('inf')

    # Create shapely objects for calculation
    passenger_point = Point(point)
    driver_route = LineString(route_coords)

    # 1. Calculate the accurate distance from the point to the line
    # Shapely's distance is in degrees, so we convert to km (1 degree lat ≈ 111 km)
    distance_in_degrees = passenger_point.distance(driver_route)
    distance_km = distance_in_degrees * 111

    # 2. Find the index of the closest vertex (for ordering pickup/dropoff)
    # This part remains the same as your original logic
    best_idx = -1
    min_vertex_dist = float('inf')
    for i, vertex in enumerate(route_coords):
        # Using simple distance formula for index finding is fast enough
        d = math.sqrt((point[0] - vertex[0])**2 + (point[1] - vertex[1])**2)
        if d < min_vertex_dist:
            min_vertex_dist = d
            best_idx = i
            
    return best_idx, distance_km


def route_matches(pass_start: Coord, pass_end: Coord, driver_polyline: str, tolerance_km: float = 5.0) -> bool:
    """
    Returns True if the driver's route passes near both start and end points
    AND the pickup occurs before the dropoff.
    """
    try:
        route_coords = decode_polyline(driver_polyline)
        if not route_coords:
            return False

        # Get the index and ACCURATE distance for start and end points
        start_idx, start_dist_km = get_nearest_point_on_route(pass_start, route_coords)
        end_idx, end_dist_km = get_nearest_point_on_route(pass_end, route_coords)

        print(f"DEBUG: start_dist={start_dist_km:.2f}km, end_dist={end_dist_km:.2f}km, start_idx={start_idx}, end_idx={end_idx}")

        # The final check: are both points close enough, and is the order correct?
        if start_dist_km <= tolerance_km and end_dist_km <= tolerance_km and start_idx < end_idx:
            return True
            
        return False
    except Exception as e:
        print(f"DEBUG: route_matches exception: {e}")
        return False