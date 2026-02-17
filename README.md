# Auto SRE The Self Healing Server Manager
An AI Agent to act as a Level-1 Site Reliability Engineer. When the server crashes or slows down, the Agent detects it, diagnoses the root cause from the logs, fixes it, and writes a post-mortem report all without human intervention.

The Architecture 
You are simulating a production environment where things go wrong.

    The "Flaky" Microservice: A Python web app designed to be unstable. It simulates real-world problems like memory leaks or database disconnects.

    The "Monitor": A script or tool (like Prometheus or a simple Python loop) that checks the app's health every 5 seconds.

    The "Agent" (Antigravity): The decision-maker. It receives alerts from the Monitor, reads the logs, and decides which repair tool to use.

The Workflow
    The Trigger: The "Flaky" app is running normally. Suddenly, you trigger a "Memory Leak" simulation.

    The Failure: The app becomes unresponsive (returns 500 errors or times out).

    The Detection: The Monitor notices the 500 error and alerts the Agent.

    The Diagnosis (The AI Part):

        The Agent reads the Docker logs.

        It sees MemoryError: Stack Overflow (or similar).

        It "thinks": "The server is out of memory. A restart is required to clear the heap."

    The Action: The Agent executes docker restart app_container.

    The Verification: The Agent pings the health endpoint (/health) to confirm the app is back up.

    The Documentation: The Agent writes a file named post_mortem_20260215_162502 summarizing the crash and the fix.
