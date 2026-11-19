# Google / Anthropic / OpenAI Prompting 差异速查

> 整理日期：2026-11-19。这里比较的是 API/开发者文档中的提示词指导，不代表三家 API 的字段可以互换。

## 1. 核心控制面

| 维度 | Google Gemini 4 / 3.8 Flash | Anthropic Opus 5.5 / Fable 5.2 | OpenAI GPT-6 / 6.1 / 6.2 |
|---|---|---|---|
| 稳定指令 | `system_instruction` | `system` | `developer` message；Responses API 也有 `instructions` |
| 推理控制 | `thinking_level`：LOW / MEDIUM / HIGH；Neon、Hydrogen 另支持 XHIGH | 自适应思考；用 `effort` 调节思考深度 | `reasoning.effort` |
| 默认值差异 | Gemini 4 Carbon / Argon 与 3.8 Flash 默认 MEDIUM；Neon / Hydrogen 默认 HIGH | Opus 5.5 默认 medium；Fable 5.2 默认 high | GPT-6.2 新集成建议从 medium 开始 |
| 结构化输出 | JSON Schema / `response_schema` | Structured Outputs / strict tool use（按模型、组织配置确认） | Structured Outputs / JSON Schema |
| 工具调用 | Function Calling；保留 `thought_signature` 等会话状态 | `tool_use` / `tool_result`；工具说明决定触发边界 | Responses API 的 tools/function calling；GPT-6.2 工具调用使用 Responses API |
| 缓存要点 | Gemini 4 隐式缓存；共享前缀至少 4,096 tokens，静态内容前置 | Prompt Caching；Opus 5.5、Fable 5.2 最小可缓存长度 512 tokens | 保持 prompt prefix 稳定；GPT-6.2 将可缓存的稳定指令放在 `input` 的第一个 developer message |

## 2. Prompt 结构建议

### Google

官方 Prompt Design Strategies 建议明确任务、定义术语、用 Markdown/XML 分隔角色/约束/上下文/任务，并显式要求输出详略。长上下文场景通常先放资料，再把具体问题放在末尾；多模态场景要明确指向图像、音频、视频或文本各自承担的任务。

### Anthropic

Anthropic 强调直接、清楚、具体；复杂 prompt 推荐使用稳定且语义明确的 XML 标签（如 `<instructions>`、`<context>`、`<examples>`）。长文档或数据集放在 prompt 前部，问题和具体指令放在后部。示例应贴近真实输入，并覆盖边界情况。

### OpenAI

把应用规则放在 `developer` message，把用户动态输入放在 `user` message。官方推荐用 Markdown 标题/列表和 XML 标签划分逻辑边界；常见 developer prompt 包含 Identity、Instructions、Examples、Context。GPT-6.2 若要利用 prompt caching，稳定指令应放在 Responses API `input` 数组的第一个 developer message，而不是只放在顶层 `instructions`。

## 3. 推理提示词不要混用

- **Gemini**：优先通过 `thinking_level` 控制质量、延迟和 token 消耗；不要用旧的 `thinking_budget`，Gemini 4 不支持 `MINIMAL`。
- **Claude**：Opus 5.5 / Fable 5.2 的 adaptive thinking 始终开启；通过 `effort` 调节，不要传旧式 `thinking: {"type":"enabled","budget_tokens":...}` 或 `disabled`。
- **GPT**：使用 `reasoning.effort`；Reasoning Best Practices 建议先写清目标和限制，不要要求模型公开逐步思维链。GPT-6.2 从 medium 开始，旧集成若使用 none/minimal，迁移时应评估 low。

## 4. 长上下文与缓存

| 厂商 | 推荐做法 |
|---|---|
| Google | Gemini 4 将输入、思考、工具和输出纳入统一 1,048,576 token 窗口；静态资料放在开头以复用 4K+ 前缀缓存。Gemini 4 不支持旧式显式 `cached_content`。 |
| Anthropic | 长文档放在前面，按 `<document>` 等标签分块并附来源/元数据；固定 system/tools 和前缀以便缓存。 |
| OpenAI | 稳定 developer 指令和可复用示例前置，动态用户内容后置；GPT-6.2 中间改写历史前缀会丢弃部分 reasoning items。 |

## 5. 工具与 Agent

跨厂商都应把工具定义写成机器可执行契约，而不是只在自然语言里描述：
- 工具名称具体、描述说明触发条件和副作用。
- 参数类型、必填字段、枚举、边界条件写入 schema。
- 说明工具何时应该用、何时不该用，以及需要用户批准的动作。
- 明确完成条件、验证步骤、错误恢复策略和最终报告格式。
- 不要把“工具调用成功”当作“业务动作成功”；应用必须执行并验证工具结果。

## 6. 最小可用 Prompt 骨架

下面是跨厂商的概念骨架；请按具体 API 的角色字段和参数改写。

```text
# Role
你是 [角色]，负责 [业务目标]。

# Objective
完成：[可验证的最终结果]。

# Context
<reference_material>
[背景资料、数据、代码、来源]
</reference_material>

# Instructions
1. [必须完成的动作]
2. [约束、边界和禁止事项]
3. [工具选择与调用规则]
4. [遇到缺失信息/错误时的处理]

# Output
- 格式：[JSON Schema / Markdown / 表格 / 文件]
- 必须包含：[字段]
- 不确定时：[说明未知，不要编造]

# Completion criteria
- [测试、校验、交付标准]
- [剩余问题或阻塞必须明确报告]
```

## 官方来源

- Google：<https://ai.google.dev/gemini-api/docs/prompting-strategies>、<https://ai.google.dev/gemini-api/docs/thinking>
- Anthropic：<https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>、<https://platform.claude.com/docs/en/build-with-claude/thinking>
- OpenAI：<https://developers.openai.com/api/docs/guides/prompt-engineering>、<https://developers.openai.com/api/docs/guides/reasoning-best-practices>
