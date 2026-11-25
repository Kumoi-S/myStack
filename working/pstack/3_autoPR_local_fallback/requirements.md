# Stage 3 — Extract the pstack PR skill

Use `../2_.agent_convention/output/` as input and write `./output/`.

1. Move the [Opening a PR procedure](../1_extract_and_pick/output/skills/poteto-mode/playbooks/opening-a-pr.md) from `skills/poteto-mode/playbooks/opening-a-pr.md` to `skills/open-a-pr/SKILL.md`. Carry over the procedure from the Stage 2 output.
2. Set `name: open-a-pr`, a short `description`, and `disable-model-invocation: true` in the skill frontmatter.
3. Update existing calls to use pstack's named-skill wording, such as `Run the **open-a-pr** skill.`
4. Remove `Opening a PR` from the Playbooks section in `skills/poteto-mode/SKILL.md`. Omit `Invoked at the end of every other playbook.` from the extracted skill. Update documentation links to point to the new skill.

Append the following fallback to the skill.

> If the repository has no configured Git remote, merge the work branch into the intended local base branch with `git merge` and report the result.
