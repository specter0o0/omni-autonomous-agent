#!/usr/bin/env python3
"""
omni-autonomous-agent — autonomous session manager

Commands:
  --add -R "<request>" -D <minutes>   Register a new session
  --dummy                             Register a dummy session for testing
  --status                            Show current session state
  --clear                             Clear the active session
  --install                           Install to PATH as 'omni-autonomous-agent'
"""

import argparse
import json
import os
import stat
import sys
from datetime import datetime, timedelta
from pathlib import Path

STATE_FILE = Path.home() / ".config" / "omni-agent" / "state.json"

BOLD = "\033[1m"
DIM  = "\033[2m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"
SEP = f"{DIM}{'─' * 54}{RESET}"


def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    return f"{code}{text}{RESET}" if _supports_color() else text


def _save(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def _load() -> dict | None:
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def _fmt_remaining(seconds: float) -> str:
    if seconds <= 0:
        return _c(RED, "past deadline")
    t = int(seconds)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    parts = []
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}m")
    if s or not parts:
        parts.append(f"{s}s")
    text = " ".join(parts)
    return _c(YELLOW, text) if seconds < 300 else text


def _row(label: str, value: str) -> None:
    print(f"  {_c(DIM, label + ':'): <16}  {value}")


def _header(title: str) -> None:
    print(SEP)
    print(f"  {_c(BOLD, title)}")
    print(SEP)


def cmd_add(request: str, duration: int) -> None:
    if duration <= 0:
        sys.exit("error: duration must be a positive integer (minutes)")

    now = datetime.now()
    deadline = now + timedelta(minutes=duration)
    _save({
        "request": request,
        "duration_minutes": duration,
        "started_at": now.isoformat(),
        "deadline": deadline.isoformat(),
    })

    _header(f"{_c(GREEN, '✓')} Session registered")
    _row("Request",  request)
    _row("Duration", f"{duration} min")
    _row("Started",  now.strftime("%a %b %d %Y · %H:%M:%S"))
    _row("Deadline", _c(BOLD, deadline.strftime("%a %b %d %Y · %H:%M:%S")))
    print(SEP)


def cmd_dummy() -> None:
    cmd_add("Dummy session — testing omni-autonomous-agent", 60)



    state = _load()
    now = datetime.now()

    if not state:
        _header("omni-autonomous-agent")
        print("  No active session.")
        print(SEP)
        return

    deadline  = datetime.fromisoformat(state["deadline"])
    started   = datetime.fromisoformat(state["started_at"])
    remaining = (deadline - now).total_seconds()
    elapsed   = (now - started).total_seconds()
    pct_done  = min(100, int((elapsed / (state["duration_minutes"] * 60)) * 100))

    active    = remaining > 0
    label     = "Active Session" if active else "Session Expired"
    _header(f"omni-autonomous-agent · {_c(GREEN if active else RED, label)}")
    _row("Request",   state["request"])
    _row("Now",       now.strftime("%a %b %d %Y · %H:%M:%S"))
    _row("Started",   started.strftime("%a %b %d %Y · %H:%M:%S"))
    _row("Deadline",  deadline.strftime("%a %b %d %Y · %H:%M:%S"))
    _row("Duration",  f"{state['duration_minutes']} min")
    _row("Elapsed",   f"{int(elapsed // 60)}m {int(elapsed % 60)}s  ({pct_done}%)")
    _row("Remaining", _fmt_remaining(remaining))
    print(SEP)


def cmd_clear() -> None:
    if not STATE_FILE.exists():
        print("  No active session to clear.")
        return
    STATE_FILE.unlink()
    print(f"{_c(GREEN, '✓')} Session cancelled.")


def cmd_install() -> None:
    script = Path(__file__).resolve()
    candidates = [
        Path.home() / ".local" / "bin",
        Path("/usr/local/bin"),
    ]

    target_dir = None
    for d in candidates:
        if d.exists() and os.access(d, os.W_OK):
            target_dir = d
            break

    if target_dir is None:
        sys.exit(
            "error: no writable bin directory found.\n"
            "       Add ~/.local/bin to your PATH or run with sudo for /usr/local/bin."
        )

    dest = target_dir / "omni-autonomous-agent"
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    dest.symlink_to(script)
    script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    _header(f"{_c(GREEN, '✓')} Installed")
    _row("Source", str(script))
    _row("Link",   str(dest))
    print()
    print(f"  Run {_c(BOLD, 'omni-autonomous-agent --status')} to verify.")

    path_dirs = os.environ.get("PATH", "").split(":")
    if str(target_dir) not in path_dirs:
        print()
        print(f"  {_c(YELLOW, '!')}"
              f" {target_dir} is not in your PATH. Add it:")
        print(f'    export PATH="{target_dir}:$PATH"')
    print(SEP)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omni-autonomous-agent",
        description="Autonomous session manager for AI agents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add",     action="store_true", help="Register a new session")
    group.add_argument("--dummy",   action="store_true", help="Register a dummy session for testing")
    group.add_argument("--status",  action="store_true", help="Show session status")
    group.add_argument("--cancel",  action="store_true", help="Cancel the active session")
    group.add_argument("--install", action="store_true", help="Install to PATH")

    parser.add_argument("-R", "--request",  metavar="REQUEST",  type=str, help="Task request (required with --add)")
    parser.add_argument("-D", "--duration", metavar="MINUTES",  type=int, help="Duration in minutes (required with --add)")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.add:
        missing = [f for f, v in [("-R/--request", args.request), ("-D/--duration", args.duration)] if v is None]
        if missing:
            parser.error(f"--add requires: {', '.join(missing)}")
        cmd_add(args.request, args.duration)

    elif args.status:
        cmd_status()

    elif args.cancel:
        cmd_clear()

    elif args.install:
        cmd_install()


if __name__ == "__main__":
    main()