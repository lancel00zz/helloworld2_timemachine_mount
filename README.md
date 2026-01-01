Time Machine Disk Mount Monitoring (Datadog Custom Check)
========================================================

This repository contains a Datadog Agent custom check used to monitor
the mount status of a macOS Time Machine backup disk.

Purpose
-------
Time Machine backups silently stop working when the destination disk
is disconnected. This check provides an explicit monitoring signal
to detect that situation.

What the check does
-------------------
The Python check performs the following actions on each run:

- Emits a heartbeat metric to confirm the check is executing
- Inspects the system mount table on macOS
- Emits a binary metric indicating whether the configured mountpoint
  is currently mounted

Metrics emitted
---------------
- timemachine.heartbeat
  Always emits value 1 to indicate the check is running

- timemachine.disk_mounted
  Reports the mount state of the configured disk:
  - 0 = not mounted / unavailable
  - 1 = mounted and available

Configuration (conf.yaml)
-------------------------
The check behavior is configured via conf.yaml:

- mountpoint
  The filesystem mountpoint to monitor
  Example:
    /Volumes/SEAGATE TIME MACHINE 5T

- tags
  Optional tags attached to all emitted metrics, used for filtering
  and alerting in Datadog

Example:

instances:
  - mountpoint: "/Volumes/SEAGATE TIME MACHINE 5T"
    tags:
      - timemachine_destination:seagate_time_machine_5t

Usage
-----
1. Install the Python check under the Datadog Agent checks.d directory
2. Add the conf.yaml under conf.d/time_machine_mount.d/
3. Restart the Datadog Agent
4. Verify metrics in Datadog Metrics Explorer
5. Create a monitor on timemachine.disk_mounted < 1

Notes
-----
- The check is macOS-specific and relies on the system mount output
- No logs are required for normal operation; metrics are sufficient
- Designed for laptop environments where disks may be intermittently
  connected or disconnected