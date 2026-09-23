"""
BBMP Swachha Bengaluru - Vehicle GPS Telemetry Simulator
Simulates live movement of BBMP waste collection trucks across Bengaluru wards.
"""

import time
import math

class VehicleSimulator:
    def __init__(self, vehicle_no, start_lat, start_lng, route_name):
        self.vehicle_no = vehicle_no
        self.lat = start_lat
        self.lng = start_lng
        self.route_name = route_name
        self.step_index = 0

    def step_forward(self):
        """Simulates vehicle moving slightly along collection route."""
        # Simple step motion
        self.lat += 0.0003 * math.sin(self.step_index * 0.5)
        self.lng += 0.0003 * math.cos(self.step_index * 0.5)
        self.step_index += 1
        return {
            'vehicle_no': self.vehicle_no,
            'lat': round(self.lat, 4),
            'lng': round(self.lng, 4),
            'route': self.route_name,
            'status': 'collecting'
        }

if __name__ == "__main__":
    print("="*65)
    print("🚛 BBMP WASTE COLLECTION TRUCK SIMULATOR")
    print("="*65)
    sim = VehicleSimulator("KA-01-GA-4501", 12.9730, 77.6400, "Indiranagar 100ft Rd")
    for i in range(3):
        pos = sim.step_forward()
        print(f"Step {i+1}: Truck at ({pos['lat']}, {pos['lng']}) - Status: {pos['status']}")
