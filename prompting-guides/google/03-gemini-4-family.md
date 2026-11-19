# Gemini 4 Family Prompting & API Guide

> 覆盖：Gemini 4 Neon、Hydrogen、Carbon、Argon
>
> 核心来源：Google 官方 Gemini 4 家族入门和模型开发者指南。

## 1. 模型定位

| 模型 | 模型 ID | 官方定位 | 默认 thinking |
|---|---|---|---|
| Gemini 4 Neon | `gemini-4-neon` | 低延迟的高性能 coding、多步推理、多模态 agent 工作流 | HIGH |
| Gemini 4 Hydrogen | `gemini-4-hydrogen` | 日常 coding、agentic workflow、多模态分析、工具使用，强调速度和效率 | HIGH |
| Gemini 4 Carbon | `gemini-4-carbon` | 面向复杂真实任务的 frontier 模型，适合跨领域深度工作 | MEDIUM |
| Gemini 4 Argon | `gemini-4-argon` | Gemini 4 家族首发 frontier 模型，适合复杂跨领域深度工作 | MEDIUM |

Google 还提供面向防御性网络安全的 Carbon / Argon Cyber Permissive 变体。它们不是普通通用模型的完全等价替代，访问权限和默认设置应以对应模型页为准。

## 2. Thinking Level

Gemini 4 通过 `thinking_level` 控制推理深度：

| 值 | 支持模型 | 建议场景 |
|---|---|---|
| `LOW` | 全部四款 | 低延迟、高吞吐、简单任务 |
| `MEDIUM` | 全部四款 | 交互式 coding、响应速度敏感的工具调用 |
| `HIGH` | 全部四款 | 多步推理、复杂 coding、agentic execution、多模态知识工作 |
| `XHIGH` | Neon、Hydrogen | `HIGH` 仍无法满足的高难度、多阶段任务 |

- Neon / Hydrogen 默认 `HIGH`。
- Carbon / Argon 默认 `MEDIUM`。
- `MINIMAL` 不支持；旧的 `thinking_budget` 参数会导致错误。
- 不要默认把所有请求设为 `XHIGH`。先在代表性任务上比较质量、延迟和 token，再选满足质量要求的最低档位。

示例（Python Gen AI SDK）：

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-4-neon",
    contents="审查这个支付重试队列中的竞态条件，并给出最小修复。",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level=types.ThinkingLevel.HIGH
        )
    ),
)
print(response.text)
```

## 3. Gemini 4 的 Prompting 原则

1. 把稳定规则放在 `system_instruction`，把本轮任务和数据放在 `input` / `contents`。
2. 用 Markdown 或 XML 明确分隔角色、任务、上下文、约束和输出。
3. 对长任务给出验收条件、需要检查的文件/数据、测试方式和停止条件。
4. 对工具使用写明触发条件、参数约束和副作用。
5. 多模态请求明确说明每种输入的用途；视频理解若要模型进行 agentic 视频分析，需按 API 文档显式开启。
6. 不要要求模型输出私有的逐 token 思维过程；需要审计时要求证据、结论、假设和验证结果。

## 4. API 行为与迁移注意事项

### 统一 Token 窗口

Gemini 4 使用统一的 1,048,576-token 窗口，输入、thinking、function call 和最终输出共同占用。默认单次同步输出上限通常为 65,536 tokens；Carbon / Argon 的非流式直接 HTTP 请求默认单次输出上限为 32,768 tokens。更长输出需要使用官方支持的 long decode / continuation 方式，并确认 SDK/API 版本。

### Sampling 参数

Gemini 4 会忽略自定义的 `temperature`、`top_p`、`top_k`。不要通过这些参数调节模型输出；优先使用 `thinking_level` 和结构化输出。

### Context Cache

Gemini 4 使用隐式上下文缓存。共享 prompt 前缀达到 4,096 tokens 或以上时可受益：
- 把稳定的系统指令、代码仓库资料、长文档放在前面。
- 把每轮变化的用户问题放在后面。
- 不要沿用 Gemini 3 的显式 `cached_content` 配置；Gemini 4 的迁移说明要求移除这类引用。

### Thought Signature

Gemini 4 对多轮和并行工具调用的 `thought_signature` 更严格：
- 保留历史响应中的签名，不要在会话历史中剥除；
- 并行调用时，签名只应保留在文档规定的首个 `functionCall` part 上；
- 不要把同一签名复制到并行兄弟调用；
- Function response 必须与此前调用严格对应。

### Agentic Video

视频上传默认采用静态处理。若需要 agentic video understanding，应按照当前 API 文档将 `media_processing` 设置为 `agentic`，并在评测中验证准确性、成本和延迟。

## 5. Gemini 4 Prompt 模板

```text
# Role
你是 [具体角色]，负责 [明确职责]。

# Objective
完成 [可验证的目标]。

# Context
<reference_material>
[仓库、文档、数据、图像或视频]
</reference_material>

# Plan and constraints
- 先检查哪些信息：[范围]
- 允许使用的工具：[工具]
- 不得执行：[禁止事项]
- 缺失信息处理：[询问/做可逆假设/报告未知]

# Task
[具体任务和步骤]

# Output
[文件/JSON/Markdown/表格]
必须包含：[字段或交付物]

# Completion criteria
- [验证步骤]
- [验收条件]
- [最终报告内容]
```

Neon 的参数与迁移要点见 [Gemini 4 Neon](08-gemini-4-neon.md)。

## 官方来源

- [Get started with Gemini 4](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start/get-started-with-gemini-4)
- [Developer's guide to Gemini 4 Neon](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-4-neon)
- [Gemini 4 Neon model page](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-neon)
- [Developer guide: Gemini 4 Hydrogen](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-4-hydrogen)
- [Developer guide: Gemini 4 Carbon](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-4-carbon)
- [Developer guide: Gemini 4 Argon](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-4-argon)
- [Thinking levels](https://ai.google.dev/gemini-api/docs/thinking)
- [Text generation](https://ai.google.dev/gemini-api/docs/text-generation)
