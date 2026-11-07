"""Core Sandbox Syscall Monitor implementation."""
import re
import shlex
from typing import List, Dict, Any, Optional


class InspectionResult:
    def __init__(self, allowed: bool, command: str, reason: str = ""):
        self.allowed = allowed
        self.command = command
        self.reason = reason

    def to_dict(self) -> Dict[str, Any]:
        return {
            "allowed": self.allowed,
            "command": self.command,
            "reason": self.reason
        }


class SandboxSyscallMonitor:
    DANGEROUS_PATTERNS = [
        r"rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|--force|--recursive)\s+/",
        r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:",  # Fork bomb
        r"mkfs",
        r"dd\s+if=.*of=/dev/",
        r">\s*/dev/sd[a-z]",
        r"curl.*\|\s*(bash|sh)",
        r"wget.*\|\s*(bash|sh)",
        r"nc\s+.*-e\s+(/bin/sh|/bin/bash)"
    ]

    def __init__(self, allowed_workdirs: Optional[List[str]] = None):
        self.allowed_workdirs = allowed_workdirs or []

    def inspect_command(self, cmd_str: str) -> InspectionResult:
        # Check dangerous shell regexes
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, cmd_str, re.IGNORECASE):
                return InspectionResult(False, cmd_str, f"Dangerous command pattern matched: {pattern}")

        # Check path traversal
        if "../../../" in cmd_str:
            return InspectionResult(False, cmd_str, "Deep directory path traversal detected")

        return InspectionResult(True, cmd_str, "Allowed")
