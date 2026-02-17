import logging
import time
import sys
import threading
from flask import Flask, jsonify

# Configure logging so the Agent can "read" what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
# Ensure clean output
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Global flag to track app health
# True = 200 OK, False = 500 Error
SYSTEM_HEALTHY = True

@app.route('/')
def home():
    if SYSTEM_HEALTHY:
        return "System Status: NORMAL", 200
    else:
        return "System Status: CRITICAL FAILURE", 500

@app.route('/health')
def health_check():
    """
    Step 1 Target: This is the URL your monitor_app.py will ping.
    """
    if SYSTEM_HEALTHY:
        return jsonify({"status": "healthy"}), 200
    else:
        # This 500 error triggers the Agent
        return jsonify({"status": "unhealthy", "reason": "memory_leak"}), 500

@app.route('/simulate-crash')
def simulate_crash():
    """
    Step 2 Target: Triggers the specific error pattern in logs.
    """
    global SYSTEM_HEALTHY
    SYSTEM_HEALTHY = False
    
    # This specific log message is what your Agent looks for
    logging.critical("OUT_OF_MEMORY_EXCEPTION: Heap space exceeded limit.")
    logging.error("Process requires immediate restart.")
    
    return "Crash simulated. Check logs.", 200

if __name__ == '__main__':
    # Debug: Print all registered routes
    print("Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
        
    # Run on all interfaces so Docker can expose it
    app.run(host='0.0.0.0', port=5000)