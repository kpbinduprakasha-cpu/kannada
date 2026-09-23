"""
BBMP Swachha Bengaluru - Blockchain Service
Proof-of-Cleanliness Immutable Ledger & Milestone Reward Smart Contract Program.
"""

import hashlib
import json
import time
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, report_id, citizen_hash, worker_hash, before_image_hash, after_image_hash, gps_lat, gps_lng, reward_amount, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.report_id = report_id
        self.citizen_hash = citizen_hash
        self.worker_hash = worker_hash
        self.before_image_hash = before_image_hash
        self.after_image_hash = after_image_hash
        self.gps_lat = gps_lat
        self.gps_lng = gps_lng
        self.reward_amount = reward_amount
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        payload = f"{self.index}_{self.timestamp}_{self.report_id}_{self.citizen_hash}_{self.worker_hash}_{self.before_image_hash}_{self.after_image_hash}_{self.gps_lat}_{self.gps_lng}_{self.reward_amount}_{self.previous_hash}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'report_id': self.report_id,
            'citizen_hash': self.citizen_hash,
            'worker_hash': self.worker_hash,
            'before_image_hash': self.before_image_hash,
            'after_image_hash': self.after_image_hash,
            'gps': {'lat': self.gps_lat, 'lng': self.gps_lng},
            'reward_amount': self.reward_amount,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

class CleanBengaluruBlockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "2026-09-23 00:00:00", 0, "GENESIS", "GENESIS", "0"*32, "0"*32, 12.9716, 77.5946, 0.0, "0"*64)
        self.chain.append(genesis)

    def get_latest_block(self):
        return self.chain[-1]

    def add_cleanup_block(self, report_id, citizen_id, worker_id, before_img_data, after_img_data, lat, lng, reward_amount=10.0):
        prev_block = self.get_latest_block()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        citizen_hash = hashlib.sha256(f"CITIZEN_{citizen_id}".encode()).hexdigest()
        worker_hash = hashlib.sha256(f"WORKER_{worker_id}".encode()).hexdigest()
        before_hash = hashlib.sha256(str(before_img_data).encode()).hexdigest()
        after_hash = hashlib.sha256(str(after_img_data).encode()).hexdigest()

        new_block = Block(
            index=len(self.chain),
            timestamp=timestamp,
            report_id=report_id,
            citizen_hash=citizen_hash,
            worker_hash=worker_hash,
            before_image_hash=before_hash,
            after_image_hash=after_hash,
            gps_lat=lat,
            gps_lng=lng,
            reward_amount=reward_amount,
            previous_hash=prev_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            if curr.hash != curr.calculate_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True

if __name__ == "__main__":
    print("="*65)
    print("💎 BBMP SWACHHA BENGALURU - BLOCKCHAIN LEDGER TEST")
    print("="*65)

    bc = CleanBengaluruBlockchain()
    b1 = bc.add_cleanup_block(101, 3, 2, "img_before_plastic", "img_after_cleaned", 12.9725, 77.6420, 10.0)
    print(f"Block #1 Appended: {b1.hash}")
    print(f"Ledger Valid? {bc.is_chain_valid()}")
