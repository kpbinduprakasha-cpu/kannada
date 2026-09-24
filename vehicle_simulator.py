"""
BCC Swachha Belagavi - Vehicle GPS Telemetry Simulator
Simulates live movement of Belagavi City Corporation (BCC) waste collection trucks (KA-22).
"""

import math

class VehicleSimulator:
    def __init__(self, vehicle_no, start_lat, start_lng, route_name):
        self.vehicle_no = vehicle_no
        self.lat = start_lat
        self.lng = start_lng
        self.route_name = route_name
        self.step_index = 0

    def step_forward(self):
        """Simulates vehicle moving slightly along collection beat in Belagavi."""
        self.lat += 0.00025 * math.sin(self.step_index * 0.5)
        self.lng += 0.00025 * math.cos(self.step_index * 0.5)
        self.step_index += 1
        return {
            'vehicle_no': self.vehicle_no,
            'lat': round(self.lat, 4),
            'lng': round(self.lng, 4),
            'route': self.route_name,
            'city': 'Belagavi',
            'status': 'collecting'
        }

if __name__ == "__main__":
    print("="*65)
    print("🚛 BELAGAVI (BCC) WASTE COLLECTION TRUCK SIMULATOR")
    print("="*65)
    sim = VehicleSimulator("KA-22-G-1801", 15.8350, 74.5030, "Tilakwadi - Congress Road Beat")
    for i in range(3):
        pos = sim.step_forward()
        print(f"Step {i+1}: Truck at Belagavi ({pos['lat']}, {pos['lng']}) - Status: {pos['status']}")
