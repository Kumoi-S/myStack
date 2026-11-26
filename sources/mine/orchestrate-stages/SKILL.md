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

ON worker completion
    Inspect the actual output against its requirements and user's special instructions before handing it off
    WHILE a correction is needed and work can proceed
        Hold downstream work and follow the stage's correction instructions
        If none are given, send the evidence to the responsible worker
        Check the revised output against the same requirements and user instructions
    IF human review is due or work is blocked
        Report the current artifact and the decision or blocker
        STOP the workflow
```

The requirements define the work. Change them only at the user's request.
