import argparse
from .session_manager import cmd_add, cmd_status, cmd_cancel, cmd_dummy
from .installer import cmd_install

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
        cmd_cancel()

    elif args.dummy:
        cmd_dummy()

    elif args.install:
        cmd_install()
