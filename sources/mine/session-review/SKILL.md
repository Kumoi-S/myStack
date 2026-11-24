---
name: session-review
description: Review completed agent sessions, identify user corrections and recurring problems, reconstruct what happened, and present evidence-based explanations and improvement options.
disable-model-invocation: true
---

# Session Review

## Goal

Help the user understand what went wrong during agent work and decide whether and how to improve the working environment.

The output is a decision-ready review, not an automatically modified repository.

## 1. Find the problems

Read the relevant conversation and available execution records.

Identify:

- Explicit user corrections and rejected results.
- Repeated revisions or misunderstandings.
- Work the user had to do manually because the agent did not.
- Important requirements or checks that were missed.
- Differences between the delivered result and its intended use.

Preserve the surrounding context. Do not interpret an isolated correction without understanding what prompted it.

Group related corrections into problems rather than listing every correction separately.

## 2. Reconstruct each problem

For each problem, explain:

- What the user wanted.
- What the agent understood or did.
- What happened next.
- What the user corrected.
- What impact this had on the work.

Distinguish observed events from inferred explanations.

## 3. Analyze possible causes

Use the task contract as a diagnostic reference:

Goal, Audience & Use Case, Context & Materials,
Constraints, Acceptance Criteria, Evidence.

Consider whether the problem involved:

- Missing or incorrect task information.
- Missing, stale, unclear, or inaccessible repo knowledge.
- An unsuitable skill or working method.
- Poor information organization or retrieval.
- Model judgment or capability limitations.
- Ignored instructions or ineffective enforcement.
- Inadequate verification.
- Tool or environment limitations.

Do not force every problem into one category.
Do not assume the user is responsible for information
the agent could reasonably have inferred or retrieved.

## 4. Consider solutions

Identify the smallest plausible improvement.

Consider existing repo documentation, skills, examples,
tools, workflows, automated checks, and verification methods.

Account for the repo's actual purpose and working conventions.
Do not apply coding-oriented solutions to writing work,
or research-oriented standards to creative work.

Explain the expected benefit, limitations, and possible
side effects of each relevant option.

Avoid adding generic instructions, redundant rules,
or requirements that reflect the model's preferences
rather than the user's needs.

## 5. Present findings

For each problem, provide:

- Observed problem and chronology.
- Supporting evidence.
- Possible cause.
- Suggested solution or alternatives.
- Expected impact and trade-offs.

Rank findings by importance, not by how easy they are to fix.

Do not edit persistent context, skills, or repo files.
Let the user decide which problems to address and how.

When the user approves a substantial documentation
or skill change, use writing-for-agents.
Use existing evaluation or verification workflows
when the proposed change warrants them.
