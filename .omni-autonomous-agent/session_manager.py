import json
import sys
from datetime import datetime, timedelta
from .constants import STATE_FILE, BOLD, DIM, GREEN, YELLOW, RED, SEP, c

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
        return c(RED, "past deadline")
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
    return c(YELLOW, text) if seconds < 300 else text

def _row(label: str, value: str) -> None:
    print(f"  {c(DIM, label + ':'): <16}  {value}")

def _header(title: str) -> None:
    print(SEP)
    print(f"  {c(BOLD, title)}")
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

    _header(f"{c(GREEN, '✓')} Session registered")
    _row("Request",  request)
    _row("Duration", f"{duration} min")
    _row("Started",  now.strftime("%a %b %d %Y · %H:%M:%S"))
    _row("Deadline", c(BOLD, deadline.strftime("%a %b %d %Y · %H:%M:%S")))
    print(SEP)

def cmd_dummy() -> None:
    cmd_add("Dummy session — testing omni-autonomous-agent", 60)

def cmd_status() -> None:
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
    _header(f"omni-autonomous-agent · {c(GREEN if active else RED, label)}")
    _row("Request",   state["request"])
    _row("Now",       now.strftime("%a %b %d %Y · %H:%M:%S"))
    _row("Started",   started.strftime("%a %b %d %Y · %H:%M:%S"))
    _row("Deadline",  deadline.strftime("%a %b %d %Y · %H:%M:%S"))
    _row("Duration",  f"{state['duration_minutes']} min")
    _row("Elapsed",   f"{int(elapsed // 60)}m {int(elapsed % 60)}s  ({pct_done}%)")
    _row("Remaining", _fmt_remaining(remaining))
    print(SEP)

def cmd_cancel() -> None:
    if not STATE_FILE.exists():
        print("  No active session to clear.")
        return
    STATE_FILE.unlink()
    print(f"{c(GREEN, '✓')} Session cancelled.")
