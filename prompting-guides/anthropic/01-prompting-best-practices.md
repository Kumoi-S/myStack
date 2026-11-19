# Claude Prompting Best Practices

> 适用：当前 Claude 模型。具体模型专属行为以对应模型指南为准。

## 1. 清楚、直接、具体

把 Claude 当作不了解你内部约定的新同事：
- 明确任务目标；
- 明确输出格式、语气和长度；
- 解释领域术语和业务背景；
- 明确“超出最低要求时”是否应该继续；
- 对不确定信息规定如何标注。

不要依赖模型从含糊措辞推断未说出的流程或质量标准。

## 2. 用 XML 标签划分 prompt

复杂 prompt 推荐使用稳定、可读的标签名，例如：

```xml
<instructions>
你负责审查以下数据，不得推测缺失字段。
</instructions>

<context>
<source_document id="A">
[文档 A]
</source_document>
<source_document id="B">
[文档 B]
</source_document>
</context>

<task>
比较 A 与 B，列出差异、来源和不确定点。
</task>

<output_format>
返回 Markdown 表格，列为：字段、文档 A、文档 B、差异、来源。
</output_format>
```

多个文件可嵌套 `<document>`，并加入 source、index、date 等元数据。

## 3. 角色与 system prompt

在 system prompt 中指定角色通常能稳定任务视角和语气。角色不应替代任务定义；角色之后仍需说明目标、输入、约束和验收标准。

## 4. 示例（Few-shot）

Few-shot 示例对格式、语气和分类边界尤其有用：
- 用 `<example>` 包裹单个示例；
- 多个示例可放在 `<examples>` 中；
- 覆盖正常输入和边界情况；
- 避免示例与规则相互矛盾。

先尝试 zero-shot；只有当模型输出不稳定时才增加示例。

## 5. 长上下文

对于大约 20K tokens 以上的长文档/数据输入：
- 把长文档和参考资料放在 prompt 前部；
- 每个文档用 XML 标签隔离；
- 明确来源和元数据；
- 把具体问题、任务指令和输出格式放在上下文之后；
- 对答案要求来源定位和不确定性标注。

## 6. 工具调用

工具调用是否发生主要受工具说明和请求内容影响：
- 工具描述应清楚说明用途和触发条件；
- 如果确实需要工具，提示“先使用工具调查再回答”通常比“总是调用所有工具”更稳妥；
- 不要对每个任务都写“有疑问就调用工具”，否则可能导致过度调用；
- 对有副作用的工具写清楚权限、审批和验证步骤。

## 7. 思考与努力程度

当前 Claude 5 系列使用 adaptive thinking；通过 `effort` 控制整体工作量。复杂任务可以提高 effort；如果模型过度思考或延迟太高，先降低 effort 并评测，不要试图用“不要思考”这类自然语言要求绕过模型的 API 限制。

## 8. 评测

对 prompt 的每次改动都应在固定数据集上做回归：
- 任务成功率；
- 事实准确率和引用正确率；
- JSON/schema 合法率；
- 工具调用精度；
- 早停/过度调用；
- 延迟、输入输出 token 和成本。

## 官方来源

- [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
- [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
