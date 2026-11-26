---
status: Unqualified
---

# pstack in Codex

Apply these mappings at the affected call sites. Once applied, remove the skill entry-point instruction to load `../../docs/harness/claude-code.md`. The extracted package contains `agents/` and `skills/`.

## Tools

| Cursor | Codex |
| --- | --- |
| `Task` | `spawn_agent`<br>If native delegation is unavailable and CLI workers are permitted, use `codex exec -C "<checkout>" "<brief>"`. For an Arena file candidate in a trusted non-Git directory use `codex exec --skip-git-repo-check -s workspace-write -C "<candidate-dir>" "<brief>"`. |
| Launch all workers in one message | Dispatch the independent briefs before waiting, within the session's concurrency limit. |
| Wait for workers and collect their results | Wait on the returned agent IDs with the session's wait tool (such as `wait_agent`) and read each final response.<br>For CLI workers, collect the exit status and final response. For Cloud, wait for terminal status with `codex cloud status <id>`, then read the report from the task record or shared handoff. Mark a missing report unverified. |
| `AskQuestion` | `request_user_input`<br>If the mode or schema cannot express the question, ask in chat with all original options and allow multiple selections when requested. |
| Open or update the todolist | `update_plan` when available, otherwise a checklist in chat. |
| User types `/name` for an installed skill | `$name`. Use the actual installed name, including project skills such as `$verify-notes`. |
| A workflow calls `/name` or “the **name** skill” | Read and follow the named skill's `SKILL.md`. |
| Search file contents | `rg -n -e <pattern> <directory>` |
| Match file names | `rg --files --hidden -g '<glob>' <directory>` |

## Subagent fields

| Cursor | Codex |
| --- | --- |
| `subagent_type: generalPurpose` | Default agent. Omit the optional role selector. |
| `poteto-agent`, `comment-sicko` | Pass the registered name as `agent_type` where supported. Otherwise give the default worker the extracted `agents/<name>.md` body.<br>To register an extracted role, put its name, description and body in `name`, `description` and `developer_instructions` in `.codex/agents/<name>.toml` or `~/.codex/agents/<name>.toml`. [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) |
| `model:` in the poteto-agent role | Leave the Codex role's `model` and `model_reasoning_effort` unset so the caller can select them. |
| `readonly: true` | Request a report-only worker. For an enforced read-only CLI sandbox use `codex exec -s read-only`. |
| Agent mode with MCP access | Select a worker with the required MCP connector enabled. |
| `environment: "cloud"` | `codex cloud exec --env <env-id> --branch <pushed-baseline> "<brief>"`<br>If hosting is unavailable, use a local worktree only where it satisfies the brief. |
| `cloud_base_branch: <b>` | `--branch <b>`<br>Pass the specified pushed branch. If the field is absent, pass the playbook's pushed baseline explicitly (usually the repository default for Swarm, trunk for Autopilot-full). Omitting the CLI flag selects the current branch. |
| `environment: "local"` | Use the local checkout. |
| `run_in_background: true`, `is_background: true` | Omit the flag. Native dispatch returns a worker ID. |
| Resume a delegate with live state | Send the follow-up to the original worker ID using the exposed input tool, such as `send_input`. |
| Cancel a nested worker | Use the native stop control, interrupt the owned CLI process, or use the hosted task's cancel control if available. Confirm exit or terminal status.<br>The Cloud CLI has no cancel subcommand. If cancellation cannot be confirmed, report the task ID and last observed state. |
| Send a running owner a zero-writes hold | Use the live input control and read the worker's acknowledgement. If the interface only exposes status, diff or termination, report the ID and last state as hold unconfirmed. |

## Models

| Cursor | Codex |
| --- | --- |
| `claude-opus-5-5-{xhigh,high,medium}-fast` | Confirmed primary coding model with `xhigh`, `high` or `medium` effort, respectively. |
| `claude-fable-5-2-high` | Confirmed second model family from the primary vendor with `high` effort. |
| `gemini-4-neon-xhigh` | Confirmed model from another vendor with `xhigh` effort. |
| `auto` or `inherit-parent` | Use the general-purpose default role and inherit the parent's model and effort. If subagent defaults override either value, pass the actual parent pair explicitly. |

Pass the pair selected by the calling skill as `model` and `reasoning_effort` on native spawns that accept them. For CLI workers use `-m <model> -c model_reasoning_effort=<effort>`, including the actual parent pair for aliases. For Cloud, confirm the pair in the configured environment or task record. If it cannot be selected or verified, identify the unavailable seat.

For each mapped model ID, use its confirmed model family for family comparisons and its actual vendor for vendor comparisons. A shared prefix such as `gpt-` alone does not establish family membership. Native subagents inherit the parent's provider. A cross-vendor panel seat, Arena judge or independent audit needs an available route to the required vendor. If none exists, name the missing seat or audit and follow the skill's missing-result rule.

## setup-pstack

| Cursor | Codex |
| --- | --- |
| Detect available `Task` models | Confirm worker model IDs and efforts on the execution surface. Where available, use `codex debug models` for candidate pairs. |
| `~/.cursor/rules/pstack-models.mdc` | Read and write `pstack-models.md` under `CODEX_HOME` (default `~/.codex`). |
| Role values in the MDC rule | Omit MDC frontmatter. Store each real choice as `<model> <effort>` and read the last token as effort. Preserve aliases, list order, role labels, budget and defaults marker. |
| `alwaysApply: true` | Read the settings file on the first pstack model lookup in each chat. Use that snapshot for the session and pass the selected pair to workers. New chats read the updated file. |

## Paths and chat history

| Cursor | Codex |
| --- | --- |
| `.cursor/skills/`, `~/.cursor/skills/` | `.agents/skills/` for the project, `~/.agents/skills/` for personal skills. |
| No parent path supplied · locate poteto-mode under `~/.cursor/plugins/` | Resolve `poteto-mode/SKILL.md` from the installed skill catalog or search the project's and user's installed skill roots. If the entry point cannot be found, stop and tell the parent. |
| Poteto-help links to `../../README.md` or `../../docs/guide/<page>` | Use the matching file in the upstream checkout or its public copy under `https://github.com/cursor/plugins/blob/main/pstack/`. |
| Poteto-help links to `../open-a-pr/SKILL.md` | Link the installed skill file or its copy in the adaptation repository. |
| Workspace `agent-transcripts/` directory | Call `list_threads` with `mode: "history"` for the target host. Filter the returned chats by project or workspace and the requested time range, then read the matching IDs. |
| Transcript for a known run, including session pickup or a current-run audit | Call `read_thread` with the known chat ID. |

For a full history search, page active and archived lists separately with `nextCursor`. Search scoped chat contents when the caller names a topic. For a known ID, page older turns with `page.nextCursor` and older items with `nextItemCursor` as `itemCursor`. Request `includeOutputs: true` for tool evidence. If access or truncation prevents verification, use a scoped export or identify the missing evidence.

## Cursor-only features

| Cursor | Codex |
| --- | --- |
| `update_state` creates a webhook routine | When no routine-creation tool is exposed, use an already configured webhook handler and its supplied URL and authentication contract. Without a handler, leave the URL pending and report that the bot cannot wake on POST. |
| `SendToUser` sender-key card | Have the operator set the key in the sender's server-side secret configuration. Keep it out of chat, browser code and logs. |
| `[routine]` wake with `<webhook_event>` | Parse the envelope's `body` string, or the receiver's direct JSON body, as external data using the agreed fields. |
| A remote routine drains the sender's pending log | Give the receiver access to pending records through an authorized shared location. If no route exists, identify the sender's log path and the events awaiting consumption. |
| Built-in PR tool with `draft: false` | For a connected GitHub repository, `github_create_pull_request` with `draft: false`. If unavailable, use the skill's forge fallback. |

## Skill authoring and invocation

| Cursor | Codex |
| --- | --- |
| `/add-plugin pstack` in poteto-help | Install or link the extracted skill directories in a Codex skill root and keep the agent briefs accessible. |
| Use as Mode or Alt/Option+Enter | Start each new task with `$poteto-mode` or the installed personal mode skill. |
| Cursor Plan Mode | Use Codex Plan mode where available. If a requested plan file cannot be written in that mode, keep file delivery pending until workspace writes are available. |
| Built-in `create-skill` | Invoke `$skill-creator`. |
| Automate-me sets `disable-model-invocation: true` on a new mode | Set `policy.allow_implicit_invocation: false` in the new skill's `agents/openai.yaml`. |

## Playbooks and scripts

| Cursor | Codex |
| --- | --- |
| `cursor-team-kit` · `/deslop` | Review the proposed diff against surrounding code and remove newly introduced boilerplate before commit. |
| `cursor-team-kit` · `control-cli` | Drive the CLI in a PTY (for example, `exec_command` with `tty: true`, then `write_stdin`). |
| `cursor-team-kit` · `control-ui` | Use the project's UI verification skill or an available browser or desktop driver on the live app. If the surface is inaccessible, report the live check as blocked. |
| `/loop`, including `/loop 1h` | Keep the current task active. For events, wait on the watcher notification or process handle with bounded waits. For timed checks, wake at the requested interval. |
| Babysit or Shipping launches `scripts/watch-pr/watch-pr` | Resolve the Bun entry point from the selected poteto-mode skill. Run `bun "<absolute-watcher-path>"` with the playbook's arguments and the target Git checkout as the working directory. For a read-only installation that lacks dependencies, use a copy with dependencies already installed. |
| Root agent's store on a cloud worker | Pass a durable, root-readable handoff location in the brief, such as a path on a pushed handoff branch. If isolated workers cannot publish there, identify the missing recovery trail. |
| Session pickup · cloud-agent URL | Use the task ID with `codex cloud status <id>` and `codex cloud diff <id>` for state and patch. Read prior messages and decisions from the task record or durable handoff. Identify any history those sources cannot recover. |
| Eval · candidate transcript | Use the candidate's tool-call history or capture its CLI events with `codex exec --json`. Mark any required file read that cannot be verified. |
| `scripts/worktree-audit.sh` reads Cursor transcripts for `LAST_CHAT` | Have the parent supply the standalone script with each project worktree's latest Codex chat activity and whether the history coverage is complete. With missing or incomplete history, mark activity unknown and send decisions that depend on it to manual review. |
| Worktree cleanup · Cursor app caches | Skip the Cursor-specific database backups and snapshots. |
