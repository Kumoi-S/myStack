Use concise prose supported by the smallest representation that makes each part of the design clear. Choose by what needs to be understood:
- Logic or algorithms: pseudocode.
- Component interactions, control or data flow, and state or other relationships: Mermaid diagrams (not just flowcharts, use other Mermaid diagram when it fits better), or Unicode diagrams when clearer.
- Structure or changes: trees, diffs, or tables.

Place each representation beside the explanation it supports. Use only what adds clarity; multiple representations are fine when they explain different aspects of the design.

## Problem and constraints

What needs to change, and which facts about the existing system shape the solution?

## Usage

Show the solution from the caller's point of view (API, CLI, UI, or another relevant interface). Use realistic examples where helpful.

## Design

Explain the overall structure, important data models, boundaries, and interactions. Use types and signatures where they clarify consequential design choices.

## Decisions and tradeoffs

Explain the important choices, why they were made, and meaningful alternatives that were not selected.

## Risks and open questions

Record material uncertainties or risks that remain.

## Implementation boundaries

Distinguish design decisions the implementer should preserve from details left to implementation judgment.
