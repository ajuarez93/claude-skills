---
description: Auditoría de consumo de tokens del proyecto (cochinito). Primero diagnostica y propone; solo cambia algo con tu visto bueno.
---

Audit this project's token consumption. **Report first, change later:** run the checks below, show me a short plan of what you would create, change or delete (with before/after line counts where relevant), and wait for my OK before touching anything. Deleting from the global `~/.claude/settings.json` always needs its own explicit confirmation, after showing me the exact list. Before editing any settings file, back it up next to the original.

1. **Model and effort.** Check the session's default model and effort level (`/model`, `settings.json`). If it defaults to the most expensive model or a long-context variant, say so and recommend reserving it for work that justifies it (complex architecture, hard debugging). Don't quote prices from memory: tell me to check the current pricing for long-context models.

2. **CLAUDE.md: existence, completeness, size.** Locate every CLAUDE.md in the repo (root and subfolders, and each sub-repo in a multi-repo workspace).
   - Missing: propose one built from exploring that codebase. A concise CLAUDE.md is read once; without it every session re-discovers the same facts by reading files.
   - Present: spot-check 2-3 of its claims against the code and flag what's stale or missing.
   - Over ~250-300 lines: propose trimming narrative ("previously believed X, corrected") and repeated explanations, keeping anything expensive to re-investigate.
   - Structure to use, only the sections that apply, 100-250 lines: what this is (2-4 lines) → architecture and why (tables over prose) → key commands (one line each) → data/API map (compact tables) → gotchas (non-obvious constraints that would burn a session) → pointers to other docs instead of duplicating them.

3. **Output-truncating hook.** Check that a PostToolUse hook on Bash truncates huge command output (over ~200 lines or ~30k characters, keeping the head and the tail). This plugin ships one: `hooks/token-filter.py` (fail-open: on any error the original output passes through); it is NOT registered automatically. Locate it with `find ~/.claude/plugins -name token-filter.py | head -3` (or in a clone of the repo). If no such hook is registered, propose copying it to `~/.claude/hooks/` and registering it in `settings.json` with matcher `Bash`, and test it with simulated stdin first. Note its trade-off: a failure in the middle of a very long output is cut, so re-run narrowed when something looks missing.

4. **Permissions: global vs project.** Compare the global `~/.claude/settings.json` against each project's `.claude/settings.local.json` (each sub-repo in a multi-repo workspace).
   - Count the global `allow` rules. Thousands of accumulated one-off rules are a smell.
   - Identify rules specific to this project (paths, URLs, deploy commands) and propose moving them to the project file: copy first, show the list, delete from global only after I confirm.
   - Flag rules that belong to other projects or are single-use junk (temp scripts that no longer exist) and propose deleting them.
   - Standing rule: the global file keeps only generic reusable patterns (git, package manager, cloud CLI by subcommand); project-specific permissions go in the project's `settings.local.json`.

5. **Working scope.** Tell me which folder to open Claude Code from (repo root vs a subfolder), depending on whether typical work crosses sub-repos.

6. **Command output** is usually the largest avoidable cost (use `/context` to see what is actually filling the window). Apply and remind me of these:
   - `grep`: `-l` or `-c` when you don't need the lines; otherwise `-m N | head -30`. Never recursive without a filter.
   - `find`/`ls`: `| head -50` or `-maxdepth`.
   - `curl`: `-o /dev/null -w "%{http_code}"` if only the status matters; otherwise filter the JSON fields you need.
   - Big files and logs: never `cat` in full; `tail -50`, `grep`, or read with offset/limit.
   - `git`: `log --oneline -20`, `diff --stat` before a full diff, `status --short`.
   - Installers and builds: redirect to a temp file (the session's scratch directory if the environment provides one, otherwise the OS temp directory) and show only the tail.

7. **Session habits.** Suggest, in one short line and only when it applies, the command that fits the moment instead of defaulting to `/clear`:
   - `/clear` when I start an unrelated task; `/compact` when the session is heavy but I still need continuity; `/context` first when it's unclear what fills the window; `/model` when the default is a heavy model for work that doesn't need it.
   - Every turn resends the whole conversation, so cost grows with length; the right fix depends on whether continuity matters.
   - Prefer editing over rewriting files, and delegate broad searches to a subagent so its context doesn't pollute mine.
   - Track multi-step work in whatever task tracker I already use (an external tool or the built-in todo list); don't introduce a second one. Update it as steps finish.
   - Check that my global `~/.claude/CLAUDE.md` carries the habits I want applied everywhere, and keep that file short (it loads in every session).

At the end give me a short summary: what you found, what you changed, and what is left for me to decide. If this session was about fixing bugs and there's a pending-issues list, also list what remains unresolved, most blocking first.
