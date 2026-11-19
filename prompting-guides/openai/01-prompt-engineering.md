# OpenAI Prompt Engineering Guide

> 适用：OpenAI API；模型专属行为请继续参考 GPT-6 / GPT-6.2 页面。

## 1. Developer 与 User 分层

- `developer` message：应用规则、业务逻辑、身份、工具调用规则和输出约束，优先级高于 user。
- `user` message：用户本轮输入和动态数据。
- `assistant` message：模型输出和多轮对话内容。

可以把 developer prompt 看成函数定义，把 user prompt 看成传入参数。不要让用户动态数据覆盖应用的稳定规则。

## 2. 推荐 Developer Prompt 结构

官方文档给出的常见结构：

1. **Identity**：助手的目的、职责和沟通风格。
2. **Instructions**：必须遵循的规则、不能做的事、工具调用方式。
3. **Examples**：典型输入和理想输出。
4. **Context**：本轮需要的背景资料；具体位置可按任务调整。

示例：

```text
# Identity
你是一个负责审阅采购合同的分析助手。

# Instructions
- 只根据提供的合同和政策文件回答。
- 对每项结论给出来源条款。
- 不确定时标记“资料不足”。
- 不提供法律意见。

# Examples
<example>
<input>合同付款期限为 30 天。</input>
<output>付款期限：30 天；来源：第 4.2 条。</output>
</example>

# Context
<policy>
[公司采购政策]
</policy>
```

## 3. Markdown 与 XML

Markdown 标题和列表有助于表达层级；XML 标签适合隔离引用文档、用户输入和结构化上下文。两者可以组合，但要保持一致。

常用标签：
- `<context>`：背景资料；
- `<user_query>`：用户问题；
- `<reference_document>`：参考文件；
- `<example>` / `<examples>`：示例；
- `<constraints>`：约束；
- `<output_format>`：输出格式。

## 4. Few-shot 示例

少量示例可以教模型分类标准、输出格式和风格：
- 展示多样输入；
- 覆盖边界情况；
- 保证示例与规则一致；
- 先试 zero-shot，必要时再加示例。

## 5. Prompt 版本管理

官方当前文档建议：
- 把生产 prompt 存在应用代码中；
- 使用 typed arguments / schema 注入动态值；
- 把 prompt builder 放在对应业务模块；
- 加代表性 fixtures、单元测试和 evals；
- 通过正常发布流程、feature flag 分阶段上线。

文档注明 reusable prompt objects 正在弃用，`v1/prompts` 计划于 2026-11-30 关闭。新项目不建议继续依赖 prompt object ID。

## 6. Prompt Caching

- 稳定的 developer instructions 放在 input 的前部；
- 复用示例和参考资料放在变化的 user input 前；
- 保持公共前缀不变；
- 不要为了每轮任务而重写整段稳定指令。

GPT-6.2 对 Responses API 顶层 `instructions` 的位置有特别行为，参见 [GPT-6.2 指南](04-gpt-6.2.md)。

## 官方来源

- [OpenAI Prompt Engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [Prompt generation](https://developers.openai.com/api/docs/guides/prompt-generation)
- [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
