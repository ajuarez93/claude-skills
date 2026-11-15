#!/usr/bin/env python3
"""PostToolUse hook: truncates huge Bash output before it enters the model context.

Fail-open: on any error or unexpected format it exits 0 without emitting JSON,
so Claude Code uses the original output untouched.

Register it in ~/.claude/settings.json under hooks.PostToolUse with matcher "Bash".
"""
import json
import sys

MAX_LINES = 200        # at or below this, nothing is touched
MAX_CHARS = 30_000     # alternative cap for outputs with few but enormous lines
HEAD_LINES = 120       # leading lines kept
TAIL_LINES = 60        # trailing lines kept (errors are usually at the end)


def extract_text(data):
    out = data.get("tool_output")
    if isinstance(out, dict):
        return out.get("text") or out.get("stdout") or ""
    if isinstance(out, str):
        return out
    resp = data.get("tool_response")
    if isinstance(resp, dict):
        return resp.get("text") or resp.get("stdout") or ""
    if isinstance(resp, str):
        return resp
    return ""


def main():
    data = json.load(sys.stdin)
    if data.get("hook_event_name") != "PostToolUse" or data.get("tool_name") != "Bash":
        return
    text = extract_text(data)
    if not text:
        return

    lines = text.splitlines()
    n_lines, n_chars = len(lines), len(text)
    if n_lines <= MAX_LINES and n_chars <= MAX_CHARS:
        return

    head = lines[:HEAD_LINES]
    tail = lines[-TAIL_LINES:] if n_lines > HEAD_LINES + TAIL_LINES else []
    # extra cap in case the kept lines are still huge (minified JSON, etc.)
    head_txt = "\n".join(head)[: MAX_CHARS * 2 // 3]
    tail_txt = "\n".join(tail)[-(MAX_CHARS // 3):]

    marker = (
        f"\n[token-filter] Output truncated ({n_lines} lines / {n_chars} chars). "
        f"Showing the first {HEAD_LINES} and last {TAIL_LINES} lines. "
        "If you need what was omitted, re-run narrowed with grep/head/tail.\n"
    )
    truncated = head_txt + marker + tail_txt if tail_txt else head_txt + marker

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "updatedToolOutput": truncated,
        }
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # fail-open: never break the session because of the filter
    sys.exit(0)
