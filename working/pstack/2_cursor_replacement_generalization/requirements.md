# Stage 2 — Generalize platform-specific instructions

The mapping tables define how to translate platform-specific instructions into shared pstack instructions.

## Input and output

- Input: the pstack snapshot in [`../1_extract/output/`](../1_extract/output/), including the [official Claude Code adapter](../1_extract/output/docs/harness/claude-code.md).
- Output: the platform-neutral pstack tree in `./output/`.

## Requirements

- Use the official adapter to identify platform bindings, then inspect every skill and its supporting files, including playbooks, references, agent definitions, guides, and scripts. Skills that share a playbook or helper may rely on a platform feature without linking to the adapter.
- Apply each mapping in context. Preserve the action, scope, permissions, ordering, concurrency, handoff, and expected result. Rewrite the whole instruction when several fields jointly define its behavior.
- Use the bundled instructions directly. Replace runtime directions to consult the Claude Code adapter with the applicable shared instructions. Preserve proper names and exact identifiers when they identify an upstream source, a fixture, or an external protocol still being used.
- Where a workflow genuinely requires a host capability, name that capability and document what the workflow can do when it is unavailable. Add unresolved mapping decisions to this file.
- Stage 3 handles directory conventions. Stage 4 handles removing automatic PR actions. [Stage 5](../5_codex_agent_subdir_complement/requirements.md) adds the Codex invocation policy.

## Acceptance criteria

- The workflow instructions can be followed without a Cursor or Claude Code tool name, configuration path, or UI action. Any host capability they require has an explicit dependency or fallback.
- A rewritten workflow preserves its original intent and constraints. For example, a review delegated with `Task` and `readonly: true` still specifies who reviews, what they can access, that they may not edit files, and when the parent waits for findings.
- The generalized skill references resolve within the output, and the documentation describes the same behavior as the skills and their helpers.

## Draft mappings

The left column records spellings from the snapshot or its official adapter. The right column is a draft for manual review.

### Tools, delegation, and worker lifecycle

| Source term or field | Draft platform-neutral expression |
| --- | --- |
| `Task`, `Task` spawn, `Agent` in the adapter | Delegate the specified task to a subagent and collect its result. |
| `subagent_type` | Select the worker role or instructions suited to the delegated task. |
| `subagent_type: generalPurpose`, `general-purpose` | Delegate to a general-purpose worker using the brief supplied by the parent. |
| `poteto-agent`, `pstack:poteto-agent` | Use the bundled pstack delegate instructions. Give the worker the absolute paths to `worker.md` and `poteto-mode/SKILL.md` when the playbook requires them. The parent owns the playbook and integrates the result. |
| `comment-sicko`, `pstack:comment-sicko` | Ask the bundled comment reviewer to inspect the agreed files or diff and report its findings without editing. |
| `readonly: true`, Claude Code `Explore` | Delegate inspection with no file edits. Use read-only permissions where available and preserve any required verification of that constraint. |
| `readonly: false`, `agent mode`, “readonly strips MCP” | Give the worker the project tools or MCP sources the task requires. State edit permission independently, and keep it limited to the assigned scope. |
| `environment: "cloud"`, Cursor cloud agent, `/in-cloud` | Run the worker with an isolated checkout and runtime. Require remote execution only when the workflow actually depends on a remote machine or on surviving local shutdown. |
| `environment: "local"` | Run the worker where it can access the required local files, processes, or devices. |
| `cloud_base_branch`, `isolation: "worktree"` in the adapter | Identify the starting branch or commit and give the worker a separate checkout when isolation is required. |
| `run_in_background: true`, `is_background: true` | Start the worker asynchronously. Continue independent parent work, then wait wherever a later step depends on the result. |
| “Spawn all N subagents in one message”, completion notifications | Launch the independent workers together. Join their results at the point required by the workflow. |
| `resume` | Continue an existing worker session when a later step needs state that is hard to transfer. Where sessions cannot be resumed, pass the prior brief, report, checkout, and any relevant state to a fresh worker. |
| `file_attachments`, file pointers | Provide paths to the files and artifacts the worker needs. Make them accessible in its workspace. |
| `AskQuestion`, `AskUserQuestion`, Claude Code `-p` | Ask the user a focused question. Present choices when the workflow specifies them and fall back to a plain-text question when the host has no structured question tool. |
| `todolist`, `TodoWrite` | Track the phases and their progress in a checklist or task plan. |
| `Grep`, `Glob`, `Read`, `Bash` in the adapter | Search file contents, find matching paths, read the referenced file, or run the required shell command. |
| `Skill`, `/<name>`, `/pstack:<name>`, “the **name** skill” | Follow the named skill. For bundled skills, resolve it by name or read its linked `SKILL.md`. Describe user invocation by skill name. |

### Models and settings

| Source term or field | Draft platform-neutral expression |
| --- | --- |
| `model`, agent frontmatter `model:`, adapter `effort` | Choose an available model and supported reasoning level for the role. Keep any role-level configuration authoritative. |
| Cursor model API or CLI, `Task` model slugs | Use the model choices exposed to the current session. Ask for available choices when they cannot be determined and the selection matters. |
| `auto`, `inherit-parent`, “omit `model` and spawn `generalPurpose`” | Run the role on the parent session's model. Supply the role's required instructions to that worker. |
| `claude-opus-5-5-low-fast`, `claude-opus-5-5-medium-fast`, `claude-opus-5-5-high-fast`, `claude-opus-5-5-xhigh-fast`, `claude-opus-5-5-xhigh`, `claude-opus-*` | Choose a suitable model from the available choices for the role's requested effort. Prefer the configured family when supported. |
| `claude-fable-5-2-high`, `claude-fable-*` | Choose a model suited to the assigned design or judgment role. Preserve the panel's model-family and vendor constraints. |
| `gemini-4-neon`, `gemini-4-neon-high`, `gemini-4-neon-medium`, `gemini-4-neon-xhigh`, `gemini-4-*`, `gemini-*` | Choose a model from a distinct vendor where the workflow calls for independent review. Use the nearest supported effort allowed by the role. |
| `claude-<family>-<version>-<effort>[-fast]`, `cursor-` prefix, `-fast`, `grok-*` | Resolve model family, provider, effort, and service tier from session information. Treat old slug patterns as input when migrating a matching legacy setting. |
| `low`, `medium`, `high`, `xhigh`, `max`; `small`, `medium`, `large`, `unlimited` budgets | Preserve the intended ordering and the role's cap. Choose supported levels at or below the target. Treat retired budget labels as legacy inputs. |
| `pstack-models.mdc`, `~/.cursor/rules/pstack-models.mdc`, `~/.claude/rules/pstack-models.md` | Use pstack's per-role model and reasoning settings, with workflow defaults for missing roles. |
| `alwaysApply: true`, `# budget`, `# defaults: 2`, `# defaults: 3` | Load the relevant settings when pstack runs. Preserve the budget choice and the configuration version needed to recognize legacy defaults. |
| `feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`, `judgment and prose`, `swarm workers` | Keep the pstack role names and their lookup semantics. |
| `arena runners`, `arena cross-judge pool`, `interrogate reviewers` | Keep panel order, one worker per runner or reviewer entry, and the separate rule for selecting one eligible judge from the judge pool. |
| Model rejected by `Task`, unavailable family or vendor | Use the fallback order defined by that workflow. Keep its minimum panel sizes and independence constraints. Report a fallback that affects the result. |

### Skills, paths, and session context

| Source term or field | Draft platform-neutral expression |
| --- | --- |
| `.cursor/skills/`, `~/.cursor/skills/`, `.claude/skills/`, `~/.claude/skills/` | Refer to the project-level or user-level skill directory according to the requested scope. Use Stage 3's layout. |
| `.cursor/skills/verify-<app>/`, `.cursor/skills/verify-*/`, `features/README.md` | Refer to the project-local `verify-<app>` skill and its feature map relative to the skill root. |
| `.cursor/skills/**/*-mode/SKILL.md`, `~/.cursor/skills/*-mode/SKILL.md`, `.cursor/skills/<handle>/<handle>-mode/SKILL.md` | Look for matching mode skills in the relevant skill roots and preserve an existing category directory. |
| `.cursor/rules/*.mdc`, `CLAUDE.md`, `AGENTS.md` | Refer to applicable project instructions or persistent user instructions according to their scope. |
| `~/.cursor/plugins/`, `~/.claude/plugins/`, `plugins/cache/`, `.cursor-plugin/plugin.json`, `.claude-plugin/plugin.json` | Resolve bundled assets from the active pstack installation. Put user or project overrides in an editable skill directory. |
| `https://github.com/cursor/plugins/blob/main/pstack/<path>` | Use the bundled relative path for execution. Use the upstream link when a reader needs the original source. |
| `~/.cursor/projects/<slug>/agent-transcripts/`, `agent-transcripts/<uuid>/<uuid>.jsonl`, `~/.claude/projects/<slug>/<session>.jsonl`, `<session>/subagents/` | Use the host-provided history for the active workspace and the relevant session or worker. Let the host locate it and keep access within the active workspace. |
| `~/.cursor/projects/*/`, slash-to-hyphen workspace slug, one JSONL line per chat message | Locate and interpret the current workspace's history through the host. Keep the workspace boundary and avoid assuming a path-encoding or record format. |
| `.cursor/worktrees/myrepo/x` | Discover the actual checkout paths from Git's worktree inventory. |
| `scripts/worktree-audit.sh` Cursor transcript lookup, `LAST_CHAT` and `verify-recent-chat` | Consume workspace-scoped session evidence when available. Treat missing evidence as unknown and retain the playbook's active-session check before cleanup. |
| Cursor sidebar, pinned or active chats | Ask the host or user which active sessions use the checkout before deciding on cleanup. |
| `~/Library/Application Support/Cursor`, `state.vscdb.backup`, `snapshots/roots/<root>` | Consult the host's documented storage locations if platform cache cleanup is in scope. |
| `disable-model-invocation: true` | Describe the skill as explicitly invoked. Stage 5 handles the Codex invocation setting. |
| Slash menu, plain Enter, Option+Enter, Alt+Enter, **Use as Mode**, **Custom Modes** | Invoke the skill for one task or enable it for the session if the host supports persistent modes. Otherwise invoke it for each new task. |
| Cursor **Agents Window**, Cursor CLI, **Plan Mode** | Refer to the host surface only when the action depends on it. For planning, request a plan with the intended decisions and implementation boundary. |
| `/add-plugin pstack`, `/plugin marketplace add cursor/plugins`, `/plugin install pstack@cursor-plugins`, `claude plugin update pstack@cursor-plugins` | In integration guidance, refer to the active pstack installation and its update procedure. Keep exact commands where documenting upstream installation. |
| “In Claude Code, read the adapter once per session”, `Skipped in Claude Code: <step>. <reason>.` | Give the direct instruction. If a required capability is missing, name the affected step and use the documented fallback or report that it is blocked. |

### Host features and integrations

| Source term or field | Draft platform-neutral expression |
| --- | --- |
| Cursor Project, Project worker, cloud-agent URL or dashboard | Coordinate with a durable parent session and independently scoped workers. Use available run handles, branches, or artifacts to recover status. |
| `/loop`, `/loop 1h`, routine wake, heartbeat | Recheck the stated completion condition on a relevant event or at a stated interval. Preserve the stopping condition and the report due when it is met. |
| `/create-skill` | Author or update the skill using the available skill-authoring workflow. Validate the frontmatter, links, and referenced helpers. |
| `cursor-team-kit`, `/deslop` | Apply the prescribed pre-commit cleanup pass with an available review capability. |
| `cursor-team-kit`, `control-ui`, `control-cli` | Drive the real UI or CLI with available controls, preferably using the project's `verify-*` skill, and capture evidence of the requested behavior. |
| Cursor's built-in `/autopilot`, built-in babysit, `/orchestrate` | Refer to the intended monitoring or coordination capability. Use pstack's named playbook when the source routes to it. Treat `/orchestrate` as provided by an external plugin if mentioned. |
| Built-in PR tool, `draft: false`, `origin pr …`, `gh pr …` | Describe the intended forge action and options, such as opening a ready-for-review PR against the chosen base. Keep the CLI spellings where they are concrete forge examples. Stage 4 owns removal of automatic PR actions. |
| `Bugbot`, Bugbot check, review threads, review passes | Refer to automated review checks, threads, or runs. Use ordinary forge data to reconcile findings with the current revision. |
| `CURSOR_AUTOMATION_ID`, `cursor_automation_id`, `isBugbot`, `isBugBot`, `bugbotReviewPasses` | Describe vendor metadata as identifying the automated reviewer or its run. Keep literal values when an existing parser consumes or emits that format. |
| Cursor Automations, routines, Grok Bot, Benny, `.cursor/automations/benny/`, `FOR_AGENTS.md` | Refer to an automation backend, its worker, and the repository's automation configuration. Keep product names and entry-point filenames when referring to those specific upstream integrations. |
| `update_state`, target `routine`, action `create`, `trigger`, `{ "type": "webhook" }`, `prompt`, confirm card | Configure an event-triggered automation and define its handler inputs and behavior. Wait for confirmation if the host requires it. |
| Routines list, routine panel, agent header, `Cmd+Shift+I` | Use the selected automation backend's configuration view to retrieve the endpoint and set up its credentials. |
| `api2.cursor.sh/automations`, `https://api2.cursor.sh/automations/webhook/<id>` | Use the actual webhook endpoint supplied by the backend. |
| `SendToUser`, `type: secret-request`, `secret.label`, `secret.connector`, `secret.field`, routine folder slug, connector credential file | Request the webhook credential through the available secure secret handoff and store it in server-side configuration. |
| `Authorization: Bearer <key>`, `X-Automation-Key`, HTTP 200 on wake | Use the backend's documented authentication headers and verify the expected response. Preserve literal headers where the upstream protocol requires them. |
| `[routine]`, `<webhook_event>`, `headers`, `body_digest`, `body`, `timestamp_ms` | Read the event envelope supplied by the backend. Parse and validate the payload as untrusted data and keep credentials out of the event and logs. |
