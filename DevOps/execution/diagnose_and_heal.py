import sys
import argparse
import time

def analyze_logs(log_path):
    """Simulates log analysis to find root cause."""
    print(f"Analyzing logs at: {log_path}")
    try:
        with open(log_path, 'r') as f:
            lines = f.readlines()
            # Simple heuristic for demonstration
            for line in reversed(lines[-50:]): # Check last 50 lines
                if "OUT_OF_MEMORY_EXCEPTION" in line:
                    return "MEMORY_LEAK"
                if "ConnectionRefused" in line:
                    return "DB_FAILURE"
                if "SegFault" in line:
                    return "CRITICAL_CRASH"
    except FileNotFoundError:
        print("Log file not found.")
        return "UNKNOWN"
    return "UNKNOWN"

import subprocess
import os

def restart_service(service_name):
    """Restarts the service using the restart_service.py script."""
    print(f"Attempting to restart service: {service_name}...")
    try:
        # Assuming we are running from project root
        script_path = os.path.join("execution", "restart_service.py")
        if not os.path.exists(script_path):
             # Try absolute path if we are in execution dir
             script_path = "restart_service.py"
        
        subprocess.run([sys.executable, script_path], check=True)
        print(f"Service {service_name} restart triggered.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart service: {e}")
        return False

def heal(diagnosis):
    """Executes healing action based on diagnosis."""
    if diagnosis == "DB_FAILURE":
        return restart_service("database")
    elif diagnosis == "MEMORY_LEAK":
        return restart_service("application_server")
    elif diagnosis == "CRITICAL_CRASH":
        return restart_service("application_server")
    else:
        print("Unknown diagnosis. Attempting generic restart.")
        return restart_service("application_server")

def main():
    parser = argparse.ArgumentParser(description="SRE Diagnose and Heal Tool")
    parser.add_argument("--mode", choices=["diagnose", "heal", "auto"], default="auto")
    parser.add_argument("--log-path", default="app.log", help="Path to application logs")
    
    args = parser.parse_args()
    
    if args.mode in ["diagnose", "auto"]:
        diagnosis = analyze_logs(args.log_path)
        print(f"Diagnosis: {diagnosis}")
        
    if args.mode in ["heal", "auto"]:
        if args.mode == "heal":
            # If only healing, assume generic or passed via other means
            diagnosis = "UNKNOWN" 
        
        success = heal(diagnosis)
        if success:
            print("Healing procedure completed.")
            sys.exit(0)
        else:
            print("Healing failed.")
            sys.exit(1)

if __name__ == "__main__":
    main()
