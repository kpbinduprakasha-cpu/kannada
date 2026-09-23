"""
BBMP Swachha Bengaluru - System Configuration
Central parameters for Municipal Geofencing, 10-Minute SLA, and Blockchain Rewards.
"""

# Municipal Ward Configurations (Bengaluru Central)
BENGALURU_CENTER_LAT = 12.9716
BENGALURU_CENTER_LNG = 77.5946

# Geofence Tolerances
VEHICLE_ALERT_RADIUS_METERS = 500.0  # Alert citizen when truck is < 500m away
WORKER_DISPATCH_RADIUS_KM = 5.0     # Alert workers within 5km radius
CLEANUP_GPS_TOLERANCE_METERS = 50.0 # Worker must be within 50m of dumped spot

# SLA Timers
WORKER_SLA_MINUTES = 10.0           # 10-minute SLA countdown before escalation

# Reward & Gamification Milestones
MONTHLY_CLEANUP_TARGET = 500        # 500 verified cleanups in calendar month
MILESTONE_REWARD_INR = 4000.0       # ₹4,000 extra cash reward

# Blockchain Genesis Seed
GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"
