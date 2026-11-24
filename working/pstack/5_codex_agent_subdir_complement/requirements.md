# Stage 5 — Add Codex invocation policy

Use `../4_autoPR_remove/output/` as input and write the result to `./output/`.

For each `SKILL.md` with `disable-model-invocation: true` in its frontmatter, create `agents/openai.yaml` in the skill directory if the file is missing. Leave any existing `agents/openai.yaml` untouched.

Use the following contents for new files.

```yaml
policy:
  allow_implicit_invocation: false
```
