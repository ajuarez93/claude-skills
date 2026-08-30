---
name: preciso-economico
description: Coding-discipline and token-economy guardrails for any non-trivial implementation, review, or refactor task — surface assumptions instead of guessing, avoid overengineering, keep edits surgical, define verifiable success criteria, and bound tool output/context growth. Load before implementing or reviewing code changes of meaningful scope.
version: 0.1.0
---

# Preciso y Económico

Two goals reinforced together: fewer wrong or wasted turns (precision) and lower token
spend (economy) — they compound, since a wrong turn is also a wasted one.

## 1. Think before coding

- State assumptions explicitly. If genuinely uncertain, ask instead of guessing.
- If multiple valid interpretations exist, name them — don't silently pick one.
- If a simpler approach exists, say so before implementing the complex one.
- Stop and name what's confusing rather than coding through it.

## 2. Simplicity first

- Minimum code that solves the problem — no speculative features, config, or
  abstractions beyond what was asked.
- No error handling for scenarios that can't happen.
- If a first draft could be a quarter of its size, rewrite it before showing it.

## 3. Surgical changes

- Touch only what the task requires; don't refactor or reformat adjacent code.
- Match existing style even when you'd choose differently.
- Clean up only orphans your own change created — mention pre-existing dead code,
  don't remove it unasked.

## 4. Goal-driven execution

- Turn vague asks into verifiable steps: "fix the bug" → reproduce with a failing
  check, then make it pass.
- For multi-step work, state a short plan as step → verify pairs before executing.

## 5. Token economy (session-wide)

- Bound all shell output: `grep -l`/`-c` or `-m N | head` when full matches aren't
  needed; `find`/`ls` with `-maxdepth` or `| head`; `curl -o /dev/null -w '%{http_code}'`
  when only status matters; never `cat` a full log — `tail` or `grep` for the relevant
  part.
- Prefer Edit over rewriting whole files; delegate broad or exploratory search to an
  Explore subagent so its context doesn't pollute the main conversation.
- Suggest whichever session command fits — `/clear` (unrelated new task), `/compact`
  (heavy session, still need continuity), `/context` (unclear what's filling the
  window), `/model` (drop Opus→Sonnet when the task doesn't need it) — one short line,
  don't default to `/clear` reflexively.
- Track multi-step work with TodoWrite, updated as steps complete — avoids re-deriving
  "what was I doing" from the transcript on long sessions.

**Signal these guardrails are working:** fewer unnecessary diffs, fewer overcomplicated
rewrites, clarifying questions land before mistakes instead of after, and shell/tool
output stays bounded.
