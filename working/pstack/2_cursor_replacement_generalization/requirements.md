# Stage 2 — Generalize platform-specific instructions

## Input and output

- Read the pstack snapshot in [`../1_extract/output/`](../1_extract/output/). Use the [Claude Code adapter](../1_extract/output/docs/harness/claude-code.md) as a review reference.
- Write the adapted pstack tree to `./output/`.

## Review and rewrite

1. Review the entire input tree for platform-specific instructions, including passages outside the examples below.
2. Use the Claude Code adapter as a reference when revising the original text, then remove the adapter from the output.

## Acceptance criteria

- Describe platform-specific tools and actions in terms of the capability the workflow requires. Keep exact names when they identify an upstream source, a fixture, or an external interface the workflow uses.
- Keep the original headings, step order, and wording wherever possible. Rewrite a whole instruction when several platform-specific fields together express one action. Preserve its action, scope, permissions, timing, concurrency, handoff, and expected result. Keep explanations and fallback steps limited to those in the original workflow.
- Each local link in an edited file still points to the intended file.

## Terms

Use these terms in prose where the source describes the capability in the corresponding context.

| Context | Source term | Host-neutral term |
| --- | --- | --- |
| Delegation | `Task`, `Agent` | subagent |
| Role selection | `subagent_type` | subagent role |
| General-purpose work | `generalPurpose`, `general-purpose` | general-purpose subagent |
| Poteto-mode delegation | `poteto-agent`, `pstack:poteto-agent` | poteto-mode subagent |
| Comment review | `comment-sicko`, `pstack:comment-sicko` | comment-sicko  subagent |
| Read-only inspection | `readonly: true`, `Explore` | read-only subagent |
| MCP access | `readonly: false`, agent mode | --subagent with MCP access-- |
| Remote execution | `environment: "cloud"`, Cursor cloud agent, `/in-cloud` | remote worker |
| Local execution | `environment: "local"` | local worker |
| Worker checkout | `cloud_base_branch` | starting branch |
| Checkout isolation | `isolation: "worktree"` | separate checkout |
| Background execution | `run_in_background: true`, `is_background: true` | background execution |
| Worker continuity | `resume` | subagent resumption |
| Worker brief | `file_attachments`, file pointers | referenced file paths |
| User choice | `AskQuestion`, `AskUserQuestion` | structured user choice |
| Task tracking | `todolist`, `TodoWrite` | task checklist |
| Text search | `Grep` | grep |
| File discovery | `Glob` | glob |
| File access | `Read` | read |
| Command execution | `Bash` | shell command |
| Bundled skill invocation | `Skill`, `/<name>`, `/pstack:<name>`, slash menu | call <name> skill    |
| Session mode | Option+Enter, Alt+Enter, Use as Mode, Custom Modes | session mode |
| Model discovery | Cursor model API or CLI | session model inventory |
| Model selection | `model`, `model:` | selected model |
| Reasoning | `effort` | reasoning level |
| Model inheritance | `auto`, `inherit-parent` | parent session model |
| Role settings | `pstack-models.mdc`, `~/.cursor/rules/pstack-models.mdc`, `~/.claude/rules/pstack-models.md` | pstack model settings |
| Project skills | `.cursor/skills/`, `.claude/skills/` | project skill directory |
| Verification skill lookup | `.cursor/skills/verify-<app>/`, `.cursor/skills/verify-*/` | project verification skill directories |
| Mode skill lookup | `.cursor/skills/**/*-mode/SKILL.md`, `~/.cursor/skills/*-mode/SKILL.md`, `.cursor/skills/<handle>/<handle>-mode/SKILL.md` | project and user mode skill definitions |
| User skills | `~/.cursor/skills/`, `~/.claude/skills/` | ~/.agents/skills/ |
| Project instructions | `.cursor/rules/*.mdc`, `CLAUDE.md`, `AGENTS.md` | .agents/AGENTS.md |
| Bundled file lookup | `~/.cursor/plugins/`, `~/.claude/plugins/`, `plugins/cache/` | active pstack installation |
| Bundled file lookup | `https://github.com/cursor/plugins/blob/main/pstack/<path>` | corresponding bundled pstack file |
| Workspace history | `~/.cursor/projects/<slug>/agent-transcripts/`, `~/.claude/projects/<slug>/` | active workspace transcript directory |
| Transcript lookup | `agent-transcripts/<uuid>/<uuid>.jsonl`, `<session>.jsonl`, `<session>/subagents/` | session transcript or subagent transcripts |
| Checkout lookup | `.cursor/worktrees/myrepo/x` | repository worktree |
| Worker grouping | Cursor Project, Project worker | worker group, worker |
| Worker tracking | cloud-agent URL, cloud-agent dashboard | worker handle, worker status view |
| Active-work lookup | Cursor sidebar, pinned or active chats | active and pinned workspace sessions |
| Disk cleanup | `~/Library/Application Support/Cursor`, `state.vscdb.backup`, `snapshots/roots/<root>` | host cache locations |
| Plugin installation | `/add-plugin pstack`, `/plugin marketplace add cursor/plugins`, `/plugin install pstack@cursor-plugins` | pstack installation |
| Plugin update | `claude plugin update pstack@cursor-plugins` | pstack update |
| Planning | Cursor Agents Window or CLI in Plan Mode | planning session |
| Scheduled audits | `/loop`, `/loop 1h`, routine wake, heartbeat | periodic audit |
| Run monitoring | `/autopilot`, built-in babysit | run monitoring |
| Worker coordination | `/orchestrate` | delegated work coordination |
| Skill authoring | `/create-skill` | skill-authoring workflow |
| Diff cleanup | `cursor-team-kit` `/deslop` | diff cleanup pass |
| UI and CLI verification | `cursor-team-kit` `control-ui`, `control-cli` | real UI or CLI verification |
| PR opening | built-in PR tool | session PR tool |
| Automated PR review | Bugbot check | automated PR review check |
| Automation setup | Cursor Automations, routine | automation service, scheduled or event-triggered automation |
| Automation settings | Routines list, routine panel, agent header | automation settings |
| Webhook credential handoff | `SendToUser` secret request | secure credential handoff |

## Examples

| Source | Original | Replacement |
| --- | --- | --- |
| [How](../1_extract/output/skills/how/SKILL.md) | Spawn one Task subagent with `subagent_type: generalPurpose` and `readonly: true` that explores and explains in one pass. Give it the user's question and this brief: | Give one general-purpose subagent the user's question and this brief for a single read-only pass that explores and explains the code. |
| [Swarm](../1_extract/output/skills/swarm/SKILL.md) | Spawn all N workers in one message with `subagent_type: generalPurpose`, `environment: "cloud"`, `run_in_background: true`, and the step 3 model, left unset for `auto` or `inherit-parent`. Use `environment: "local"` only when the worker needs access to something on the user's computer. | Start all N general-purpose workers together in the background on remote machines. Use the model selected in step 3, or the parent session's model for `auto` or `inherit-parent`. Run a worker locally only when it needs access to something on the user's computer. |
| [Recall](../1_extract/output/skills/recall/SKILL.md) | Spawn one investigator subagent per source, in agent mode because readonly strips MCP access, and ask each "what's the current state, what's been tried and didn't hold, and what are users still reporting". Run them in parallel with the chat-history mining. | Give one investigator subagent per source access to the session's MCP servers and ask each "what's the current state, what's been tried and didn't hold, and what are users still reporting". Run them in parallel with the chat-history mining. |
| [Automate me](../1_extract/output/skills/automate-me/SKILL.md) | Locate the active workspace's transcripts before fanning out. The system prompt names the workspace's `agent-transcripts/` directory. Use only that path. | Locate the active workspace's transcripts before fanning out. Use only the chat history for that workspace. |
| [Reframe](../1_extract/output/README.md) | runs only when you type `/reframe`. | runs only when you explicitly invoke the `reframe` skill. |
| [Autopilot](../1_extract/output/skills/poteto-mode/playbooks/autopilot-full.md) | On the operator's go, arm `/loop 1h` to audit until no delegated work is left, because long runs drift and agents stall silently. | On the operator's go, audit once an hour until no delegated work is left, because long runs drift and agents stall silently. |
| [Opening a PR](../1_extract/output/skills/poteto-mode/playbooks/opening-a-pr.md) | Open PRs ready, through the run's PR tool with `draft: false`. Without one, use `gh pr create` without `--draft`, or `origin pr create --status open` when Origin's CLI resolves the repository. | Use the session's PR tool to open a ready-for-review PR. If that tool is unavailable, use `gh pr create` to open it ready for review, or use `origin pr create --status open` when Origin's CLI resolves the repository. |
