import os
import stat
import sys
from pathlib import Path
from .constants import GREEN, YELLOW, BOLD, SEP, c

def _row(label: str, value: str) -> None:
    print(f"  {c(DIM, label + ':'): <16}  {value}")

def _header(title: str) -> None:
    print(SEP)
    print(f"  {c(BOLD, title)}")
    print(SEP)

def cmd_install() -> None:
    script = Path(__file__).resolve().parent.parent / "main.py"
    
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

    _header(f"{c(GREEN, '✓')} Installed")
    _row("Source", str(script))
    _row("Link",   str(dest))
    print()
    print(f"  Run {c(BOLD, 'omni-autonomous-agent --status')} to verify.")

    path_dirs = os.environ.get("PATH", "").split(":")
    if str(target_dir) not in path_dirs:
        print()
        print(f"  {c(YELLOW, '!')}"
              f" {target_dir} is not in your PATH. Add it:")
        print(f'    export PATH="{target_dir}:$PATH"')
    print(SEP)
