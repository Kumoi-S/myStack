# Stage 2 — Generalize platform-specific instructions

## Input and output

- Read the pstack snapshot in [`../1_extract/output/`](../1_extract/output/). Use the [Claude Code adapter](../1_extract/output/docs/harness/claude-code.md) as a review reference.
- Write the adapted pstack tree to `./output/`.

## Review and rewrite

1. Check whether these requirements miss any passages that need changes.
2. Use the Claude Code adapter as a reference when revising the original text, then remove the adapter from the output.

## Acceptance criteria

- Describe platform-specific tools and actions in terms of the capability the workflow requires. Keep exact names when they identify an upstream source, a fixture, or an external interface the workflow uses.
- Keep the original headings, step order, and wording wherever possible. Rewrite a whole instruction when several platform-specific fields together express one action. Preserve its action, scope, permissions, timing, concurrency, handoff, and expected result. Keep explanations and fallback steps limited to those in the original workflow.
- Each local link in an edited file still points to the intended file.

## Rewrite examples

The left column pairs source terms with their context. The right column shows how the instruction could read in that context. Adapt each example to the original passage.

### Tools, delegation, and worker lifecycle

| Source term and context | Example rewrite |
| --- | --- |
| `Task`, `Agent`<br>Delegation to a subagent | Delegate the task to a fresh-context subagent and collect its result. |
| `subagent_type`<br>Role selection for a delegated task | Give the subagent the instructions for the assigned role. |
| `subagent_type: generalPurpose`, `general-purpose`<br>Worker with a task brief | Give the brief to a general-purpose subagent. |
| `poteto-agent`, `pstack:poteto-agent`<br>Delegation from a poteto-mode playbook | Give the worker the absolute paths to `worker.md` and `poteto-mode/SKILL.md`. As the parent, follow the playbook and integrate the result. |
| `comment-sicko`, `pstack:comment-sicko`<br>Comment review of an agreed scope | Ask the bundled comment reviewer to inspect the specified files or diff and report findings without editing files. |
| `readonly: true`, `Explore`<br>Code inspection and explanation in `how` | Give one subagent the question and brief. Have it inspect and explain the code without editing files. |
| `readonly: false`, agent mode, “readonly strips MCP”<br>Worker access to MCP servers | Give the worker access to the session's MCP servers. |
| `environment: "cloud"`, Cursor cloud agent, `/in-cloud`<br>Work that runs on a remote machine | Run the worker on a remote machine. |
| `environment: "local"`<br>Worker access to the user's computer | Run the worker on the user's computer so it can access the required local resources. |
| `cloud_base_branch`, `isolation: "worktree"`<br>Isolated work from a specified starting revision | Start the worker in a separate checkout of the specified branch or commit. |
| `run_in_background: true`, `is_background: true`<br>Asynchronous delegation | Start the worker in the background. |
| “Spawn all N subagents in one message”, completion notifications<br>Parallel panel with a later join | Start all N subagents together and collect their results before the next step that needs them. |
| `resume`<br>Continuation of a prior worker session | Resume the worker's previous session. |
| `file_attachments`, file pointers<br>Inputs passed in a worker brief | Give the worker the paths to the referenced files. |
| `AskQuestion`, `AskUserQuestion`<br>User decisions with specified choices | Ask the user to choose among the listed options. |
| `todolist`, `TodoWrite`<br>Progress tracking across phases | Put the steps in a checklist and update it after each phase. |
| `Grep`, `Glob`<br>Search by content or filename | Find files matching the specified text or filename pattern. |
| `Read`<br>Opening a referenced file | Read the referenced file. |
| `Bash`<br>Executing a prescribed command | Run the specified command. |
| `Skill`, `/<name>`, `/pstack:<name>`<br>Workflow handoff to another bundled skill | Follow the named skill. |

### Models and settings

| Source term and context | Example rewrite |
| --- | --- |
| `model`, `model:`, `effort`<br>Settings for a subagent role | Run the subagent with the model and reasoning level configured for its role. |
| Cursor model API or CLI, `Task` model slugs<br>Model discovery in setup | List the models and reasoning levels available to this session. |
| `auto`, `inherit-parent`<br>A role configured to share its parent's model | Run the worker on the parent session's model and give it the role brief. |
| `claude-opus-5-5-low-fast`, `claude-opus-5-5-medium-fast`, `claude-opus-5-5-high-fast`, `claude-opus-5-5-xhigh-fast`, `claude-opus-5-5-xhigh`, `claude-opus-*`<br>Configured Opus model for a code worker | Run the code worker on the configured Opus model with the specified reasoning level. |
| `claude-fable-5-2-high`, `claude-fable-*`<br>Configured Fable model for design or judgment | Run the design reviewer on the configured Fable model with high reasoning effort. |
| `gemini-4-neon`, `gemini-4-neon-high`, `gemini-4-neon-medium`, `gemini-4-neon-xhigh`, `gemini-4-*`, `gemini-*`<br>Independent reviewer on a different provider | Run the independent reviewer on a model from a distinct provider at the specified effort. |
| `claude-<family>-<version>-<effort>[-fast]`, `cursor-`, `-fast`, `grok-*`<br>Model identifier parsing for role selection | Read the model family, provider, reasoning level, and service tier from the available model information. |
| `low`, `medium`, `high`, `xhigh`, `max`, `small`, `medium`, `large`, `unlimited`<br>Reasoning levels and budget caps in setup | Cap the role's reasoning effort at the selected budget. |
| `pstack-models.mdc`, `~/.cursor/rules/pstack-models.mdc`, `~/.claude/rules/pstack-models.md`<br>Per-role model configuration | Use the configured model for each role and the skill's default for a role with no configured model. |
| `alwaysApply: true`, `# budget`, `# defaults: 2`, `# defaults: 3`<br>Settings loading and versioned setup defaults | Load the model settings when pstack runs. Keep the saved budget and defaults version. |
| `feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`, `judgment and prose`, `swarm workers`<br>Keys in the pstack model configuration | Read the role setting for this playbook. |
| `arena runners`, `arena cross-judge pool`, `interrogate reviewers`<br>Panel entries and judge selection | Start one worker per runner or reviewer entry in the listed order. Select one eligible judge from the judge pool. |
| `Task` model rejection, unavailable model family or vendor<br>Workflow with an existing retry order | Try the next eligible model in the specified order. |

### Skills, paths, and session context

| Source term and context | Example rewrite |
| --- | --- |
| `.cursor/skills/`, `~/.cursor/skills/`, `.claude/skills/`, `~/.claude/skills/`<br>Skill lookup by project or user scope | Look in the project or user skill directory for the requested scope. |
| `.cursor/skills/verify-<app>/`, `.cursor/skills/verify-*/`, `features/README.md`<br>Lookup of an app's verification skill and feature map | Open the project's `verify-<app>` skill and read its `features/README.md`. |
| `.cursor/skills/**/*-mode/SKILL.md`, `~/.cursor/skills/*-mode/SKILL.md`, `.cursor/skills/<handle>/<handle>-mode/SKILL.md`<br>Discovery of mode skills | Search the project and user skill roots for mode skills, including those in existing category directories. |
| `.cursor/rules/*.mdc`, `CLAUDE.md`, `AGENTS.md`<br>Persistent instructions by scope | Read the instructions that apply to the project. |
| `~/.cursor/plugins/`, `~/.claude/plugins/`, `plugins/cache/`, `.cursor-plugin/plugin.json`, `.claude-plugin/plugin.json`<br>Lookup of files shipped with pstack | Find the bundled file in the active pstack installation. |
| `https://github.com/cursor/plugins/blob/main/pstack/<path>`<br>Workflow reading a file shipped with pstack | Read the file at the corresponding path in the pstack installation. |
| `~/.cursor/projects/<slug>/agent-transcripts/`, `agent-transcripts/<uuid>/<uuid>.jsonl`, `~/.claude/projects/<slug>/<session>.jsonl`, `<session>/subagents/`<br>Lookup of a worker or session transcript | Read the relevant session or worker history for the current workspace. |
| `~/.cursor/projects/*/`, slash-to-hyphen workspace slug, JSONL chat records<br>History lookup across recent chats in one workspace | List recent chats for the current workspace and read their messages. |
| `.cursor/worktrees/myrepo/x`<br>Checkout lookup during a worktree audit | Locate the checkout in Git's worktree list. |
| `scripts/worktree-audit.sh`, `LAST_CHAT`, `verify-recent-chat`<br>Checking recent chat activity before worktree cleanup | Check the current workspace's chat history for recent activity in the checkout. |
| Cursor sidebar, pinned or active chats<br>Active-session check during cleanup | Check which active or pinned chats use this checkout. |
| `~/Library/Application Support/Cursor`, `state.vscdb.backup`, `snapshots/roots/<root>`<br>Reclaiming disk space from host caches | Check the session host's documented cache locations for files eligible for cleanup. |
| Slash menu, Enter<br>Skill invocation for one task | Invoke the named skill for this task. |
| Option+Enter, Alt+Enter, **Use as Mode**, **Custom Modes**<br>Skill activation for the session | Enable the named skill for the session. |
| Cursor **Agents Window**, Cursor CLI, **Plan Mode**<br>A planning step before implementation | Open a planning session and draft the implementation plan. |
| `/add-plugin pstack`, `/plugin marketplace add cursor/plugins`, `/plugin install pstack@cursor-plugins`, `claude plugin update pstack@cursor-plugins`<br>Installation or update instructions for the active setup | Update the installed pstack bundle. |

### Host features and integrations

| Source term and context | Example rewrite |
| --- | --- |
| Cursor Project, Project worker, cloud-agent URL or dashboard<br>Tracking individual workers in a multi-worker run | Keep the worker handles in the parent session and use them to check each worker's status. |
| `/loop`, `/loop 1h`, routine wake, heartbeat<br>Periodic status check with a stopping condition | Check once an hour until the completion condition is met, then report the result. |
| `/create-skill`<br>Turning a workflow into a reusable skill | Write the reusable skill using the skill-authoring workflow. |
| `cursor-team-kit`, `/deslop`<br>Cleanup review before commit | Run the prescribed cleanup pass on the diff before committing. |
| `cursor-team-kit`, `control-ui`, `control-cli`<br>Verification through the real UI or CLI | Exercise the workflow in the real UI or CLI and capture the result. |
| `/autopilot`, built-in babysit<br>Monitoring a run to completion | Monitor the run until the specified stopping condition is met. |
| `/orchestrate`<br>Coordination of delegated work | Coordinate the workers and collect their results. |
| Built-in PR tool, `draft: false`, `origin pr …`, `gh pr …`<br>Opening a ready-for-review PR against a chosen base | Open a ready-for-review PR against the specified base branch. |
| `Bugbot`, Bugbot check, review threads, review passes<br>Triage of automated review findings on a PR | Check the automated review findings against the current revision. |
| `CURSOR_AUTOMATION_ID`, `cursor_automation_id`, `isBugbot`, `isBugBot`, `bugbotReviewPasses`<br>Review or automation metadata in status reporting | Use the review metadata to identify the automated reviewer and its run. |
| Cursor Automations, routines, Grok Bot, Benny, `.cursor/automations/benny/`, `FOR_AGENTS.md`<br>Reading a repository's automation configuration | Read the worker instructions in the repository's automation configuration. |
| `update_state`, target `routine`, action `create`, `trigger`, `{ "type": "webhook" }`, `prompt`, confirm card<br>Creating an automation with a webhook trigger and handler | Create a webhook-triggered automation with the specified handler instructions. |
| Routines list, routine panel, agent header, `Cmd+Shift+I`<br>Locating the webhook settings after creation | Open the automation settings and copy the webhook endpoint. |
| `api2.cursor.sh/automations`, `https://api2.cursor.sh/automations/webhook/<id>`<br>Endpoint used by a webhook client | Send the request to the webhook URL issued for this automation. |
| `SendToUser`, `type: secret-request`, `secret.label`, `secret.connector`, `secret.field`, routine folder slug, connector credential file<br>Collecting and storing a webhook credential | Request the webhook credential through the secure handoff and store it in server-side configuration. |
| `Authorization: Bearer <key>`, `X-Automation-Key`, HTTP 200 on wake<br>Testing an authenticated webhook request | Send the request with the webhook's required authentication headers and check for HTTP 200. |
| `[routine]`, `<webhook_event>`, `headers`, `body_digest`, `body`, `timestamp_ms`<br>Reading the webhook event at handler entry | Read the request headers, body digest, body, and timestamp from the webhook event. |
