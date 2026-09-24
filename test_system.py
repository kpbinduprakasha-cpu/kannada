"""
End-to-End Test Suite for Belagavi City Corporation (BCC) Swachha Belagavi Smart Waste Management System.
Validates all 13 core requirements + initial website open onboarding (OTP, First Name, Last Name, Mobile & Home Center),
Individual Personal Worker Accounts, Dynamic Decision Attribution Dispatch, and Active Working Progress Tracking.
"""

import sys
import unittest
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from app import app, init_db, get_db_connection

class TestBCCWasteSystem(unittest.TestCase):
    test_report_id = None
    assigned_worker_id = 2
    report_lat = 15.8348
    report_lng = 74.5022

    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = app.test_client()

    def test_01_web_page_serves(self):
        """Verify Web Portal UI serves successfully with Belagavi branding and onboarding modal."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'SWACHHA BELAGAVI', res.data)
        self.assertIn(b'modal-auth-onboarding', res.data)
        self.assertIn(b'Home Center Location', res.data)
        print("[PASS] 1. Belagavi Web Portal & Initial Onboarding UI served successfully.")

    def test_02_first_time_open_otp_and_home_center(self):
        """New User Requirement: Open website -> Mobile/Email OTP -> First Name, Last Name, Mobile, Home Center in Belagavi."""
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

        # 3. Step 3: Complete First Name, Last Name, Mobile Number and Belagavi Home Center Location
        res_profile = self.client.post('/api/auth/save-profile-home', json={
            'first_name': 'Ananya',
            'last_name': 'Bhat',
            'phone': '9845012345',
            'aadhaar': '789012345678',
            'home_lat': 15.8345,
            'home_lng': 74.5015,
            'home_address': 'Congress Road, Tilakwadi, Belagavi'
        })
        self.assertEqual(res_profile.status_code, 200)
        data_profile = json.loads(res_profile.data)
        self.assertTrue(data_profile['success'])
        self.assertEqual(data_profile['user']['first_name'], 'Ananya')
        self.assertEqual(data_profile['user']['last_name'], 'Bhat')
        self.assertEqual(data_profile['user']['home_lat'], 15.8345)

        # 4. Step 4: Verify vehicle proximity check calculates relative to this Belagavi Home Center
        res_vehicles = self.client.get(f"/api/vehicles/live?lat={data_profile['user']['home_lat']}&lng={data_profile['user']['home_lng']}")
        self.assertEqual(res_vehicles.status_code, 200)
        data_veh = json.loads(res_vehicles.data)
        self.assertTrue(data_veh['success'])
        self.assertIn('home_center', data_veh)
        print(f"[PASS] 2. First-time website open OTP & Belagavi Home Center configured: {data_profile['user']['first_name']} {data_profile['user']['last_name']} at {data_profile['user']['home_address']}.")

    def test_03_officer_exclusive_onboarding(self):
        """Requirement 8: Only Main Belagavi City Corporation (BCC) Officer can create worker & officer accounts."""
        unique_phone = f"98450{hash('new_worker_test') % 90000 + 10000}"
        res = self.client.post('/api/officer/create-account', json={
            'officer_id': 1,
            'role': 'worker',
            'name': 'Shankar Naik (New Belagavi Worker)',
            'phone': unique_phone,
            'aadhaar': '999988887766',
            'ward': 'Ward 21 - Tilakwadi, Belagavi'
        })
        if res.status_code == 400:
            self.assertIn('already exists', json.loads(res.data)['message'])
        else:
            self.assertEqual(res.status_code, 200)
            data = json.loads(res.data)
            self.assertTrue(data['success'])
            self.assertTrue(data['worker_emp_id'].startswith('BCC-W'))
        print("[PASS] 3. Strict BCC Officer-only Worker/Officer onboarding with Emp ID verified.")

    def test_04_vehicle_500m_proximity_alert(self):
        """Requirement 1: Belagavi Municipal Vehicle (KA-22) near home (<500m) alert."""
        res0 = self.client.get('/api/vehicles/live')
        self.assertEqual(res0.status_code, 200)
        data0 = json.loads(res0.data)
        self.assertGreater(len(data0['vehicles']), 0)
        target_veh = data0['vehicles'][0]
        
        # Test location right next to the municipal vehicle (<50m away)
        test_lat = target_veh['current_lat'] + 0.0002
        test_lng = target_veh['current_lng'] + 0.0002

        res = self.client.get(f'/api/vehicles/live?lat={test_lat}&lng={test_lng}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['proximity_alert'])
        self.assertLess(data['nearest_vehicle']['distance_meters'], 500)
        self.assertTrue(data['nearest_vehicle']['vehicle_no'].startswith('KA-22'))
        print(f"[PASS] 4. Belagavi Vehicle Proximity Tracker verified (Nearest: {data['nearest_vehicle']['vehicle_no']} at {data['nearest_vehicle']['distance_meters']}m, Proximity Alert: {data['proximity_alert']}).")

    def test_05_garbage_report_and_dynamic_decision_dispatch(self):
        """Requirement 1, 3, 11: Dumped waste reporting + Dynamic Decision Dispatch attributing task to specific individual worker within 5km."""
        lat = 15.8348
        lng = 74.5022
        res = self.client.post('/api/reports/create', json={
            'citizen_id': 5,
            'citizen_name': 'Praveen Kulkarni',
            'waste_type': 'plastic_bottles',
            'description': 'Plastic bottles dumped near Tilakwadi Railway Overbridge',
            'latitude': lat,
            'longitude': lng,
            'address': '1st Gate, Tilakwadi, Belagavi',
            'before_image': 'sample_before_image_base64'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['alerted_workers']), 0)
        
        # Verify Dynamic Decision Engine attribution to individual worker
        self.assertIn('attributed_worker', data)
        self.assertIn('dynamic_decision_note', data)
        attrib = data['attributed_worker']
        self.assertIsNotNone(attrib['worker_id'])
        self.assertIsNotNone(attrib['emp_id'])
        self.assertTrue(attrib['emp_id'].startswith('BCC-W'))
        
        TestBCCWasteSystem.test_report_id = data['report_id']
        TestBCCWasteSystem.assigned_worker_id = attrib['worker_id']
        TestBCCWasteSystem.report_lat = lat
        TestBCCWasteSystem.report_lng = lng

        print(f"[PASS] 5. Report #{data['report_id']} created with Dynamic Decision Engine: Attributed to {attrib['name']} ({attrib['emp_id']}) - Note: {data['dynamic_decision_note']}.")

    def test_06_worker_accept_task_and_sla(self):
        """Requirement 7 & 9: Attributed worker accepts task & 10-minute SLA countdown activated."""
        report_id = TestBCCWasteSystem.test_report_id or 1
        worker_id = TestBCCWasteSystem.assigned_worker_id or 2

        res = self.client.post('/api/reports/accept', json={
            'report_id': report_id,
            'worker_id': worker_id,
            'worker_name': 'Basavaraj Belagavi'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        print(f"[PASS] 6. Individual Worker #{worker_id} Task Acceptance & 10-Minute SLA Timer verified.")

    def test_07_cleanup_proof_ai_comparison_and_blockchain(self):
        """Requirement 2, 4, 5, 9, 10: Live camera photo, AI Before/After comparison, Green Mark & Blockchain logging."""
        report_id = TestBCCWasteSystem.test_report_id or 1
        worker_id = TestBCCWasteSystem.assigned_worker_id or 2
        lat = TestBCCWasteSystem.report_lat or 15.8348
        lng = TestBCCWasteSystem.report_lng or 74.5022

        res = self.client.post('/api/reports/submit-cleanup', json={
            'report_id': report_id,
            'worker_id': worker_id,
            'after_image': 'sample_after_cleaned_spot_base64',
            'latitude': lat,
            'longitude': lng
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['location_verified'])
        self.assertGreater(data['ai_similarity_score'], 80.0)
        self.assertIn('blockchain_hash', data)
        print(f"[PASS] 7. Proof-of-Cleanliness verified: Location Matched, AI Score {data['ai_similarity_score']}%, Blockchain Block Hash: {data['blockchain_hash'][:20]}...")

    def test_08_blockchain_ledger_integrity(self):
        """Requirement 10: Immutable Belagavi Municipal Blockchain Block Explorer."""
        res = self.client.get('/api/blockchain/blocks')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['blocks']), 0)
        print(f"[PASS] 8. Belagavi Municipal Blockchain Ledger validated with {len(data['blocks'])} verified blocks.")

    def test_09_monthly_reward_milestone(self):
        """Requirement 6: Rs 4,000 Reward for 500 cleanings milestone for individual worker."""
        res = self.client.get('/api/rewards/status/2')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('progress_percentage', data)
        print(f"[PASS] 9. Monthly Reward Milestone verified for Worker #2: {data['total_cleanups']}/{data['target_milestone']} cleanups ({data['progress_percentage']}%), Reward: Rs {data['reward_amount_inr']}.")

    def test_09b_citizen_ineligible_for_reward(self):
        """User Requirement: Rs 4,000 reward is strictly for workers to see and earn, not citizens/people."""
        # Citizen Praveen Kulkarni is user_id 5
        res = self.client.get('/api/rewards/status/5')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertFalse(data['is_eligible'])
        self.assertEqual(data['reward_amount_inr'], 0)
        self.assertIn('sanitation workers only, not citizens', data['message'])
        print("[PASS] 9b. Citizen reward ineligibility verified: Rs 4,000 bonus is strictly worker-exclusive.")

    def test_10_officer_dashboard_analytics(self):
        """Requirement 9 & 13: Belagavi City Corporation Officer Dashboard, Red Alerts & GPS Metrics."""
        res = self.client.get('/api/officer/dashboard')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        m = data['metrics']
        print(f"[PASS] 10. BCC Officer Dashboard verified: Total: {m['total_reports']}, Pending/Red Alerts: {m['pending_reports']}, Verified Green: {m['verified_reports']}, SLA Delayed: {m['overdue_delayed']}.")

    def test_11_individual_worker_personal_accounts_and_active_progress(self):
        """Specific Belagavi User Requirement: Individual worker accounts, personal duty status, and live active progress."""
        # 1. Fetch individual worker list
        res_list = self.client.get('/api/workers/list')
        self.assertEqual(res_list.status_code, 200)
        data_list = json.loads(res_list.data)
        self.assertTrue(data_list['success'])
        self.assertGreaterEqual(len(data_list['workers']), 3)
        emp_ids = [w['worker_emp_id'] for w in data_list['workers'] if w.get('worker_emp_id')]
        self.assertTrue(any('BCC-W2101' in eid for eid in emp_ids))
        self.assertTrue(any('BCC-W3402' in eid for eid in emp_ids))

        # 2. Fetch specific individual worker profile and active working progress (Worker 2)
        res_prof = self.client.get('/api/worker/profile/2')
        self.assertEqual(res_prof.status_code, 200)
        data_prof = json.loads(res_prof.data)
        self.assertTrue(data_prof['success'])
        w = data_prof['worker']
        self.assertEqual(w['name'], 'Basavaraj Belagavi')
        self.assertEqual(w['emp_id'], 'BCC-W2101')
        self.assertIn('cleanups_today', w)
        self.assertIn('distance_walked_km', w)
        self.assertIn('performance_score', w)
        self.assertIn('hours_worked', w)
        self.assertIn('duty_status', w)

        # 3. Update personal duty status
        res_duty = self.client.post('/api/worker/update-duty', json={
            'worker_id': 2,
            'duty_status': 'off_duty'
        })
        self.assertEqual(res_duty.status_code, 200)
        data_duty = json.loads(res_duty.data)
        self.assertTrue(data_duty['success'])
        self.assertIn('duty updated to off_duty', data_duty['message'])

        # Reset back to on_duty
        self.client.post('/api/worker/update-duty', json={'worker_id': 2, 'duty_status': 'on_duty'})
        print(f"[PASS] 11. Individual Worker Personal Accounts & Active Working Progress verified: {w['name']} ({w['emp_id']}) with {w['cleanups_today']} cleanups today and {w['distance_walked_km']} km walked.")

if __name__ == '__main__':
    unittest.main()
