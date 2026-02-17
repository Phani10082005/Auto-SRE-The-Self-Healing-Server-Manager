import os
import subprocess
import time
import signal
import sys

# In a real world, we'd use PID files or systemd.
# Here, we'll use a scorched earth policy for the demo: kill anything on port 5000.

def kill_process_on_port(port):
    """Kills the process listening on the specified port (Windows)."""
    print(f"Finding process on port {port}...")
    try:
        # distinct steps to find and kill
        cmd_find = f"netstat -ano | findstr :{port}"
        result = subprocess.check_output(cmd_find, shell=True).decode()
        
        if not result:
            print(f"No process found on port {port}.")
            return

        # Parse PID (last column)
        lines = result.strip().split('\n')
        for line in lines:
            parts = line.strip().split()
            pid = parts[-1]
            if pid.isdigit() and int(pid) > 0:
                print(f"Killing PID {pid}...")
                subprocess.run(f"taskkill /F /PID {pid}", shell=True)
                
    except subprocess.CalledProcessError:
        print(f"No process found on port {port} (clean).")
    except Exception as e:
        print(f"Error killing process: {e}")

def start_app():
    """Starts the app.py and redirects output to app.log."""
    print("Starting app.py...")
    # calculating absolute path to ensure we find the file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app.py")
    log_path = os.path.join(os.path.dirname(script_dir), "app.log")
    
    # We use Popen so it runs in background
    with open(log_path, "a") as log_file:
        subprocess.Popen([sys.executable, app_path], stdout=log_file, stderr=log_file)
    
    print(f"App started. Logs redirected to {log_path}")

def main():
    print("Initiating Service Restart...")
    kill_process_on_port(5000)
    time.sleep(2) # Wait for port to clear
    start_app()
    print("Service Restart Configuration Completed.")

if __name__ == "__main__":
    main()
