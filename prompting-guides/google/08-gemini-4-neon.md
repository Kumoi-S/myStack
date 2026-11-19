# Gemini 4 Neon 开发者指南

本文整理 Gemini Enterprise Agent Platform 上 `gemini-4-neon` 的使用要点。

## 提示词与推理配置

- 把任务目标、输入资料和交付要求写清楚。延迟敏感的工作流可以试用 `MEDIUM`，再用同一组任务比较耗时、质量和输出 token。
- 多步工具调用、代码生成、架构重构和复杂多模态分析可从默认的 `HIGH` 开始。用代表性任务评估提高到 `XHIGH` 的收益。
- GenerateContent 支持 `LOW`、`MEDIUM`、`HIGH`、`XHIGH`，Interactions API 使用相应的小写值。从 Gemini 3.8 Flash 或 Gemini 4 Argon 迁移时，显式选择 `MEDIUM` 可保留原来的推理级别。移除 `thinking_budget` 和 `MINIMAL`。

## 长输出与工具调用上下文

- 输入和输出共享 1,048,576 token，包括推理、工具调用和最终回复。单个前台 API 分段默认最多生成 65,536 token。需要跨分段生成时，按文档通过 `v1beta1` 使用长输出续传，并为推理和最终回答预留预算。
- 将稳定的系统指令和公共资料放在输入前缀。公共前缀达到 4,096 token 时适用隐式缓存，Neon 不支持显式缓存。
- 多轮任务保留模型返回的 thought signatures，并在压缩历史前检查上下文预算。使用视频时，默认 `media_processing="static"`，需要 agentic video 时显式启用 `media_processing="agentic"`。

## 官方来源

- [Developer's guide to Gemini 4 Neon](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-4-neon)
- [Gemini 4 Neon 模型页](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-neon)
