---
name: orchestrate-stages
description: Run a staged workflow with fresh subagents while the main agent verifies results and coordinates handoffs.
---

# Orchestrate stages

```text
FOR stage IN requested stages, in workflow order
    IF stage/orchestration.md exists
        READ stage/orchestration.md
        FOLLOW that file
    ELSE IF stage/requirements.md exists
        DISPATCH one fresh worker for the whole stage using stage/requirements.md
    ELSE
        REPORT "stage <strage> missing both orchestration.md and requirements.md"
        STOP the workflow
    AFTER the stage is accepted, report its output and continue

ON "DISPATCH"
    Start the fresh subagent without forking the conversation
    Give it the only requirements.md as input, if user have special instructions, append them in input

ON worker completion OR a worker pause for human edits or review
    Inspect the actual output against every requirement and user instruction due before handoff
    WHILE a correction is needed and the worker can make it
        Hold downstream work and follow the stage's correction instructions
        If none are given, send the evidence to the responsible worker
        Check the revised output against the same requirements and user instructions
    IF any requirement due before handoff is unmet or unverified, or work is blocked
        Report the current artifact, the outstanding issue, and what is needed to proceed
        STOP the workflow
    IF human edits or review are due
        Hand the verified artifact to the user, state the requested action, and STOP the workflow
```

The requirements define the work. Change them only at the user's request.
