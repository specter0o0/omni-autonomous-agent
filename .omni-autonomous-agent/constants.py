from pathlib import Path
import sys

STATE_FILE = Path.home() / ".config" / "omni-agent" / "state.json"

BOLD = "\033[1m"
DIM  = "\033[2m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"
SEP = f"{DIM}{'─' * 54}{RESET}"

def supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

def c(code: str, text: str) -> str:
    return f"{code}{text}{RESET}" if supports_color() else text
