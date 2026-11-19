---
name: explain
description: Explain existing systems, implementations, and proposed designs, including how they work, why key decisions were made, and their trade-offs. Use when a clear, evidence-grounded technical explanation is needed.
disable-model-invocation: "true"
---
Help readers quickly build a clear mental model of what something is and how it works. Explain why important choices were made when relevant.

Use available context first. When needed, use /how to investigate existing implementations and /why to trace past design decisions. For proposed designs, rely on their design materials and stated rationale. Keep investigations focused.

## Explanation Principles

- **Explain the design and its rationale.** Clarify the problems and constraints behind key design decisions, meaningful alternatives, and relevant trade-offs or risks. Focus on what helps explain the design or affects a decision.
- **Separate evidence from inference.** Distinguish established facts, stated requirements, inferences, and unknowns. Ground explanations in available evidence, citing sources when useful. When the original rationale is unclear, explain plausible reasons as hypotheses rather than confirmed intent.
- **Lead with what matters.** Match the request's scope and depth. For broad requests, establish the big picture before expanding into details. Make conclusions easy to find and details easy to explore. Recommend a course of action when a decision is needed and the evidence supports it.

## Representation Selection

Use the simplest representation that makes the explanation clear. Prefer diagrams, pseudocode, or other structured formats over lengthy prose when they communicate the information more directly. If a specific format is requested, use it.

- **Pseudocode - Operations.** Show how something works step by step (e.g., logic, algorithms, calculations, state changes). Use LaTeX for math-heavy algorithms and Python-style code blocks for program-heavy operations. Use comments when useful.
- **Mermaid - Relationships.** Show how things connect or interact (e.g., architecture, dependencies, control/data flow, call sequences). Choose the Mermaid diagram type that best fits.
- **Plain Language - Explanations.** Explain concepts, reasons, trade-offs, and conclusions. Also use it for simple operations or relationships that don't need a diagram or pseudocode.
- **Other Formats.** Use other formats (e.g., tables, trees, diffs, specialized diagrams) when they better communicate the information than the options above.

**Presentation:** Keep supporting prose brief and close to the diagram or code it explains. Highlight the key point rather than repeating the representation. Include only details relevant to the current question. Combine formats only when each adds important information.
