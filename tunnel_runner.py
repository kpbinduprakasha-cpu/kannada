import subprocess
import re
import time
import threading
import urllib.request
import sys

URL_FILE = "tunnel_url.txt"
current_url = None

def keep_alive():
    while True:
        time.sleep(45)
        if current_url:
            try:
                urllib.request.urlopen(current_url, timeout=10)
                # Keepalive successful
            except Exception:
                pass

t = threading.Thread(target=keep_alive, daemon=True)
t.start()

cmd = [
    "ssh",
    "-o", "StrictHostKeyChecking=no",
    "-o", "ServerAliveInterval=10",
    "-o", "ServerAliveCountMax=3",
    "-R", "80:127.0.0.1:5000",
    "nokey@localhost.run"
]

print("Starting resilient tunnel runner...")
while True:
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in iter(proc.stdout.readline, ''):
            sys.stdout.write(line)
            sys.stdout.flush()
            match = re.search(r'https://[a-zA-Z0-9\.\-]+\.lhr\.life', line)
            if match:
                current_url = match.group(0)
                print(f"\n[ACTIVE TUNNEL URL]: {current_url}\n", flush=True)
                with open(URL_FILE, "w", encoding="utf-8") as f:
                    f.write(current_url)
        proc.wait()
    except Exception as e:
        print(f"Tunnel runner error: {e}", flush=True)
    time.sleep(3)
    print("Reconnecting tunnel...", flush=True)
