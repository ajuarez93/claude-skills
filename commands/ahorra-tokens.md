---
description: Audit and optimize the current project's token consumption
---

Audit and optimize this project's token consumption. CREATE items (missing CLAUDE.md, missing
settings.local.json, missing hook) directly, no need to ask first — report what you created at
the end. The only thing that always needs my confirmation before it happens is DELETING
anything from the global ~/.claude/settings.json (item 4).

1. MODEL: check the session's default model (/model or settings.json). If it's set to Opus
   or has the [1m] modifier, recommend switching the default to Sonnet and using Opus only
   when the task justifies it (complex architecture, hard debugging). The [1m] modifier
   doubles input pricing once the conversation exceeds 200k tokens.

2. CLAUDE.md — existence, completeness, and size. Locate every CLAUDE.md in the repo
   (root and subfolders):
   - If a repo (or sub-repo in a multi-repo workspace) has NO CLAUDE.md, CREATE one by
     exploring that codebase. A good CLAUDE.md pays for itself: without it, every session
     re-discovers the same facts by reading files (far more expensive than loading a
     concise doc once).
   - If a CLAUDE.md exists, verify it is COMPLETE and CURRENT: does it cover what the
     project is, how it's structured, and the non-obvious facts? Spot-check 2-3 claims
     against the actual code; flag and fix anything stale or missing.
   - If any exceeds ~250-300 lines, trim self-referential narrative ("previously believed
     X, corrected", "confirmed by comparing A with B", repeated explanations of the same
     fact) without losing content that is expensive to re-investigate.
   - Token-efficient structure to use when creating or restructuring (in this order, only
     the sections that apply, target 100-250 lines):
     * What this is: 2-4 lines — product, stack, role of this repo in the ecosystem.
     * Architecture: how code is organized and WHY, only what's not obvious from folder
       names. Prefer tables and lists over prose.
     * Key commands: build, test, run, deploy — exact commands, one line each.
     * Data/API map: tables, endpoints, env vars — as compact tables, not paragraphs.
     * Gotchas: non-obvious constraints that would burn a session to rediscover
       (state machines, implicit schemas, deploy quirks, naming traps).
     * Pointers: link to STYLE.md/TODO.md/other docs instead of duplicating them.
   - Show me before/after line counts for anything you create or change.

3. SAVINGS INFRASTRUCTURE — verify it exists, create what's missing:
   - Output-filter hook: check that ~/.claude/hooks/token-filter.py exists and that
     ~/.claude/settings.json registers it as a PostToolUse hook on Bash. If either is
     missing, create them: a fail-open Python script (no dependencies) that reads the hook
     JSON from stdin and, when a Bash tool_output exceeds 200 lines or 30k chars, replies
     with {"hookSpecificOutput": {"hookEventName": "PostToolUse", "updatedToolOutput":
     "<first 120 lines + truncation marker + last 60 lines>"}}; on any exception it must
     exit 0 silently so the original output passes through. Register it with matcher
     "Bash" and timeout 10. Test it with simulated stdin before registering.
   - Project settings: if this is a multi-repo workspace (root has no CLAUDE.md/.git of its
     own but contains several sub-repos, as in item 2), check EACH sub-repo — if a sub-repo's
     .claude/settings.local.json does NOT exist, CREATE it there with the base structure
     {"permissions": {"allow": []}}. If it's a single repo, just check its own root.

4. PERMISSIONS — global vs project: compare ~/.claude/settings.json (global, shared across
   ALL my projects) against this project's .claude/settings.local.json — or, in a multi-repo
   workspace, against EACH sub-repo's settings.local.json (same scope as item 3).
   - Identify rules in the global file that are specific to THIS project (paths in this
     repo, its API/Lambda URLs, its deploy commands) and MOVE them to the project's
     settings.local.json: copy them to the local file first, show me the list, and only
     delete them from the global file after I confirm.
   - Also flag global rules that belong to OTHER projects or are single-use junk (absolute
     paths of another repo, one-off URLs/commands, scripts in /tmp or scratchpads that no
     longer exist) and propose deleting them. Never delete anything from the global file
     without my confirmation.
   - Standing rule: the global file only keeps generic reusable patterns (git, npm, docker,
     aws by subcommand); every new project-specific permission goes into that project's
     settings.local.json, not the global file.

5. WORKING SCOPE: tell me which folder I should open Claude Code from for this project
   (repo root vs. a subfolder) based on whether typical work crosses multiple sub-repos.

6. COMMAND OUTPUT — the #1 source of waste in real sessions (public measurements: unfiltered
   grep/find/curl/cat is ~85-99% noise; a single unbounded grep can cost hundreds of
   thousands of tokens). ALWAYS apply these in this session and remind me of them:
   - grep: use -l (filenames only) or -c (count only) when you don't need the lines; if you
     do, bound with -m N and | head -30. Never recursive grep without a filter.
   - find/ls: always | head -50, or use -maxdepth.
   - curl to APIs: discard the body with -o /dev/null -w "%{http_code}" if you only check
     status; if you need the JSON, filter only the relevant fields with | python3 -c / jq.
   - cat on large files / logs / builds: never in full — tail -50, grep for the relevant
     pattern, or Read with offset/limit.
   - git: log --oneline -20, diff --stat before full diff, status --short.
   - Installers/builds (npm install, pip, docker build): redirect to a file and show only
     the tail: `command > /tmp/out.log 2>&1; tail -20 /tmp/out.log`.

7. SESSION HABITS — apply during this session and every future one in this project:
   - PROACTIVELY SUGGEST whichever command best reduces cost for the situation (one short
     line, without interrupting the work) — don't default to /clear every time:
     * /clear — I'm starting a task unrelated to the conversation so far (full reset, no
       continuity needed).
     * /compact — the session is heavy (long transcript, many accumulated tool
       outputs/processes, slow responses) but I still need mid-task continuity.
     * /context — before recommending /clear or /compact, or whenever it's unclear what's
       filling the window, check /context first so the suggestion is informed rather than
       reflexive.
     * /model — the session default is Opus (or has [1m]) for work that doesn't need it;
       recommend dropping to Sonnet (see item 1).
     Rationale: every turn resends the ENTIRE conversation — cost grows quadratically — but
     the fix depends on whether continuity matters and what's actually filling the context.
   - Also remind me in one line, when relevant: prefer Edit over rewriting whole files, and
     delegate broad searches to an Explore subagent (its context doesn't pollute mine).
   - ALWAYS start non-trivial work with a TodoWrite list of the steps, and keep it updated
     as steps complete (mark items done as soon as they're done, don't batch). Rationale:
     an explicit TODO avoids re-deriving "what was I doing" from the transcript, which is
     itself a source of wasted tokens on long sessions.
   - Check that ~/.claude/CLAUDE.md contains BOTH of the above rules (command-suggestion,
     TODO-tracking) so they apply globally; add whichever is missing (keep that file under
     ~10 lines — it loads in every session).

At the end give me a short summary: what you created, what you changed, what's left for me
to decide. If this session was about fixing errors/bugs and there's a TODO or pending-issues
list, also list which items remain unresolved, ordered by urgency (most blocking/severe
first).
