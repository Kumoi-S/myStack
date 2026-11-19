# Claude API Prompting Patterns

## 1. Adaptive Thinking 与 Effort

Claude Opus 5.5、Fable 5.2 的 thinking 始终开启，使用 adaptive thinking。`thinking` 决定思考模式，`effort` 决定整体工作量和推理深度，两者不是同一参数。

示例：

```python
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    thinking={"type": "adaptive", "display": "summarized"},
    output_config={"effort": "medium"},
    messages=[
        {"role": "user", "content": "审查这个设计中的并发风险，并给出可验证的修复建议。"}
    ],
)
```

要点：
- `adaptive` 是 thinking 类型，不是 effort 值。
- 不要给 Opus 5.5 / Fable 5.2 传 `thinking: disabled` 或旧式 `budget_tokens`。
- thinking token 计入 `max_tokens`。
- effort 应按自己的评测集校准；不要认为不同模型的 high 等价。

## 2. Tool Use

Claude 通过工具描述判断何时调用工具：
- 工具 schema 使用 `input_schema`；
- 说明工具用途、调用边界和副作用；
- 客户端工具由应用执行，服务端工具由 Anthropic 执行；
- 工具返回通过 `tool_result` 回传；
- 如果希望模型先调查，给出轻量明确的触发指令；
- 需要强制调用时使用 API 的 `tool_choice`，不要仅靠模糊提示词。

工具提示词示例：

```text
当问题涉及当前账户状态或外部实时数据时，先调用对应只读工具。
如果问题可以直接从当前上下文回答，不必调用工具。
任何会写入、发送、删除或触发外部动作的工具，必须遵循应用的确认策略。
```

## 3. Prompt Caching

Opus 5.5 和 Fable 5.2 的最小可缓存 prompt 长度为 512 tokens。常见策略：
- 把稳定的 system prompt、工具定义和复用文档放在前面；
- 把每轮变化的用户输入放在后面；
- 使用 cache breakpoint / `cache_control`；
- 不要随意修改已缓存的历史前缀；
- 支持的模型可通过追加 system message 在会话中改变指令，避免改写早期 system 前缀。

## 4. 结构化输出

如果应用需要稳定 JSON：
- 使用 Structured Outputs 或 strict tool schema；
- 在 schema 中明确字段、类型和 required；
- 应用端仍要验证业务约束；
- Fable 5.2 在部分 CMEK 组织配置下不支持 structured outputs；此时移除 strict/format 配置，并在应用侧校验。

## 5. 长上下文与会话前缀

- 长资料放在前部并用 XML 标签分块。
- 保留来源、文件名、时间和编号。
- 任务指令放在资料之后。
- 不要修改旧对话中已发送的历史内容来“重写 prompt”；某些模型会执行 prefix check 或使缓存失效。
- 中途更新指令时，按模型文档支持的方式追加新消息。

## 官方来源

- [Claude API usage primer](https://platform.claude.com/docs/en/claude_api_primer)
- [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Fable 5.2 migration guide](https://platform.claude.com/docs/en/models/fable-5-2/migration-guide)
