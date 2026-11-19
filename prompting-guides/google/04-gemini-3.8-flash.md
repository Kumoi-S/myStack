# Gemini 3.8 Flash Prompting & API Guide

> 模型 ID：`gemini-3.8-flash`
>
> 官方定位：高能力 workhorse，适合软件工程、agentic tasks 和关键多步推理；高 effort 可能增加 token 消耗。

## 1. Thinking 配置

- 默认 `thinking_level`：`MEDIUM`。
- 支持：`LOW`、`MEDIUM`、`HIGH`。
- `MINIMAL` 不支持；显式设置会触发 API validation error。
- 从 3.7 / 3.6 Flash 迁移时，使用 `thinking_level`，不要继续使用旧的整数 `thinking_budget`。

## 2. 参数兼容性

以下规则来自 Gemini Enterprise Agent Platform 的开发者指南。
- 自定义 `temperature`、`top_p`、`top_k` 会被后端忽略。
- `frequency_penalty`、`presence_penalty`、`candidate_count` 不支持；传入会触发 API 错误。
- 不要依赖旧版 prefilled model turns；升级时移除不兼容的预填充 assistant/model turn。
- 请求的聊天历史不能以 `model` 角色轮次结束；空 turn 也可能被丢弃或触发校验错误。

## 3. Function Calling 严格性

Gemini 3.8 Flash 对工具调用往返有严格约束：
- `FunctionResponse` 必须对应此前的 `FunctionCall`；
- `id`、`name` 和执行次数必须匹配；
- 多模态资产应放在响应 payload 中；
- 遇到 `Malformed_Function_Call`，检查工具调用前是否有不合法的前置文本/格式；
- 不要自行改写模型生成的工具调用参数结构。

## 4. 按任务选择 Thinking Level

| Level | 适合任务 |
|---|---|
| LOW | 快速转写检索、基础元数据抽取、延迟敏感的简单任务 |
| MEDIUM | 一般视频问答、课程/会议总结、片段检索、常规 coding |
| HIGH | 密集视觉问答、快速动作/运动识别、长视频跨片段多步推理 |

如果高 effort 下模型为追求质量消耗大量 token，先评估能否降到 MEDIUM 或 LOW，而不是直接压低 `max_output_tokens` 导致截断。

## 5. 迁移清单

从 Gemini 3.7 / 3.6 Flash 迁移：
1. 更新模型 ID 为 `gemini-3.8-flash`。
2. 把 `thinking_budget` 替换为 `thinking_level`。
3. 移除 `MINIMAL`。
4. 移除 `temperature`、`top_p`、`top_k`。
5. 移除 `candidate_count`、`frequency_penalty`、`presence_penalty`。
6. 检查工具调用的 ID、name 和轮次匹配。
7. 清理不兼容的 prefilled model turns 和空历史 turn。
8. 对视频、音频、多模态请求重新运行回归评测。

## 官方来源

- [Developer's guide to Gemini 3.8 Flash](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-3-8-flash)
- [Gemini 3.8 Flash model page](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash)
- [Gemini thinking](https://ai.google.dev/gemini-api/docs/thinking)
