# Gemini Thinking Levels：质量、延迟与成本控制

## 1. 模型支持矩阵

| 模型 | 默认值 | 支持值 |
|---|---|---|
| Gemini 4 Carbon | MEDIUM | LOW / MEDIUM / HIGH |
| Gemini 4 Argon | MEDIUM | LOW / MEDIUM / HIGH |
| Gemini 4 Neon | HIGH | LOW / MEDIUM / HIGH / XHIGH |
| Gemini 4 Hydrogen | HIGH | LOW / MEDIUM / HIGH / XHIGH |
| Gemini 3.8 Flash | MEDIUM | LOW / MEDIUM / HIGH |

`MINIMAL` 不支持 Gemini 4 和 Gemini 3.8 Flash。

## 2. 选择策略

- **LOW**：简单分类、提取、低延迟对话和高吞吐任务。
- **MEDIUM**：日常交互、一般 coding、响应速度敏感的工具调用。
- **HIGH**：复杂 coding、agentic execution、多步推理和多模态知识工作。
- **XHIGH**：仅 Neon / Hydrogen 支持；用于 `HIGH` 仍无法完成的复杂、多阶段问题。

先用默认值建立基线，再对代表性数据集做 level sweep。选达到质量门槛的最低档位。

## 3. 不要用小输出上限替代降低推理等级

`max_output_tokens` 是硬上限，thinking token 也可能计入。若模型在推理中达到上限，可能返回 incomplete 状态或截断结果。要降低延迟/成本，优先评估降低 `thinking_level`，不要用过小的输出上限硬截断。

## 4. Prompting 与参数的分工

Prompt 负责告诉模型“要解决什么问题、成功标准是什么”；`thinking_level` 负责控制“允许模型花多少推理资源”。不要把两者混成一句模糊的“请非常认真思考”。

推荐：
- 给出明确目标和成功标准；
- 指定需要检查的输入和边界；
- 用 level 控制推理预算；
- 需要可审计性时要求输出关键证据、假设和验证结果；
- 用评测集选择 level，而不是只凭个别案例判断。

## 官方来源

- [Gemini thinking](https://ai.google.dev/gemini-api/docs/thinking)
- [Get started with Gemini 4](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start/get-started-with-gemini-4)
