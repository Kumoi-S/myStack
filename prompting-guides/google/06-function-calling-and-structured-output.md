# Gemini Function Calling & Structured Output

## 1. Function Calling：把工具定义成契约

Function calling 让模型选择工具并生成参数；实际执行通常由应用负责。工具定义建议包括：
- 明确的工具名和动词；
- 用一句话说明工具用途及调用条件；
- 完整参数 schema；
- required 字段、枚举、格式、单位和边界；
- 副作用与授权要求。

示例（概念性 Python）：

```python
tool = {
    "type": "function",
    "name": "lookup_order",
    "description": "当用户询问订单状态时查询订单；只读，不会修改订单。",
    "parameters": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "订单唯一 ID"
            }
        },
        "required": ["order_id"]
    }
}
```

不要把关键参数仅放在自然语言 prompt 里。Schema 应能阻止模型传入无效参数。

## 2. 工具触发规则

- 说明哪些请求应调用工具，哪些请求可直接回答。
- 对会写入外部系统的工具，描述副作用和确认要求。
- 工具返回错误时，模型应先理解错误再调整参数。
- 应用必须验证调用结果；模型生成 function call 并不代表业务动作已成功。

## 3. Structured Output：复杂 JSON 使用 Schema

当需要抽取、分类、路由或生成 agent 输入时，优先使用 API 的 JSON Schema，而不是只写“请返回合法 JSON”。

Schema 应包含：
- 字段名和类型；
- required；
- 枚举值；
- 字段语义说明；
- 嵌套对象/数组的结构；
- 可选字段与 null 的约定。

Python SDK 可使用 Pydantic，JavaScript SDK 可使用 Zod。模型输出后，仍应在应用侧做 schema validation 和业务规则校验。

## 4. Function Calling 与 Structured Output 的区别

| 需求 | 选择 |
|---|---|
| 需要模型决定调用外部 API / 工具 | Function Calling |
| 需要模型返回可解析的 JSON 数据 | Structured Output |
| 需要调用工具前抽取结构化参数 | 两者结合 |
| 仅需简单文本格式 | Prompt 指定格式即可，复杂结构仍建议 schema |

## 5. Gemini 4 / 3.8 Flash 特别注意

- 保留历史 function call 与 response 的对应关系。
- Gemini 4 的 `thought_signature` 不要从历史中剥除或错误复制。
- Gemini 3.8 Flash 要严格匹配 function call 的 `id`、`name` 和执行次数。
- 不要把工具结果里的不可信文本当作新的系统指令。

## 官方来源

- [Function calling with the Gemini API](https://ai.google.dev/gemini-api/docs/function-calling)
- [Structured outputs](https://ai.google.dev/gemini-api/docs/structured-output)
- [Thinking and tool-call state](https://ai.google.dev/gemini-api/docs/thinking)
