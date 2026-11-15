# Claude Skills

A small, growing collection of [Claude Code](https://claude.com/claude-code) Skills and slash commands, built while working on real production projects. Each one exists because it earned its place in daily use, not as a demo.

**Contributions welcome.** Found a way to improve one of these, or want to propose a new one? Open a PR or an issue.

## What's a Skill vs. a Command?

Both extend Claude Code, but they trigger differently:

- **Skills** (`skills/<name>/SKILL.md`) load automatically when Claude recognizes that the task matches the skill's description. Good for standing guardrails and workflows that should apply whenever they're relevant.
- **Commands** (`commands/<name>.md`) are explicit: you type `/<name>` to run them. Good for a deliberate, on-demand audit.

## Available Skills

| Skill | What it does |
|---|---|
| [bisturi](skills/bisturi/) | *(the scalpel; formerly `preciso-economico`)* Coding discipline for changes of real scope: state assumptions, write the minimum, touch only what the task needs, define how it will be verified, check every caller before changing shared behavior, and keep command output bounded. Skips trivial work on purpose. |
| [orquestra-spec](skills/orquestra-spec/) | **Works with [Orquestra](https://orquestra.me)** and needs its MCP server (`npx orquestra-mcp setup`). A spec with acceptance criteria *before* building a big task, recorded inside Orquestra: a pre-verdict on the idea, the spec as a doc, a cold review by a subagent that has none of your context, your approval, and then a task created with checklist and per-criterion verifications. Also has a `drift` mode that checks a doc against the real code. In Spanish, since Orquestra is. |

## Available Commands

| Command | What it does |
|---|---|
| [cochinito](commands/cochinito.md) | *(the piggy bank; formerly `ahorra-tokens`)* Audits a project's token consumption: default model and effort, CLAUDE.md existence/size/freshness, an output-truncating hook, global vs. project permission hygiene, command-output habits and session habits. **Reports and proposes first; changes nothing without your OK**, and deleting from global settings needs its own confirmation. |

## Hooks

| Hook | What it does |
|---|---|
| [token-filter.py](hooks/token-filter.py) | PostToolUse hook for `Bash`: when a command prints more than ~200 lines or ~30k characters, keeps the first 120 and last 60 lines and says what was cut. Fail-open: on any error the original output passes through. Used by `cochinito`. |

## Installation

```bash
git clone https://github.com/ajuarez93/claude-skills.git
cd claude-skills

# Skills (global; for one project use <project>/.claude/skills/ instead)
cp -r skills/bisturi ~/.claude/skills/
cp -r skills/orquestra-spec ~/.claude/skills/   # only if you use Orquestra

# Command
cp commands/cochinito.md ~/.claude/commands/

# Hook (optional, `cochinito` can set it up for you)
mkdir -p ~/.claude/hooks && cp hooks/token-filter.py ~/.claude/hooks/
```

To register the hook, add it to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "python3 \"$HOME/.claude/hooks/token-filter.py\"", "timeout": 10 }] }
    ]
  }
}
```

Then work normally (`bisturi` and `orquestra-spec` load themselves when the task fits), or run `/cochinito` for the audit. To stay up to date, symlink instead of copying.

### Renamed

`preciso-economico` is now **`bisturi`** and `ahorra-tokens` is now **`cochinito`**. If you installed the old names, remove them and install the new ones.

## License

[MIT](LICENSE). Use these however you like.
