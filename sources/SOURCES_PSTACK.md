## 上游来源

在仓库根目录运行以下命令

```sh
git submodule update --init --recursive -- sources/cursor-plugins
```

以下路径均相对于本文件

## Cursor pstack

### 原始插件

- Agent　`cursor-plugins/pstack/agents/`
- 安装与使用说明　`cursor-plugins/pstack/README.md`
- 插件元数据与许可证　`cursor-plugins/pstack/plugin.json`、`cursor-plugins/pstack/LICENSE`

[cursor-plugins/pstack/skills/](cursor-plugins/pstack/skills/) 下共有 58 个技能目录

**指令技能（34 个）**
- `architect`、`arena`、`automate-me`、`benchmark-checklist`、`blast-radius`、`bro`、`correct`
- `create-formal-verification-skill`、`create-verification-skill`、`figure-it-out`、`how`、`in-your-own-words`、`interrogate`、`ketchup`、`ketchup-video`
- `maintain-formal-verification-skill`、`maintain-verification-skill`、`make-bot-ui`、`no-comments`、`poteto-help`、`poteto-mode`
- `recall`、`reflect`、`setup-pstack`、`sharpen`、`show-me-your-work`、`statechart`、`swarm`、`tdd`、`teach`、`technical-writing`、`typescript-best-practices`、`unslop`、`why`

**Principles（24 个）**
- `principle-attack-the-premise`、`principle-boundary-discipline`、`principle-build-the-lever`、`principle-encode-lessons-in-structure`、`principle-exhaust-the-design-space`、`principle-experience-first`
- `principle-explain-the-number`、`principle-fix-root-causes`、`principle-foundational-thinking`、`principle-guard-the-context-window`、`principle-laziness-protocol`、`principle-make-operations-idempotent`
- `principle-migrate-callers-then-delete-legacy-apis`、`principle-minimize-reader-load`、`principle-model-the-domain`、`principle-never-block-on-the-human`、`principle-outcome-oriented-execution`、`principle-prove-it-works`
- `principle-redesign-from-first-principles`、`principle-separate-before-serializing-shared-state`、`principle-sequence-verifiable-units`、`principle-subtract-before-you-add`、`principle-test-behavior-not-implementation`、`principle-type-system-discipline`

### Claude Code 迁移机制

- 适配规则　`cursor-plugins/pstack/docs/harness/claude-code.md`
- 生成脚本　`cursor-plugins/scripts/generate-pstack-harness-trees.mjs`
- 插件注册　`cursor-plugins/.claude-plugin/marketplace.json`
- 插件校验　`cursor-plugins/scripts/validate-plugins.mjs`
- CI 与生成结果检查　`cursor-plugins/.github/workflows/validate-plugins.yml`
- 文档校验　`cursor-plugins/scripts/check-pstack-docs.mjs`

### 生成产物

- 对照验证　`cursor-plugins/harness/pstack/claude-code/`

### 通用插件校验

- `cursor-plugins/schemas/marketplace.schema.json`、`cursor-plugins/schemas/plugin.schema.json`
