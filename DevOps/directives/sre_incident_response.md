# SRE Incident Response Directive

**Goal**: Restore service availability and document the incident.

**Triggers**: 
- `monitor_app.py` reports DOWN or SLOW.
- HTTP 500 errors detected.

**Inputs**:
- App Logs (`app.log` or similar)
- Error Message from Monitor

**Outputs**:
- Restored Service
- `post_mortem.md` report

**Procedure**:

1.  **Acknowledge**: Log that an incident has been detected.
2.  **Diagnose**:
    - Run `execution/diagnose_and_heal.py --mode=diagnose --log-path <LOG_PATH>`
    - Identify the Root Cause (e.g., Database Connection Failed, Memory Leak, Syntax Error).
3.  **Heal**:
    - Based on diagnosis, execute the matching repair action:
        - *DB Connection Failed* -> Run `execution/restart_service.py --target=db`
        - *Memory Leak* -> Run `execution/restart_service.py --target=app`
        - *Disk Full* -> Run `execution/clear_cache.py`
    - Verify health by re-running `execution/monitor_app.py`.
4.  **Report**:
    - Run `execution/generate_post_mortem.py` with incident details.
    - Save report to `incident_reports/` (cloud sync recommended).

**Escalation**:
- If auto-healing fails twice, notify the human admin immediately.
