# OpenAI GPT Prompting Guides

> 整理日期：2026-11-19

## 模型范围

| 系列 | 模型 ID / 变体 | 官方 prompting guide |
|---|---|---|
| GPT-6 | `gpt-6-astra`、`gpt-6-sol`、`gpt-6-luna` | `Using GPT-6` |
| GPT-6.1 | `gpt-6.1-sol`、`gpt-6.1-terra` | 没有找到单独的 GPT-6.1 专属 Prompting Guide；`Using GPT-6` 明确覆盖 GPT-6 与 GPT-6.1 |
| GPT-6.2 | `gpt-6.2-astra`、`gpt-6.2-sol` | `Using GPT-6.2` |

## 阅读导航

1. [Prompt Engineering](01-prompt-engineering.md)：developer/user 分层、Markdown/XML、示例、prompt 版本化和缓存。
2. [GPT-6 Family](02-gpt-6-family.md)：GPT-6 / GPT-6.1 的模型行为、长任务、工具和子 Agent。
3. [GPT-6.1 Notes](03-gpt-6.1-notes.md)：GPT-6.1 独立指南缺失说明及已确认差异。
4. [GPT-6.2](04-gpt-6.2.md)：Astra / Sol 的专属 prompting、Responses API、推理 effort 和缓存变化。
5. [Reasoning, Tools & Evals](05-reasoning-tools-and-evals.md)：推理模型提示、工具 schema、结构化输出和评测。

## 特别注意

- GPT-6.2 工具调用应使用 Responses API。
- GPT-6.2 新集成建议从 `reasoning.effort="medium"` 开始。
- GPT-6.2 中稳定指令应放在 Responses API `input` 数组最前面的 developer message；顶层 `instructions` 会追加在 input 之后，不适合作为可缓存的稳定前缀。
- GPT-6.2 中途编辑历史前缀可能导致 Responses API 丢弃 reasoning items。
- OpenAI 文档指出 reusable prompt objects 正在弃用：prompt creation 自 2026-06-03 起逐步降级，`v1/prompts` 计划于 2026-11-30 关闭。新项目建议在应用代码中管理 prompt。

## 官方来源

- [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)
- [Using GPT-6.2](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.2-astra)
- [Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
- [Prompt generation](https://developers.openai.com/api/docs/guides/prompt-generation)
- [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [Responses API](https://developers.openai.com/api/docs/guides/responses)
