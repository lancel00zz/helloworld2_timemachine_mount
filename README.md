Time Machine Disk Mount Monitoring (Datadog Custom Check)
========================================================

This repository contains a Datadog Agent custom check that is part of the
**helloworld2 utility suite**, used to monitor the mount status of a macOS
Time Machine backup disk.

Purpose
-------
Time Machine backups can silently stop working when the destination disk
is disconnected (e.g. laptop undocked, cable unplugged).

This check provides an explicit, reliable monitoring signal indicating
whether the configured Time Machine destination disk is currently mounted.

What the check does
-------------------
On each execution, the Python check performs the following actions:

- Emits a heartbeat metric to confirm the check is running
- Inspects the macOS system mount table
- Emits a binary metric indicating whether the configured mountpoint
  is currently mounted

This check is designed to be robust in laptop environments where disks
may be intermittently connected or disconnected.

Metrics emitted
---------------
The check emits the following metrics under the `helloworld2` namespace:

- **helloworld2.timemachine.heartbeat**
  Always emits value `1` to indicate the check is executing successfully.

- **helloworld2.timemachine.mounted**
  Reports the mount state of the configured disk:
  - `0` = not mounted / unavailable
  - `1` = mounted and available

Configuration (conf.yaml)
-------------------------
The check behavior is configured via `conf.yaml`.

Each instance defines a single mountpoint to monitor and optional tags
to attach to all emitted metrics.

Configuration options:

- **mountpoint**
  The filesystem mountpoint to monitor.
  Example:
    `/Volumes/SEAGATE TIME MACHINE 5T`

- **tags**
  Optional tags attached to emitted metrics, used for filtering,
  grouping, dashboards, and alerting in Datadog.

Example configuration:

```yaml
instances:
  - mountpoint: "/Volumes/SEAGATE TIME MACHINE 5T"
    tags:
      - suite:helloworld2
      - component:timemachine
      - timemachine_destination:seagate_time_machine_5t