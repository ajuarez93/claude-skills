# Claude Skills

A small, growing collection of [Claude Code](https://claude.com/claude-code) Skills and slash commands, built while working on real production projects. Each one exists because it earned its place in daily use, not as a demo.

**Contributions welcome.** Found a way to improve one of these, or want to propose a new one? Open a PR or an issue.

## What's a Skill vs. a Command?

Both are ways to extend Claude Code, but they trigger differently:

- **Skills** (`skills/<name>/SKILL.md`) are loaded automatically when Claude recognizes the task matches the skill's description — no explicit invocation needed. Good for standing guardrails/conventions that should apply whenever they're relevant.
- **Commands** (`commands/<name>.md`) are explicit — you type `/<name>` to run them. Good for a deliberate, on-demand audit or workflow you want to trigger yourself.

## Available Skills

| Skill | Description |
|---|---|
| [preciso-economico](skills/preciso-economico/) | Coding-discipline and token-economy guardrails for any non-trivial implementation, review, or refactor task — surface assumptions instead of guessing, avoid overengineering, keep edits surgical, define verifiable success criteria, and bound tool output/context growth. |

## Available Commands

| Command | Description |
|---|---|
| [ahorra-tokens](commands/ahorra-tokens.md) | Audits and optimizes a project's token consumption end to end: default model, CLAUDE.md existence/size/freshness, an output-truncating hook for noisy Bash commands, project vs. global permission hygiene, and session habits (when to `/clear`/`/compact`/`/model`, TodoWrite discipline). Creates what's missing directly; only asks before deleting anything from the global `~/.claude/settings.json`. |

## Installation

### Skills

```bash
# Global (all your projects)
cp -r skills/preciso-economico ~/.claude/skills/

# Project-only
cp -r skills/preciso-economico /path/to/your/project/.claude/skills/
```

### Commands

```bash
# Global (all your projects)
cp commands/ahorra-tokens.md ~/.claude/commands/

# Project-only
cp commands/ahorra-tokens.md /path/to/your/project/.claude/commands/
```

Then, inside Claude Code, run `/ahorra-tokens` to trigger the command manually, or just work normally — `preciso-economico` loads itself when the task fits.

### Via git (to stay up to date)

```bash
git clone https://github.com/ajuarez93/claude-skills.git
ln -s "$(pwd)/claude-skills/skills/preciso-economico" ~/.claude/skills/preciso-economico
ln -s "$(pwd)/claude-skills/commands/ahorra-tokens.md" ~/.claude/commands/ahorra-tokens.md
```

## License

[MIT](LICENSE). Use these however you like.
