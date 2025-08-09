# app/utils/matching.py
import math
from typing import List, Tuple
import polyline as polyline_decoder
from shapely.geometry import LineString, Point

Coord = Tuple[float, float]

def decode_polyline(poly: str) -> List[Coord]:
    try:
        return polyline_decoder.decode(poly)
    except:
        return []

def get_nearest_point_on_route(point: Coord, route_coords: List[Coord]) -> Tuple[int, float]:
    if not route_coords:
        return -1, float('inf')

    passenger_point = Point(point)
    driver_route = LineString(route_coords)

    distance_in_degrees = passenger_point.distance(driver_route)
    distance_km = distance_in_degrees * 111

    best_idx = -1
    min_vertex_dist = float('inf')
    for i, vertex in enumerate(route_coords):
        d = math.sqrt((point[0] - vertex[0])**2 + (point[1] - vertex[1])**2)
        if d < min_vertex_dist:
            min_vertex_dist = d
            best_idx = i
            
    return best_idx, distance_km

def route_matches(pass_start: Coord, pass_end: Coord, driver_polyline: str, tolerance_km: float = 5.0) -> bool:
    print(f"DEBUG: [route_matches] --- Checking polyline: {driver_polyline[:40]}...")
    try:
        route_coords = decode_polyline(driver_polyline)
        if not route_coords:
            print("DEBUG: [route_matches] Polyline decoded to an empty list. Skipping.")
            return False

        start_idx, start_dist_km = get_nearest_point_on_route(pass_start, route_coords)
        end_idx, end_dist_km = get_nearest_point_on_route(pass_end, route_coords)

        print(f"DEBUG: [route_matches] Start Dist: {start_dist_km:.2f}km (Tolerance: {tolerance_km}), End Dist: {end_dist_km:.2f}km (Tolerance: {tolerance_km})")
        print(f"DEBUG: [route_matches] Start Index: {start_idx}, End Index: {end_idx}")

        is_match = start_dist_km <= tolerance_km and end_dist_km <= tolerance_km and start_idx < end_idx
        
        print(f"DEBUG: [route_matches] Final match decision: {is_match}")
        return is_match
        
    except Exception as e:
        print(f"!!! EXCEPTION in route_matches: {e}")
        return False