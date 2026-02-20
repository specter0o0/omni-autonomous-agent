---
name: omni-autonomous-agent
description: Makes the AI agent autonomous and able to work for a fixed duration without interruptions. Use the skill when the user asks you to work autonomously (EG. Work overnight, I'll be gone for few hours, keep working until I get back, etc.)
---

# omni-autonomous-agent

Autonomous work mode. You execute a task continuously for a fixed duration with zero
interruptions, then report back.

---

## One-time install

```bash
python3 helper.py --install
```

## Activation (MANDATORY FIRST STEP)

**Before anything else**, you MUST register the task by running:

```bash
omni-autonomous-agent --add -R "<user_request_verbatim>" -D <duration_in_minutes>
```

This is non-negotiable. Do not proceed to any other step until this command has
been executed and returns successfully. Do not simulate or skip this step.

After `--add` succeeds, run:

```bash
omni-autonomous-agent --status
```

Read the output carefully. It tells you:
- Current date and time
- Deadline (when you must stop and conclude)
- Time remaining
- The registered request

When you notice the deadline is near, start concluding your work and prepare a report.

---

## Execution Rules

### What you MUST do
- Work **continuously** from activation until the deadline
- Make **real, measurable progress** every step — no filler, no stalling
- Track your own time by checking the system clock periodically
- Begin conclusion and wrap-up **a few minutes before** the deadline
- Deliver a structured report immediately after the deadline passes

### What you MUST NOT do
| Forbidden | Why |
|-----------|-----|
| `sleep` / `time.sleep` / any delay command | Wastes allotted work time |
| Pausing to ask clarifying questions | Defeats autonomous mode |
| Skipping steps "to save time" | Quality floor must be maintained |
| Assuming the task is done without verification | Always validate outputs |
| Stopping early | Use all available time productively |

> ⚠️ `sleep` and equivalent delay calls are **disabled** during an active task.
> Any attempt to introduce artificial waiting will be treated as a failure.

---

## Time Management

```
[Start] → check --status → internalize deadline
  ↓
[Work loop] → real work → periodic clock checks → adjust pace
  ↓
[few minutes before deadline] → begin conclusion
  ↓
[Just after deadline] → deliver report
```

Check the clock at natural breakpoints (after each major subtask). If you are running
behind, compress scope — never compress quality.

---

## End-of-Session Report

When the deadline is reached, deliver a structured report:

```
## Autonomous Session Report

**Request:** <original request>
**Duration:** <planned> → <actual time worked>
**Completed at:** <timestamp>

### What was done
<concrete summary of every action taken>

### Outputs
<list all files created, modified, commands run, results produced>

### Status
<COMPLETE | PARTIAL — with honest reason if partial>

### Blockers / Notes
<anything the user needs to know>
```

Do not omit sections. Be factual and concise.

---

## Status Command

At any point (within or outside a session), you can check the current session state:

```bash
omni-autonomous-agent --status
```

Output includes: current time, work deadline, time remaining, and the active request.
Use this to orient yourself during long sessions or after any tool call that may take
significant time.

---

## Notes

- When user uses this skill, 99% of the time they're away, so do not try to communicate with them, you must work with what you have, be creative, and go all-in!
- To cancel a session mid-way (e.g. user returns early), run `omni-autonomous-agent --cancel`. Stop all work immediately and skip the end-of-session report. NOTE: do this only if user explicitly asks you for a report immediately.
- Scope management is your responsibility. If the task is larger than the time budget, prioritize the highest-value work and note what you couldn't finish in your report.