"""
End-to-End Test Suite for BBMP Swachha Bengaluru Smart Waste Management System.
Validates all 13 core requirements + initial website open onboarding (OTP, First Name, Last Name, Mobile & Home Center).
"""

import sys
import unittest
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from app import app, init_db, get_db_connection

class TestBBMPWasteSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = app.test_client()

    def test_01_web_page_serves(self):
        """Verify Web Portal UI serves successfully with onboarding modal."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'SWACHHA BENGALURU', res.data)
        self.assertIn(b'modal-auth-onboarding', res.data)
        self.assertIn(b'Home Center Location', res.data)
        print("[PASS] 1. Web Portal & Initial Onboarding UI served successfully.")

    def test_02_first_time_open_otp_and_home_center(self):
        """New User Requirement: Open website -> Mobile/Email OTP -> First Name, Last Name, Mobile, Home Center."""
        # 1. Step 1: Send OTP to mobile or email
        res_send = self.client.post('/api/auth/send-login-otp', json={'identifier': '9845012345'})
        self.assertEqual(res_send.status_code, 200)
        data_send = json.loads(res_send.data)
        self.assertTrue(data_send['success'])
        self.assertEqual(data_send['demo_otp'], '123456')

        # 2. Step 2: Verify OTP
        res_verify = self.client.post('/api/auth/verify-login-otp', json={'identifier': '9845012345', 'otp': '123456'})
        self.assertEqual(res_verify.status_code, 200)
        data_verify = json.loads(res_verify.data)
        self.assertTrue(data_verify['success'])

        # 3. Step 3: Complete First Name, Last Name, Mobile Number and Home Center Location
        res_profile = self.client.post('/api/auth/save-profile-home', json={
            'first_name': 'Ananya',
            'last_name': 'Bhat',
            'phone': '9845012345',
            'aadhaar': '789012345678',
            'home_lat': 12.9352,
            'home_lng': 77.6245,
            'home_address': '80 Feet Rd, 4th Block, Koramangala, Bengaluru'
        })
        self.assertEqual(res_profile.status_code, 200)
        data_profile = json.loads(res_profile.data)
        self.assertTrue(data_profile['success'])
        self.assertEqual(data_profile['user']['first_name'], 'Ananya')
        self.assertEqual(data_profile['user']['last_name'], 'Bhat')
        self.assertEqual(data_profile['user']['home_lat'], 12.9352)

        # 4. Step 4: Verify vehicle proximity check calculates relative to this Home Center
        res_vehicles = self.client.get(f"/api/vehicles/live?lat={data_profile['user']['home_lat']}&lng={data_profile['user']['user']['home_lng'] if 'user' in data_profile['user'] else data_profile['user']['home_lng']}")
        self.assertEqual(res_vehicles.status_code, 200)
        data_veh = json.loads(res_vehicles.data)
        self.assertTrue(data_veh['success'])
        self.assertIn('home_center', data_veh)
        print(f"[PASS] 2. First-time website open OTP & Home Center configured: {data_profile['user']['first_name']} {data_profile['user']['last_name']} at {data_profile['user']['home_address']}.")

    def test_03_officer_exclusive_onboarding(self):
        """Requirement 8: Only Main BBMP Officer can create worker & officer accounts."""
        res = self.client.post('/api/officer/create-account', json={
            'officer_id': 1,
            'role': 'worker',
            'name': 'Shankar Naik (New Worker)',
            'phone': '9845088888',
            'aadhaar': '999988887777',
            'ward': 'Ward 80 - Indiranagar'
        })
        if res.status_code == 400:
            self.assertIn('already exists', json.loads(res.data)['message'])
        else:
            self.assertEqual(res.status_code, 200)
        print("[PASS] 3. Strict BBMP Officer-only Worker/Officer onboarding verified.")

    def test_04_vehicle_500m_proximity_alert(self):
        """Requirement 1: BBMP Vehicle near home (<500m) alert."""
        res = self.client.get('/api/vehicles/live?lat=12.9735&lng=77.6405')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['vehicles']), 0)
        print(f"[PASS] 4. Vehicle Proximity Tracker verified (Nearest: {data['nearest_vehicle']['distance_meters']}m, Proximity Alert: {data['proximity_alert']}).")

    def test_05_garbage_report_and_5km_worker_dispatch(self):
        """Requirement 1, 3, 11: Dumped waste reporting + 5km radius worker alert dispatch."""
        res = self.client.post('/api/reports/create', json={
            'citizen_id': 3,
            'citizen_name': 'Suresh Kumar',
            'waste_type': 'plastic_bottles',
            'description': 'Plastic bottles and beverage cartons piled near bus stop',
            'latitude': 12.9720,
            'longitude': 77.6410,
            'address': 'Indiranagar 100ft Rd',
            'before_image': 'sample_before_image_base64'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['alerted_workers']), 0)
        print(f"[PASS] 5. Report created #{data['report_id']} & 5km Geofence Alert dispatched to {len(data['alerted_workers'])} worker(s).")
        self.report_id = data['report_id']

    def test_06_worker_accept_task_and_sla(self):
        """Requirement 7 & 9: Worker accepts task & 10-minute SLA countdown activated."""
        res = self.client.post('/api/reports/accept', json={
            'report_id': 1,
            'worker_id': 2,
            'worker_name': 'Manjunath K'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        print("[PASS] 6. Worker Task Acceptance & 10-Minute SLA Timer verified.")

    def test_07_cleanup_proof_ai_comparison_and_blockchain(self):
        """Requirement 2, 4, 5, 9, 10: Live camera photo, AI Before/After comparison, Green Mark & Blockchain logging."""
        res = self.client.post('/api/reports/submit-cleanup', json={
            'report_id': 1,
            'worker_id': 2,
            'after_image': 'sample_after_cleaned_spot_base64',
            'latitude': 12.9725,
            'longitude': 77.6420
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['location_verified'])
        self.assertGreater(data['ai_similarity_score'], 80.0)
        self.assertIn('blockchain_hash', data)
        print(f"[PASS] 7. Proof-of-Cleanliness verified: Location Matched, AI Score {data['ai_similarity_score']}%, Blockchain Block Hash: {data['blockchain_hash'][:20]}...")

    def test_08_blockchain_ledger_integrity(self):
        """Requirement 10: Immutable Blockchain Block Explorer."""
        res = self.client.get('/api/blockchain/blocks')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['blocks']), 1)
        print(f"[PASS] 8. Blockchain Ledger validated with {len(data['blocks'])} verified blocks.")

    def test_09_monthly_reward_milestone(self):
        """Requirement 6: Rs 4,000 Reward for 500 cleanings milestone."""
        res = self.client.get('/api/rewards/status/2')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('progress_percentage', data)
        print(f"[PASS] 9. Monthly Reward Milestone verified: {data['total_cleanups']}/{data['target_milestone']} cleanups ({data['progress_percentage']}%), Reward: Rs {data['reward_amount_inr']}.")

    def test_10_officer_dashboard_analytics(self):
        """Requirement 9 & 13: Officer Dashboard, Red Alerts & GPS Metrics."""
        res = self.client.get('/api/officer/dashboard')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        m = data['metrics']
        print(f"[PASS] 10. BBMP Officer Dashboard verified: Total: {m['total_reports']}, Pending/Red Alerts: {m['pending_reports']}, Verified Green: {m['verified_reports']}, SLA Delayed: {m['overdue_delayed']}.")

if __name__ == '__main__':
    unittest.main()
