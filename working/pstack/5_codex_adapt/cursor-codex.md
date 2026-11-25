---
status: ready-for-human
---

# pstack in Codex

Apply these mappings in the affected agent, skill, playbook, or script. Remove the entry-point instruction to read `../../docs/harness/claude-code.md` once the mappings are in place. Script and reference paths below are relative to `poteto-mode/`.

## Tools

| Cursor | Codex |
| --- | --- |
| `Task` | Use `spawn_agent` when available. Otherwise run an independent brief with `codex exec -C <checkout> "<brief>"`. Collect each result before combining them. |
| `AskQuestion` | Use `request_user_input` when the current mode offers it. Otherwise ask in chat. A worker routes decisions back to its parent. |
| Open a todolist or copy playbook steps into it | Use `update_plan` when available. Otherwise keep the steps in chat and mark progress after each phase. |
| Run `/name` or "the **name** skill" | In a user prompt, write `$name`, for example `$open-a-pr`. Inside a workflow, open the named skill's `SKILL.md` and follow it. |
| Grep or glob files | Run `rg -n <pattern> <dir>` or `rg --files --hidden -g '<glob>' <dir>` in the shell. |

## Subagent fields

| Cursor | Codex |
| --- | --- |
| `subagent_type: generalPurpose` | Call `spawn_agent` with the brief. Omit `agent_type`. |
| `poteto-agent`, `comment-sicko` | Pass the role name only if `spawn_agent` accepts `agent_type` and the role is registered. Otherwise omit the field and put the body of `agents/<name>.md` in the brief. To register a role, use `.codex/agents/<name>.toml` or `~/.codex/agents/<name>.toml` with `name`, `description`, and `developer_instructions`. |
| `readonly: true` | Use `agent_type: "explorer"` if the schema offers that role, otherwise omit the field. In both cases specify "report only, make no changes." For a read-only filesystem sandbox, run `codex exec -s read-only -C <checkout> "<brief>"`. |
| `readonly: false`, agent mode | Omit `readonly`. Use the named role or its brief as above. The worker inherits the parent's sandbox and available MCP servers. |
| `environment: "local"` | Use the local checkout. For concurrent writers, run each in its own worktree. |
| `environment: "cloud"`, `cloud_base_branch: <b>` | Submit one task per worker with `codex cloud exec --env <env-id> --branch <pushed-branch> "<brief>"`. Omitting `--branch` selects the current branch. Include the expected SHA. |
| `run_in_background: true`, `is_background: true` | Omit the flag. Launch independent subagents before waiting. Keep their IDs and collect results with `wait_agent` when available. |
| `resume` | Start fresh for a new unit. For a live checkout or process that must stay with its owner, use `followup_task` or `send_input`, as offered, with the original agent ID. |

Begin each poteto-mode worker brief with `Read <absolute-worker-path>/worker.md before anything else.` Resolve the path on the worker's machine. Give a poteto-agent the absolute path to `poteto-mode/SKILL.md` there too.

## Models

| Cursor | Codex |
| --- | --- |
| `claude-opus-5-5-xhigh-fast`, `claude-opus-5-5-high-fast`, `claude-fable-5-2-high`, `gemini-4-neon-xhigh` | Select an available Codex `model` and pass `reasoning_effort` separately. The four starting efforts are `xhigh`, `high`, `high`, and `xhigh`, respectively. Drop the Cursor `-fast` suffix. |
| `model:` in `poteto-agent.md` | Leave the Codex role's `model` and `model_reasoning_effort` unset so each caller can select them. Values in a custom role file take precedence over spawn values. |
| `auto`, `inherit-parent` | Use the default role. Omit model and effort when it inherits both. If `agents.default_subagent_model` or `agents.default_subagent_reasoning_effort` changes the result, pass the parent's actual model and effort explicitly. |
| A panel or cross-vendor judge | Run one worker per confirmed seat. For a cross-vendor check, use an available model from another vendor. If none qualifies, report the missing judge or audit and keep that verdict open. |

An explicit spawn value overrides the corresponding `[agents]` default. Selecting a model without a spawn or configured effort uses that model's default effort. [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

## setup-pstack

| Cursor | Codex |
| --- | --- |
| Detect models and apply the budget | Use `/model` in the signed-in CLI to confirm the model and efforts. Start with the session model, e.g. `gpt-6.2-sol high` if offered. Apply the skill's budget ladder to each role. Ask for a supported pair if none fits. |
| `~/.cursor/rules/pstack-models.mdc` | Write `pstack-models.md` under `CODEX_HOME` (default `~/.codex`). Keep the defaults marker, budget, role labels and ordered lists. Store confirmed `<model> <effort>` pairs or the user's aliases, without MDC frontmatter. |
| Always apply the role rule | Read the file explicitly before selecting workers in poteto-mode, arena, interrogate and swarm. On a missing role, use the mapped skill default above. |

## Paths

| Cursor | Codex |
| --- | --- |
| `.cursor/skills/`, `~/.cursor/skills/` | Use `.agents/skills/` for project skills and `~/.agents/skills/` for personal skills. Preserve an existing skill's category. |
| Search `~/.cursor/plugins/` and compare plugin versions | Resolve the selected poteto-mode skill in the Codex skill catalog or the supplied checkout and pass its path. If several copies qualify, use the parent's selected copy. |
| `../../README.md`, `../../docs/guide/<page>` in poteto-help | Replace each link with its upstream URL under `https://github.com/cursor/plugins/blob/main/pstack/`, using `README.md` or the exact `docs/guide/<page>` path. Read the matching file under `sources/cursor-plugins/pstack/` in this workbench. |
| Cursor and Claude plugin installation in poteto-help | Replace the install instructions and the whole Claude compatibility paragraph. Link or copy each extracted `skills/<name>/` into `.agents/skills/` or `~/.agents/skills/`, keep `agents/` accessible for worker briefs, and invoke `$poteto-mode`. |
| Workspace `agent-transcripts/` | In the app, select chats for this checkout from `list_threads`, then page through those IDs with `read_thread`. In the CLI, run `codex resume` from this checkout to select a prior chat, or `codex resume <session-id>` for a known one. If history is unavailable, use a supplied transcript or handoff and identify the gap. |

## Cursor-only features

| Cursor | Codex |
| --- | --- |
| Webhook routine, `update_state`, `[routine]` wake, `SendToUser` secret request | Skip the Cursor provisioning and secret-card steps. Use a supplied endpoint and a server-side secret if available. Otherwise leave URL and key placeholders and report the live wake as unverified. |
| Bugbot | Triage existing PR threads with the forge using `references/bugbot-triage.md`. Skip a Bugbot-specific wait when the PR has no Bugbot check or comment. |
| Built-in PR tool, `draft: false` | If `git remote` lists no remote, run `git merge <work-branch>` in the intended local base checkout and report the result. Otherwise run `origin pr create --status open` when Origin resolves the repo, or `gh pr create` without `--draft`. |

## Playbooks and scripts

| Cursor | Codex |
| --- | --- |
| `/loop`, `/loop 1h` | Recheck the predicate in the current task after each change or watcher event. For the hourly audit, wait between checks and repeat until all owners finish. For shipping, run `scripts/watch-pr/watch-pr --queued-stack --stack-prs <n1,n2,...>` with the same bottom-to-top list on each restart. Stop at `COMPLETE` or the playbook's stop condition. |
| Custom Mode / Use as Mode | Start a new task with `$poteto-mode`. For a planning-only request, use `/plan` or the Multi-phase plan playbook. |
| `/create-skill` | Invoke `$skill-creator`. In automate-me, follow the draft with `$unslop` and the user's voice check. |
| `cursor-team-kit` · `/deslop` | Review `git diff <base>...HEAD` and pending changes before commit. Remove newly introduced redundant guards, casts and comments that conflict with nearby code. |
| `cursor-team-kit` · `control-cli`, `control-ui` | Drive the CLI in a PTY or use a project `verify-*` skill or browser driver on the live UI. Capture the output or screenshots at the requested SHA. Mark the live check blocked if no driver can reach it. |
| Cloud PR owner, verifier or pickup URL | Give each owner or independent verifier its own task. Record its ID, pushed branch, SHA and handoff where a replacement can read them. On pickup read `codex cloud status <id>` and `codex cloud diff <id>` alongside the pushed branch. For a Cursor URL, request the handoff or pushed branch if the trail is inaccessible. If cloud access is missing, use a separate local worktree where it meets the brief. Report any cloud-only check as blocked. |
| `scripts/worktree-audit.sh` · `LAST_CHAT`, `BUCKET` | Replace the Cursor transcript scan with a workspace-scoped Codex chat lookup if available. Without reliable data, skip the scan and set `last=unknown`. Keep `hold-wip` and `hold-open-pr` first, then set `bucket=review` for unknown activity before the `safe` branch. Keep each candidate until its path and worker worktrees have been checked against pinned and active chats. |
| `scripts/watch-pr/github.ts` · Bugbot recognition | Keep the forge identifiers. Match the first comment case-insensitively. A login containing `bugbot` qualifies. Login `cursor` also needs `bugbot`, `cursor_automation_id`, `agentic security review`, `description start`, or `severity` in the body. Count distinct `RUN_ID` or `CURSOR_AUTOMATION_ID` values, with one pass if all recognized threads lack keys. Triage other unresolved threads too. |
| `scripts/watch-pr/policy.ts` · pending review checks | Keep the case-insensitive check-name matches for `bugbot`, `security review`, `pr review automation`, and `review automation`. |
