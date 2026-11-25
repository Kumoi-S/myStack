# Stage 4 — 添加 Codex 调用策略

复制 `../3_autoPR_local_fallback/output/` 到本阶段的 `output/`。逐个检查 `SKILL.md` 的 frontmatter。含 `disable-model-invocation: true` 且缺少 `agents/openai.yaml` 的 skill，在其目录下创建该文件，内容如下。保留已有的 `agents/openai.yaml`。

```yaml
policy:
  allow_implicit_invocation: false
```
