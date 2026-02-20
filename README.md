# omni-autonomous-agent

Lets an AI agent work non-stop for a fixed duration, then report back, no interruptions, no hand-holding.

---

## Setup

```bash
python3 main.py --install
```

Installs `omni-autonomous-agent` to `~/.local/bin`. Run once, use anywhere.

---

## Commands

| Command | Description |
|---|---|
| `--add -R "<request>" -D <minutes>` | Register a new session |
| `--status` | Show current session state |
| `--cancel` | Cancel the active session |
| `--install` | Install to PATH |

---

## Usage

```bash
# Start a 2-hour session
omni-autonomous-agent --add -R "Refactor the auth module and write unit tests" -D 120

# Check progress
omni-autonomous-agent --status

# Cancel early
omni-autonomous-agent --cancel
```

---

## How it works

1. User registers a task with `--add`
2. Agent reads `--status` to get the deadline
3. Agent works continuously until the deadline
4. Agent delivers a structured report when time is up

State is stored at `~/.config/omni-agent/state.json`.

## Support

If you liked omni-autonomous-agent, please consider starring the repo, and dropping me a follow for more stuff like this :)  
It takes less than a minute and will help a lot ❤️  

If you want to show extra love, consider *[buying me a coffee](https://buymeacoffee.com/clankert800)*! ☕

![alt text](https://imgs.search.brave.com/FolmlC7tneei1JY_QhD9teOLwsU3rivglA3z2wWgJL8/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93aG9w/LmNvbS9ibG9nL2Nv/bnRlbnQvaW1hZ2Vz/L3NpemUvdzIwMDAv/MjAyNC8wNi9XaGF0/LWlzLUJ1eS1NZS1h/LUNvZmZlZS53ZWJw)