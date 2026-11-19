# Anthropic Claude Prompting Guides

> 整理日期：2026-11-19

## 模型矩阵

| 模型 | API ID | Context | Max output | Thinking | 默认 effort |
|---|---|---:|---:|---|---|
| Claude Opus 5.5 | `claude-opus-5-5` | 1M | 128K | Adaptive，始终开启 | `medium` |
| Claude Fable 5.2 | `claude-fable-5-2` | 1M | 128K | Adaptive，始终开启 | `high` |

两个模型都通过 `effort` 控制推理深度。不要把旧模型的 thinking token budget、默认 effort 或 prompt 模板原样迁移。

## 阅读导航

1. [Prompting Best Practices](01-prompting-best-practices.md)：通用 prompt 结构、XML、示例、长上下文和工具触发。
2. [Claude Fable 5.2](02-claude-fable-5.2.md)：长任务、早停、代码所有权、进度更新、subagents、审批和迁移。
3. [Claude Opus 5.5](03-claude-opus-5.5.md)：effort 校准、始终开启的 adaptive thinking、长任务 Agent harness。
4. [API Prompting Patterns](04-api-prompting-patterns.md)：thinking、effort、tool use、prompt caching 和 API 限制。

## 官方来源

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2)
- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
- [Claude API usage primer](https://platform.claude.com/docs/en/claude_api_primer)
- [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Fable 5.2 migration guide](https://platform.claude.com/docs/en/models/fable-5-2/migration-guide)
- [Opus 5.5 model overview](https://platform.claude.com/docs/en/models/opus-5-5/overview)
