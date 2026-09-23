# BBMP Swachha Bengaluru - Smart Waste Management & Blockchain Verification

A production-grade municipal smart waste collection, real-time GPS tracking, AI-powered Before/After cleanup verification, multi-role portal (Citizen, Worker, BBMP Officer), and Blockchain reward ecosystem.

---

## 👤 Author & Maintainer
- **K P Bindu Prakasha** ([@kpbinduprakasha-cpu](https://github.com/kpbinduprakasha-cpu))
- Project Repository: [https://github.com/kpbinduprakasha-cpu/kannada](https://github.com/kpbinduprakasha-cpu/kannada)

---

## 🌟 Key Features Implemented

1. **First-Time Website Open Onboarding & Home Center Setup**:
   - **Step 1**: Enter Mobile Number or Email to receive 6-digit OTP.
   - **Step 2**: 6-digit OTP identity verification.
   - **Step 3**: Setup First Name, Last Name, Mobile Number, and pin your **Home Center Location** (GPS or Bengaluru Neighborhood presets: Indiranagar, Koramangala, Jayanagar, etc.).

2. **Home Center-Anchored Vehicle Proximity Alert (< 500m)**:
   - Tracks BBMP garbage collection vehicles in real-time.
   - When a vehicle enters within 500 meters of your Home Center, an instant alert pops up, playing the traditional chime and Kannada + English voice announcement (*"BBMP ಕಸದ ವಾಹನ ಬಂದಿದೆ! / BBMP Waste collection truck is near your home!"*).

3. **Roadside Spot Garbage Reporting & 5km Worker Dispatch**:
   - Citizens can snap/upload a photo of dumped garbage (plastic bottles, vegetable wet waste, mixed garbage, or e-waste).
   - Auto-captures GPS coordinates and automatically dispatches alerts to all on-duty workers within a **5 km radius** using the Haversine spatial matching engine.

4. **Sanitation Worker Live Proof of Work**:
   - Hardware-bound camera capture preventing gallery uploads.
   - Real-time embedded GPS latitude/longitude and ISO timestamp watermark.
   - Proximity verification ($\pm 25$m tolerance) ensuring the worker is physically at the dumped spot.

5. **10-Minute SLA Watchdog & Red Alert Badges**:
   - When a worker accepts a task, a **10:00 countdown timer** starts.
   - If the task is delayed past 10 minutes without completion, it turns into a glowing **RED ALERT (SLA OVERDUE)** state and escalates to the BBMP Officer.
   - Once successfully cleaned and verified, the report switches to a vibrant **GREEN MARK (CLEANED & VERIFIED)** badge.

6. **AI Vision Verification (Before vs. After)**:
   - Evaluates background physical consistency (walls, pavements, curb lines) and confirms complete waste removal before clearing the ticket.

7. **₹4,000 Monthly Milestone Reward**:
   - Automatic tracker for monthly cleanups.
   - When a citizen or worker reaches **500 verified cleanups** in a month, an automated **₹4,000 cash bonus** is unlocked and logged on-chain.

8. **Strict Multi-Role Security & Aadhaar OTP**:
   - **Citizens**: Register with Name, 12-digit Aadhaar number, and Mobile OTP.
   - **Workers & Sub-Officers**: Can **ONLY** be created and authorized by the Main BBMP Officer (Super Admin).

9. **SHA-256 Blockchain Audit Explorer**:
   - Every verified cleanup is stored in an immutable cryptographic block containing:
     - Block Index & Timestamp
     - Report ID
     - Citizen Hash & Worker Hash
     - Before & After Photo SHA-256 Hashes
     - Geotagged Lat/Lng
     - Previous Block Hash & Current Block Hash

10. **Bengaluru GIS Municipal Radar Map**:
    - Interactive Leaflet map displaying real-time positions of BBMP garbage vehicles, on-duty workers, 500m household proximity zones, 5km worker dispatch radiuses, and incident status pins.

---

## 🚀 How to Run

### Method 1: Double-Click Launcher
Double-click `run.bat` in this folder.

### Method 2: Command Line
```powershell
.venv\Scripts\python.exe app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Automated Testing

Run the included end-to-end test suite:
```powershell
.venv\Scripts\python.exe test_system.py
```
All 10 test cases validate:
- Web UI delivery
- Aadhaar + OTP validation
- Initial website open onboarding flow
- Home Center distance anchoring
- Officer-exclusive staff creation
- 500m vehicle proximity alerts
- 5km spatial worker dispatch
- 10-minute SLA watchdog
- AI comparison & Blockchain ledger logging
- ₹4,000 monthly reward progress
- BBMP Officer GIS dashboard metrics
