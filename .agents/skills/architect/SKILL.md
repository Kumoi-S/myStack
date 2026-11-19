---
name: architect
description: "Create or revise a technical design for a change. Use when the user asks to architect or design a solution before implementation."
disable-model-invocation: true
---

Design a technical solution from the requirements and existing code. Produce a design the user can understand, question, and change, and another agent can implement.

## Design

### 1. Understand the system

Read the requirements and relevant code. Build a mental model of every system the new code touches. When a change alters ownership or layering, investigate rationale and constraints.

### 2. Design

Start from how callers will use the solution. Develop a coherent design for the important data structures, interfaces, module boundaries, and interactions.

If user input could substantially narrow the design space, ask focused questions with the relevant options and trade-offs. Leave local implementation details to the implementer.

Create or update `technical-design.md` with the current design, linking to the requirements source. Follow `references/design-template.md` and keep it concise.

### 3. Explore and refine

When multiple viable candidate approaches have meaningful trade-offs and no clear winner emerges, update `technical-design.md` with the current design before delegating candidate design directions to subagents using `references/runner-prompt.md`.

For each design direction, fork to `technical-design-<direction>.md`. Give each subagent an independent context with references to the requirements, `technical-design-<direction>.md`, and relevant code. Each should explore its assigned direction, treating the current design as a starting point rather than a constraint, and considering coupled decisions together.

As each candidate returns, assign an independent reviewer subagent to evaluate it. Examine the candidate and their reviews yourself, incorporate worthwhile findings, and continue refining the design as needed.

### 4. Revise

The user can ask questions, propose changes, or edit the document. Explain tradeoffs and update the affected design when needed, keeping its related parts consistent.

## Output

A concise, reviewable technical design covering the decisions that matter for implementation. Include sketches, types, examples, or diagrams where they make the design clearer; don't expand the document to cover every internal detail.

Do not proceed to implementation or another workflow unless the user requests it.
