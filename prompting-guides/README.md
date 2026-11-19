# Prompting Guides 汇编

> **整理日期：2026-11-19**
>
> **语言：中文整理 + 英文官方术语**
>
> **范围：Google Gemini、Anthropic Claude、OpenAI GPT 的模型专属 Prompting Guide 与开发者/API 文档**

本目录不是厂商文档的逐字镜像，而是基于官方文档编写的中文要点、模型差异、API 注意事项和可复用提示词模式。每篇文档末尾均列出官方原始来源，建议在实施前打开原文确认最新参数和平台可用性。

## 厂商目录

- [`google/`](google/README.md)：Gemini 4（Neon、Hydrogen、Carbon、Argon）、Gemini 3.8 Flash、Prompt Design、Thinking、Function Calling、Structured Output、多模态输入。
- [`anthropic/`](anthropic/README.md)：Claude Opus 5.5、Claude Fable 5.2、通用 Prompting Best Practices、Adaptive Thinking、Effort、Tool Use、Prompt Caching。
- [`openai/`](openai/README.md)：GPT-6、GPT-6.1、GPT-6.2、Prompt Engineering、Reasoning、Responses API、Tools、Structured Outputs、Prompt Caching、Evals。

## 模型范围与官方文档

| 厂商 | 模型系列 | 官方文档状态 / 备注 |
|---|---|---|
| Google | Gemini 4 Neon / Hydrogen / Carbon / Argon | 官方 Gemini 4 家族指南列出四款模型，各有独立开发者指南 |
| Google | Gemini 3.8 Flash | 有独立开发者指南；`thinking_level` 默认 `MEDIUM` |
| Anthropic | Claude Opus 5.5 | 有独立模型专属 prompting guide；自适应思考始终开启，默认 effort 为 `medium` |
| Anthropic | Claude Fable 5.2 | 有独立模型专属 prompting guide；自适应思考始终开启，默认 effort 为 `high` |
| OpenAI | GPT-6 | 官方 `Using GPT-6` 页面包含模型行为、迁移和 prompting best practices |
| OpenAI | GPT-6.1 | **未找到独立的 GPT-6.1 专属 Prompting Guide**；官方 `Using GPT-6` 页面明确覆盖 GPT-6 与 GPT-6.1，另有 GPT-6.1 模型差异说明 |
| OpenAI | GPT-6.2 | 有独立 `Using GPT-6.2` 指南，覆盖 Astra 与 Sol |

## 推荐阅读顺序

1. 写提示词时，先读[怎样给模型写提示词](prompt-writing-guide.md)。里面有三家共用的写法、可直接改用的中文示例和各型号的注意事项。
2. 需要进一步了解某款模型时，从对应厂商的 README 进入型号指南。
3. 开发 API 应用时，再查阅工具调用、结构化输出、缓存和评测的专题文档。

## 使用注意

- **模型参数不要跨厂商照搬。** `thinking_level`、`reasoning.effort`、Claude `effort` 的枚举和语义并不相同。
- **模型默认值会变。** 本次复核于 2026-11-19 抽查了官方型号指南、关键 API 参数和迁移说明；线上部署应再次核对模型 ID、API 版本、参数支持和地区可用性。
- **不要把旧模型技巧无条件迁移。** 例如 Gemini 4 与 Gemini 3 的 token 预算、缓存和 `thought_signature` 规则不同；Claude 5.2 不接受旧式手动 thinking budget；GPT-6.2 对 Responses API 的指令位置和 prompt cache 有专门要求。
- **优先做评测。** 把本文的建议作为起始假设，用真实输入、成功标准、回归集和成本/延迟指标验证。

## 目录约定

- `README.md`：导航、范围和状态。
- `01-...md`：通用指南或模型专属指南。
- 每篇文档的“官方来源”列出对应原文，便于追踪和更新。
