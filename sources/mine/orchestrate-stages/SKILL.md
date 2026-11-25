---
name: orchestrate-stages
description: Run an existing workflow one stage at a time when the user wants a fresh subagent to own each stage and the main agent to supervise, verify results, and handle handoffs.
---

# Orchestrate stages

Start at the first stage the user asked to run. Read its requirements and locate its actual input. Keep its steps together under one worker, including any pause for human review. Change requirements only at the user's request.

1. **Dispatch one stage.** Start a fresh subagent without forking the conversation. Give it the stage requirements, input location, permitted output, and any user decision that affects this stage. Ask it to produce the output, verify it, and report what it checked. Keep its agent ID for follow-up.
2. **Observe and verify.** The worker makes the changes. As coordinator, inspect the actual output yourself. Compare it with the requirements and the input it will replace or pass on. Check a concrete behavior where a change could affect existing callers. For example, if only a scratch path should change, check that omitting an optional argument still gives the original default.
3. **Handle a discrepancy.** Stop the worker if it is still making the faulty change, and hold later stages. Show the expected behavior, what you observed, and the smallest correction. Identify whether the worker departed from the requirements, the requirements conflict with the user's intent, or a choice needs the user's decision. An existing default usually settles a choice the stage never asked to change.
4. **Return the correction to its owner.** If the user asked to stop and report, wait for their direction. When a correction is authorized, resume the same worker with the evidence, then independently check its revised output. If the same problem persists, report what is still failing before another attempt.
5. **Hand off.** After verification passes, give the next fresh subagent the accepted output as its input. At a human review step, link the editable artifact, state what decision is due, and stop. Resume under that stage's stated approval conditions.

Report each handoff briefly. On completion or a stop, identify the last accepted stage, the current artifact, and any work still pending.
