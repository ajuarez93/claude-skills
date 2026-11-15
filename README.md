# Claude Skills

A small, growing collection of [Claude Code](https://claude.com/claude-code) skills and slash commands, built while working on real production projects. Each one exists because it earned its place in daily use, not as a demo.

This repo is a **plugin marketplace**: each tool is its own plugin, so you install only what you want.

**Contributions welcome.** Found a way to improve one of these, or want to propose a new one? Open a PR or an issue.

## Plugins

| Plugin | What it does |
|---|---|
| [bisturi](plugins/bisturi/) | *(the scalpel; formerly `preciso-economico`)* A skill with coding discipline for changes of real scope: state assumptions, write the minimum, touch only what the task needs, define how it will be verified, check every caller before changing shared behavior, and keep command output bounded. Skips trivial work on purpose. |
| [cochinito](plugins/cochinito/) | *(the piggy bank; formerly `ahorra-tokens`)* A command that audits a project's token consumption: default model and effort, CLAUDE.md existence/size/freshness, global vs. project permission hygiene, command-output habits and session habits. **Reports and proposes first; changes nothing without your OK**, and deleting from global settings needs its own confirmation. Ships an optional hook, `token-filter.py`, that truncates huge Bash output (keeps the first 120 and last 60 lines; fail-open). The hook is **not** registered automatically. |

Skills that work with [Orquestra](https://orquestra.me) live in their own repo: [orquestra-skills](https://github.com/ajuarez93/orquestra-skills).

## Install as a plugin (recommended)

```bash
claude plugin marketplace add ajuarez93/claude-skills
claude plugin install bisturi@claude-skills
claude plugin install cochinito@claude-skills
```

Or inside a session: `/plugin marketplace add ajuarez93/claude-skills`, then `/plugin install bisturi@claude-skills`.

- `bisturi` loads itself when the task fits its description.
- Run the audit with `/cochinito:cochinito` (plugin commands are prefixed with the plugin name).
- Third-party marketplaces don't auto-update by default: run `claude plugin update bisturi@claude-skills`, or enable auto-update.

## Install by hand

If you prefer plain files (the commands are then un-prefixed, e.g. `/cochinito`):

```bash
git clone https://github.com/ajuarez93/claude-skills.git
cd claude-skills

# Skill (global; for one project use <project>/.claude/skills/)
cp -r plugins/bisturi/skills/bisturi ~/.claude/skills/

# Command
cp plugins/cochinito/commands/cochinito.md ~/.claude/commands/
```

To keep them up to date, symlink instead of copying.

## The optional hook

`cochinito` can set it up for you. By hand:

```bash
mkdir -p ~/.claude/hooks && cp plugins/cochinito/hooks/token-filter.py ~/.claude/hooks/
```

and register it in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "python3 \"$HOME/.claude/hooks/token-filter.py\"", "timeout": 10 }] }
    ]
  }
}
```

Trade-off: a failure in the middle of a very long output gets cut; re-run narrowed with `grep`, `head` or `tail` when something looks missing.

### Renamed

`preciso-economico` is now **`bisturi`** and `ahorra-tokens` is now **`cochinito`**. If you installed the old names, remove them and install the new ones.

## License

[MIT](LICENSE). Use these however you like.
