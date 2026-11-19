---
name: show-me
description: Help the user understand the current topic visually with concise diagrams or code-shape sketches.
disable-model-invocation: true
---
Help the user understand the current topic of conversation visually. Skip the preamble and keep prose brief. Pick the smallest view that makes the key point clear.

Choose the representation by what needs to be understood:
- Show logic or an algorithm as pseudocode: code block or LaTeX algorithm notation.
- Show component interactions, control flow, data flow, or other complex relationships using Mermaid diagrams. Choose Mermaid diagram types by semantics: flowchart, sequenceDiagram, classDiagram, stateDiagram-v2, erDiagram, gantt, journey, mindmap, timeline, pie, gitGraph, quadrantChart, xychart, kanban, block, packet, requirementDiagram. If a Mermaid cannot adequately represent the structure, use Unicode text diagram instead.
- Show structure or changes as trees, diffs, or tables.

Place each visual next to the short text it supports. Keep only the things needed to answer the user's current question or the options to resolve the current discussion point.

You may use one of these, you may use several, it is unlikely you will use all of them. Use your judgement and don't overwhelm the user.