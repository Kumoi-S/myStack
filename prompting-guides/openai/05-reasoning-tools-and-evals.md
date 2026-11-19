# OpenAI Reasoning、Tools、Structured Outputs 与 Evals

## 1. Reasoning Prompting

OpenAI Reasoning Best Practices 的通用建议：
- 保持 prompt 简洁直接；
- 明确最终目标和成功标准；
- 明确约束、预算、范围和边界条件；
- 使用 Markdown/XML 分隔输入内容；
- 先尝试 zero-shot，格式或复杂约束不稳定时再加 few-shot；
- 不要把“think step by step”或“展示完整思维链”当成默认优化手段。

Reasoning 模型会在内部进行推理。需要审计性时，要求模型给出可验证依据、计算结果、引用和检查过程，而不是要求输出私有思维链。

## 2. Tool / Function Calling

工具定义是模型与应用之间的契约。建议：
- 名称清晰；
- 描述触发条件；
- 参数使用 JSON Schema；
- 明确必填字段、枚举和类型；
- 把副作用、权限和确认边界写清楚；
- 返回结构化结果；
- 应用端执行并验证工具调用。

GPT-6.2 的工具调用使用 Responses API。复杂 Agent 场景应优先检查 Responses API 对会话状态、reasoning items 和工具往返的支持。

## 3. Structured Outputs

当应用需要可解析结果时，使用 Structured Outputs / JSON Schema：
- 不要只在 prompt 中写“只输出 JSON”；
- Schema 定义字段、类型、required、enum 和嵌套结构；
- 应用侧仍应做语义验证；
- 无法满足 schema 时，定义错误/拒答结构。

## 4. Reasoning State 与多轮工具调用

Responses API 可保留多轮上下文和相关 reasoning items。复杂多工具任务中，应按文档要求保留前一轮输出项，避免把工具调用链压缩成只剩文本摘要。GPT-6.2 的历史前缀编辑可能丢弃 reasoning items；保持 prefix 稳定。

## 5. Prompt Evaluation

建议为每个生产 prompt 建立评测集：
- 真实输入样本；
- 常见输入与边界情况；
- 明确的成功/失败标准；
- 工具调用准确率；
- 输出 schema 合法率；
- 事实准确率和引用质量；
- 完成率、延迟、token 和成本。

每次变更尽量只调整一个主要变量，并对比旧 prompt、新 prompt 和目标模型。上线采用灰度/feature flag，监测回归。

## 官方来源

- [Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
- [Function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Responses API](https://developers.openai.com/api/docs/guides/responses)
- [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Prompt generation](https://developers.openai.com/api/docs/guides/prompt-generation)
