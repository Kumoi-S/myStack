# myStack

A collection of agent skills, CLI tools, and memory workflows. Each collection keeps its skills and supporting files together.

| Path | Contents |
| --- | --- |
| [.agents/skills/](.agents/skills/) | Project skills |
| [.agents/tools/](.agents/tools/) | Standalone tools, including [the model-list script](.agents/tools/get_avaliable_models.sh) |
| [pstack/](pstack/) | Engineering skills, playbooks, agents, and CLI scripts |
| [teaching/](teaching/) | Learning plans and retrospectives |
| [continual-learning/](continual-learning/) | Workflows for recording reusable preferences and workspace facts in `AGENTS.md` |
| [third_party/](third_party/) | Third-party skills and their licenses |

Other top-level collections follow the same `<collection>/skills/<skill>/SKILL.md` layout.

## Use a skill

For agents that discover project skills in `.agents/skills/`, open the repository and invoke a skill by name. To use a skill from another collection, open its `SKILL.md` directly or copy its entire directory into the skill location your agent reads. Keep its references and scripts alongside it. For workflows that use other skills or subagents, make those available to the same agent.

Some collections have skills with the same name as project skills, including `architect`, `tdd`, and `teach`. Use their full paths when choosing between them.

Individual skills may require specific CLIs, MCP servers, or agent features. See the skill's instructions for those requirements. The [pstack setup guide](pstack/docs/guide/01-setup.md) covers its workflow and links to Claude Code mappings.

## Validate pstack

Run these commands from the repository root using Node.js 22.

```sh
npm install --no-save --package-lock=false fast-check@4.5.3
node scripts/check-pstack-docs.mjs
node --disable-warning=ExperimentalWarning --test pstack/skills/*/scripts/test/*.test.ts
```

Rendering tests download pinned packages from npm. Live TLC integration tests require Java and `TLA2TOOLS` set to the path of `tla2tools.jar`.
