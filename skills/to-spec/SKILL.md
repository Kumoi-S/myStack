---
name: to-spec
description: "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed."
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

The issue tracker and triage label vocabulary should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.
2. Write the spec using the template below, then publish it to the project issue tracker. Apply the `ready-for-agent` triage label - no need for additional triage.
```
## Problem Statement

The problem that the user is facing, from the user's perspective.

## Requirements

Capture the agreed requirements in the simplest clear, verifiable form, using the user's language where possible. Use direct statements, user stories, or Gherkin as appropriate.

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes.
```

