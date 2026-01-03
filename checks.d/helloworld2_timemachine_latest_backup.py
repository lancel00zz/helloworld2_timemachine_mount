import os
import re
import subprocess
from datetime import datetime, timezone

from datadog_checks.base import AgentCheck


class Helloworld2TimeMachineLatestBackup(AgentCheck):
    def check(self, instance):
        tags = list(instance.get("tags", []))

        # Heartbeat: proves the check is executing and metrics can reach Datadog
        self.gauge("helloworld2.timemachine.latest_backup_heartbeat", 1, tags=tags)

        # Default: if anything fails, emit "unknown" as a large age OR -1.
        # I recommend -1 so it's explicit and easy to alert on.
        latest_backup_seconds = -1

        try:
            # Example output:
            # /Volumes/SEAGATE TIME MACHINE 5T/Backups.backupdb/<MacName>/2026-01-01-141512
            out = subprocess.check_output(["/usr/bin/tmutil", "latestbackup"], text=True).strip()

            # Extract the trailing timestamp folder (Time Machine format is typically YYYY-MM-DD-HHMMSS)
            m = re.search(r"(\d{4}-\d{2}-\d{2}-\d{6})$", out)
            if not m:
                raise ValueError(f"Could not parse backup timestamp from: {out}")

            ts = m.group(1)  # e.g. 2026-01-01-141512
            backup_dt = datetime.strptime(ts, "%Y-%m-%d-%H%M%S").replace(tzinfo=timezone.utc)

            # Use UTC consistently to avoid DST/local parsing issues.
            now = datetime.now(timezone.utc)
            latest_backup_seconds = int((now - backup_dt).total_seconds())

            if latest_backup_seconds < 0:
                # Clock skew shouldn't happen, but guard anyway.
                latest_backup_seconds = 0

            # Optional: service check OK if parsing succeeded
            self.service_check("helloworld2.timemachine.latest_backup", self.OK, tags=tags)

        except Exception as e:
            # Emit CRITICAL service check, but still emit the metric as -1 (explicit unknown)
            self.service_check("helloworld2.timemachine.latest_backup", self.CRITICAL, message=str(e), tags=tags)

        # Always emit the metric, even on failure
        self.gauge("helloworld2.timemachine.latest_backup_seconds", latest_backup_seconds, tags=tags)