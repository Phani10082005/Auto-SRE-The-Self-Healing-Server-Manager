import requests
import time
import sys
import os

# Configuration (To be moved to .env in production)
APP_URL = os.getenv("APP_URL", "http://127.0.0.1:5000/health")
CHECK_INTERVAL_SECONDS = 10
TIMEOUT_SECONDS = 2

def check_health():
    """Pings the app health endpoint."""
    try:
        response = requests.get(APP_URL, timeout=TIMEOUT_SECONDS)
        if response.status_code == 200:
            print(f"[OK] App is healthy. Status: {response.status_code}")
            return True
        else:
            print(f"[ERROR] App returned status: {response.status_code} at {APP_URL}")
            print(f"[DEBUG] Response content: {response.text[:200]}") # Print first 200 chars
            return False
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Connection refused. App might be down.")
        return False
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timed out.")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

def main():
    print(f"Starting Monitor for {APP_URL}...")
    while True:
        is_healthy = check_health()
        if not is_healthy:
            print("!!! FAILURE DETECTED !!! Triggering SRE Agent...")
            # Trigger the SRE Agent
            # In a real system, this might fire a webhook or message queue event.
            # Here, we call the script directly.
            
            # 1. Diagnose and Heal
            diagnose_cmd = f"{sys.executable} execution/diagnose_and_heal.py --mode auto --log-path app.log"
            os.system(diagnose_cmd)
            
            # 2. Generate Report (assuming healing worked, otherwise we might report failure)
            # We'll just generate a report for the attempt.
            report_cmd = f"{sys.executable} execution/generate_post_mortem.py"
            os.system(report_cmd)
            
            # Wait a bit for the app to come back up before monitoring again
            time.sleep(10) 
            
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
