# Stage 5 — Add Codex invocation policy

Use `../4_autoPR_remove/output/` as input and write the result to `./output/`.

For each `SKILL.md` with `disable-model-invocation: true` in its frontmatter, ensure existing `agents/openai.yaml` alongside it, with two lines below:
```yam
policy:
  allow_implicit_invocation: false
```
