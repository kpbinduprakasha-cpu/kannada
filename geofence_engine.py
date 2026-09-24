"""
BCC Swachha Belagavi - Geofencing Engine
Computes 5km Worker Alert Radius and 500m Household Waste Vehicle Proximity in Belagavi.
"""

import math

class GeofenceEngine:
    EARTH_RADIUS_KM = 6371.0

    @classmethod
    def haversine_distance_km(cls, lat1, lon1, lat2, lon2):
        """Calculates spherical distance between two points in km."""
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2.0) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return round(cls.EARTH_RADIUS_KM * c, 3)

    @classmethod
    def haversine_distance_meters(cls, lat1, lon1, lat2, lon2):
        """Calculates spherical distance in meters."""
        return round(cls.haversine_distance_km(lat1, lon1, lat2, lon2) * 1000.0, 1)

    @classmethod
    def is_within_radius(cls, lat1, lon1, lat2, lon2, radius_km):
        """Returns True if point 2 is within radius_km of point 1."""
        return cls.haversine_distance_km(lat1, lon1, lat2, lon2) <= radius_km

    @classmethod
    def find_nearby_workers(cls, incident_lat, incident_lng, active_workers, radius_km=5.0):
        """Finds all active on-duty workers within the specified radius (default 5km in Belagavi)."""
        nearby = []
        for worker in active_workers:
            w_lat = worker.get('lat') or worker.get('current_lat')
            w_lng = worker.get('lng') or worker.get('current_lng')
            if w_lat and w_lng:
                dist = cls.haversine_distance_km(incident_lat, incident_lng, w_lat, w_lng)
                if dist <= radius_km:
                    nearby.append({
                        'worker_id': worker.get('id') or worker.get('worker_id'),
                        'name': worker.get('name') or worker.get('worker_name'),
                        'emp_id': worker.get('worker_emp_id', 'BCC-W000'),
                        'distance_km': dist,
                        'distance_meters': round(dist * 1000.0, 1)
                    })
        return sorted(nearby, key=lambda x: x['distance_km'])

if __name__ == "__main__":
    print("="*65)
    print("📍 BELAGAVI GEOFENCE ENGINE TEST (5KM RADAR & 500M PROXIMITY)")
    print("="*65)
    # Tilakwadi 1st Gate to Congress Road in Belagavi
    d_m = GeofenceEngine.haversine_distance_meters(15.8340, 74.5020, 15.8345, 74.5015)
    print(f"Distance in Tilakwadi, Belagavi: {d_m} meters")
    print(f"Is within 500m vehicle alert zone? {d_m <= 500.0}")
