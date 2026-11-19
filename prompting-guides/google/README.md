# Google Gemini Prompting Guides

> 整理日期：2026-11-19

## 模型范围

| 模型 | 模型 ID | 默认 thinking | 支持的 thinking level | 典型定位 |
|---|---|---:|---|---|
| Gemini 4 Neon | `gemini-4-neon` | HIGH | LOW / MEDIUM / HIGH / XHIGH | 低延迟的高性能 coding、多步推理和多模态 agent 工作流 |
| Gemini 4 Hydrogen | `gemini-4-hydrogen` | HIGH | LOW / MEDIUM / HIGH / XHIGH | 日常 coding、agentic workflow、多模态分析和工具使用，强调速度/效率 |
| Gemini 4 Carbon | `gemini-4-carbon` | MEDIUM | LOW / MEDIUM / HIGH | 复杂真实任务的 frontier 模型，适合深度工作 |
| Gemini 4 Argon | `gemini-4-argon` | MEDIUM | LOW / MEDIUM / HIGH | Gemini 4 家族首发 frontier 模型，面向复杂跨领域任务 |
| Gemini 3.8 Flash | `gemini-3.8-flash` | MEDIUM | LOW / MEDIUM / HIGH | 通用 workhorse，软件工程、agentic task、多步推理和视频理解 |

> `MINIMAL` 不适用于 Gemini 4 和 Gemini 3.8 Flash。Gemini 4 Neon / Hydrogen 才支持 `XHIGH`。

## 阅读导航

1. [Prompt Design Strategies](01-prompt-design-strategies.md)：通用提示词结构、任务拆分、示例、上下文和多模态。
2. [Agentic System Instructions](02-agentic-system-instructions.md)：系统指令、工具边界、完成条件、错误恢复。
3. [Gemini 4 Family](03-gemini-4-family.md)：四款 Gemini 4 模型差异、thinking、缓存、token 和迁移注意事项。
4. [Gemini 3.8 Flash](04-gemini-3.8-flash.md)：模型专属行为、参数兼容性和迁移清单。
5. [Thinking Levels](05-thinking-levels.md)：推理深度与成本/延迟的权衡。
6. [Function Calling & Structured Output](06-function-calling-and-structured-output.md)：工具 schema 与 JSON Schema。
7. [Multimodal Prompting](07-multimodal-prompting.md)：图像、音频、视频和文件输入。
8. [Gemini 4 Neon](08-gemini-4-neon.md)：官方独立开发者指南的提示词、推理级别与长输出要点。

## 官方来源

- [Gemini Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Get started with Gemini 4](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start/get-started-with-gemini-4)
- [Gemini thinking](https://ai.google.dev/gemini-api/docs/thinking)
- [Text generation / system instructions](https://ai.google.dev/gemini-api/docs/text-generation)
- [Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [Structured outputs](https://ai.google.dev/gemini-api/docs/structured-output)
- [Files API](https://ai.google.dev/gemini-api/docs/files)
- [Developer guide: Gemini 4 Hydrogen](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-4-hydrogen)
- [Developer guide: Gemini 4 Carbon](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-4-carbon)
- [Developer guide: Gemini 4 Argon](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-4-argon)
- [Developer guide: Gemini 3.8 Flash](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-3-8-flash)
- [Developer's guide to Gemini 4 Neon](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-4-neon)
- [Gemini 4 Neon model page](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-neon)
