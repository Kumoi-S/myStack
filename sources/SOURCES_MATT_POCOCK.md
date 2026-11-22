## 上游来源

在仓库根目录运行以下命令。

```sh
git submodule update --init --recursive -- sources/mattpocock-skills
```

以下路径均相对于本文件。

## Matt Pocock Skills

安装命令为 `npx skills@latest add mattpocock/skills -a <agent>`，可用 `--skill=<name>` 选定单项。Vercel Skills CLI 负责发现技能

- 安装说明　`mattpocock-skills/.agents/install-block.md`
- 正式技能清单　`mattpocock-skills/.claude-plugin/plugin.json` 的 `skills` 数组
- 技能元数据校验　`mattpocock-skills/scripts/check-frontmatter.mjs`
- 发布流程　`mattpocock-skills/.github/workflows/release.yml`
- 开发用软链接　`mattpocock-skills/scripts/link-skills.sh`

### 正式发布的技能（27 个）

v1.3.2 与当前检出的插件清单一致。各技能的入口为对应目录下的 `SKILL.md`。[v1.3.2 发布页](https://github.com/mattpocock/skills/releases/tag/v1.3.2)

- [mattpocock-skills/skills/engineering/](mattpocock-skills/skills/engineering/)（20 个）
  - `ask-matt`、`code-review`、`codebase-design`、`diagnosing-bugs`、`domain-modeling`、`grill-with-docs`、`implement`、`implement-spec`、`improve-codebase-architecture`、`pr`
  - `prototype`、`research`、`retro`、`setup-matt-pocock-skills`、`tdd`、`to-spec`、`to-tickets`、`triage`、`wayfinder`、`wizard`
- [mattpocock-skills/skills/productivity/](mattpocock-skills/skills/productivity/)（7 个）
  - `grill-me`、`grilling`、`handoff`、`teach`、`to-questionnaire`、`wait-what`、`writing-for-agents`

当前检出共有 39 个可发现的技能，含 `mattpocock-skills/skills/in-progress/` 的 8 个开发中技能和 `mattpocock-skills/skills/misc/` 的 4 个冻结技能。
