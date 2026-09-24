"""
BCC Swachha Belagavi - System Configuration
Central parameters for Belagavi City Corporation (BCC - ಬೆಳಗಾವಿ ಮಹಾನಗರ ಪಾಲಿಕೆ),
Geofencing, Dynamic Worker Attribution, 10-Minute SLA, and Blockchain Rewards.
"""

# Municipal Ward Configurations (Belagavi City Corporation)
BELAGAVI_CENTER_LAT = 15.8497
BELAGAVI_CENTER_LNG = 74.4977

# Prominent Belagavi Wards & Coordinates
BELAGAVI_WARDS = {
    'Ward 21 - Tilakwadi': {'lat': 15.8340, 'lng': 74.5020},
    'Ward 12 - Rani Channamma Circle': {'lat': 15.8530, 'lng': 74.5100},
    'Ward 34 - Shahapur': {'lat': 15.8380, 'lng': 74.5180},
    'Ward 18 - Hindwadi': {'lat': 15.8420, 'lng': 74.4980},
    'Ward 45 - Vadgaon': {'lat': 15.8240, 'lng': 74.5150},
    'Ward 28 - Khasbag': {'lat': 15.8360, 'lng': 74.5240}
}

# Geofence Tolerances
VEHICLE_ALERT_RADIUS_METERS = 500.0  # Alert citizen when truck is < 500m away
WORKER_DISPATCH_RADIUS_KM = 5.0     # Alert workers within 5km radius
CLEANUP_GPS_TOLERANCE_METERS = 50.0 # Worker must be within 50m of dumped spot

# SLA Timers
WORKER_SLA_MINUTES = 10.0           # 10-minute SLA countdown before escalation

# Sanitation Worker Exclusive Monthly Reward Milestones (Workers Only - Not Citizens)
WORKER_MONTHLY_CLEANUP_TARGET = 500   # 500 verified cleanups in calendar month by worker
WORKER_MILESTONE_REWARD_INR = 4000.0  # ₹4,000 extra cash bonus exclusively for workers
MONTHLY_CLEANUP_TARGET = 500          # Legacy alias
MILESTONE_REWARD_INR = 4000.0         # Legacy alias

# Blockchain Genesis Seed
GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"
