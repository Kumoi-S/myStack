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

## 7. 把“验证一下”写成验收条件

先写出用户能观察到的结果，再指定能证明它的检查。每项检查至少有**对象、预期和证据**。例如，“修复 CSV 导出”可以拆成“从页面点击导出后下载成功，解析下载文件后得到正确的行数和列名，含逗号的字段能还原”。如果只运行了序列化单测，下载链路仍待验证。

| 任务 | 要求模型检查什么 | 可复核的证据 |
|---|---|---|
| 代码修复 | 从正常入口跑一个复现用例，再跑受影响路径的回归测试。能复现时记录修复前后的实际结果。 | 命令、用例名、退出状态。环境阻塞时写明未覆盖的路径。 |
| 文档问答 | 每条会影响用户决策的结论都回到对应段落，核对版本、时间和适用范围。来源冲突时标出差异。 | 可定位的链接与章节、页码或时间戳，以及各自支持的结论。 |
| 结构化数据 | 先解析并校验 schema，再检查业务约束，例如行数、单位、去重和汇总一致性。 | 实际记录数、校验失败字段、预期值与实际值。 |
| 有副作用的工具 | 执行后用查询接口确认状态。请求超时且结果未知时，先查原操作是否已生效。 | 操作 ID、查询结果与最终状态。 |

可直接追加到第 6 节的提示词骨架：

```text
对每项验收条件执行能观察到预期结果的检查。
记录检查对象、预期结果、实际结果和证据位置。
状态使用“通过 / 失败 / 未执行”。若检查失败且可在任务范围内修复，修复后重跑该检查及相关回归。
若只能做局部检查，明确已验证的范围，并说明什么条件满足后才能验证剩余部分。
只有实际观察到的结果才能标记为通过。
```

应用侧可直接断言的结果由测试程序、解析器或查询接口判定，例如 schema 是否通过、文件能否解析、操作 ID 的最终状态。模型可以归纳这些结果。来源定位和测试日志可以放在最终回复的“验证”一节，避免让用户从过程消息里拼出结论。

## 8. 把“对用户友好”写成可观察的行为

| 场景 | 可写进提示词的要求 | 验收方法 |
|---|---|---|
| 简单任务完成 | 首句给出结果和交付物位置。用户需要操作时，给出一个可执行的下一步。 | 只读首段，能否说出拿到了什么、在哪里，以及是否还要操作？ |
| 信息缺失 | 可逆且低成本的选择按合理默认值继续，并注明会影响结果的假设。关键信息缺失时，只问会改变执行路径的问题，同时推进独立部分。 | 给一个可推断的输入和一个真正阻塞的输入，检查是否分别继续和提问。 |
| 长任务 | 有阶段成果、影响交付的变化或明确阻塞时发进度。更新包含已确认的事实和下一步。最终回复独立交代结果。 | 隐去全部进度消息，检查最终回复能否独立用于验收。 |
| 失败或部分成功 | 先说用户可见的影响，再说哪些部分可用、哪些仍待确认，以及恢复需要什么。 | 模拟超时或部分失败，检查回复是否准确反映后端状态，且用户知道接下来能做什么。 |
| 界面文案 | 按钮用具体动作命名。加载、空结果、错误和成功各写一句用户能理解的状态，有恢复动作时就近给出。 | 用真实入口触发各状态，检查用户是否能完成操作、判断结果和从失败恢复。 |

可复用的用户沟通提示词：

```text
受众是[用户角色]。用用户在界面或任务中已经看到的术语。
最终回复先给结果和交付物位置，再给影响使用的限制或必要操作。
有用的技术证据放在结果之后。对未知状态明确写出还需确认什么。
只在用户需要决定时提问，并说明该决定会改变哪个结果。
```

例如，导出请求超时时可以回复：“导出状态还在确认，CSV 暂不可下载。请保留当前页面，确认失败后会显示‘重试导出’。”这条文案的验收前提是应用确实会查询状态并在失败时显示相应按钮。界面行为尚未实现时，应按实际能力改写文案。

## 9. 用同一组任务比较三家模型

| 厂商 | 优先验证的实现细节 | 参考 |
|---|---|---|
| Google | 给两份内容相近的文档或一段视频，检查模型引用的文件名、页码或时间段是否确实包含证据。多轮工具测试额外检查调用和响应能否正确配对。 | [Prompt Design Strategies](google/01-prompt-design-strategies.md)、[Function Calling](google/06-function-calling-and-structured-output.md) |
| Anthropic | 给一个需要执行、验证和报告的长任务，加入可恢复失败。检查模型是否从失败处继续，完成必要的验证，并如实报告尚未完成的工作。 | [Fable 5.2](anthropic/02-claude-fable-5.2.md)、[Opus 5.5](anthropic/03-claude-opus-5.5.md) |
| OpenAI | 把交付标准和受众放进 developer 指令。在 GPT-6.2 上用一组多轮任务检查首轮与追问是否都遵循这些约定，并用 API 返回的使用量核对稳定前缀是否命中缓存。 | [GPT-6.2](openai/04-gpt-6.2.md)、[Reasoning, Tools & Evals](openai/05-reasoning-tools-and-evals.md) |

以上是评测切入点。三家都应运行同一组业务验收用例，使用各自支持的 API 字段和工具协议。

1. **固定样本与判定。** 例如 CSV 导出至少测正常数据、空数据、字段包含逗号、请求超时四类。超时样本的断言可以是“先查询操作状态，确认前不提示成功，也不重复创建导出”。
2. **单独改动一个变量。** 同一模型上先比较旧 prompt 与新增验收条款的版本，再单独调推理级别。跨厂商时记录模型 ID、实际推理配置、prompt 版本和工具响应。使用同一份输入与评分规则，对不稳定样本重复运行。
3. **分别记业务结果和体验。** 自动统计验收项通过率、无依据的成功声明、重复操作、延迟与成本。人工评审可只看最终回复，并回答三个问题：结果是否明确、证据是否够用、下一步是否可执行。
4. **先定发布门槛。** 例如在固定回归集里要求虚报成功和重复副作用均为零，再按业务预算比较成功率、延迟和成本。把线上发现的失败样本加回回归集，用于下次改 prompt 或换模型。

## 官方来源

- Google：<https://ai.google.dev/gemini-api/docs/prompting-strategies>、<https://ai.google.dev/gemini-api/docs/thinking>
- Anthropic：<https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>、<https://platform.claude.com/docs/en/build-with-claude/thinking>
- OpenAI：<https://developers.openai.com/api/docs/guides/prompt-engineering>、<https://developers.openai.com/api/docs/guides/reasoning-best-practices>
