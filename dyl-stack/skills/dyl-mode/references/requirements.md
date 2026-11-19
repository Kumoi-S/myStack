# Requirements

dyl-stack uses skills and subagents from other collections. Check the dependencies your workflow needs. Use the sibling collections in this checkout or load them in your agent. If a required skill, subagent, or MCP connection is unavailable, name it before continuing.

| Collection or integration | Available when | Reach its files |
|---|---|---|
| `pstack` | `setup-pstack` is in your skill list | Most pstack skills are slash-only and hidden from the list. They sit beside `setup-pstack`: `<setup-pstack dir>/../poteto-mode/SKILL.md`, `../poteto-mode/playbooks/<name>.md`, `../principle-<name>/SKILL.md`, `../bro/SKILL.md`, `../unslop/SKILL.md`. |
| `cursor-team-kit` | `control-ui`, `verify-this`, and `deslop` are in your skill list | Their listed paths. |
| `thermos` | `thermo-nuclear-review-subagent` and `thermo-nuclear-code-quality-review-subagent` are available Task subagent types | Launch them by subagent type. |
| `figma` | `figma-design-to-code` is in your skill list and a Figma MCP tool call succeeds | Its listed path. |
