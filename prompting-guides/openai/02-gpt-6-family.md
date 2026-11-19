# GPT-6 Family Prompting Guide

> 覆盖 GPT-6 与 GPT-6.1。官方 `Using GPT-6` 页面是这两个版本的家族指南。

## 1. 模型选择

| 模型 | 官方定位 |
|---|---|
| GPT-6 Astra | 最复杂、要求最高的工作 |
| GPT-6.1 Sol | 较低成本的复杂工作；支持多 Agent beta |
| GPT-6.1 Terra | 视觉推理与写作 |
| GPT-6 Luna | 专注、高吞吐量任务 |
| GPT-6 Sol | GPT-6 系列模型；`none` reasoning effort 可用 |

具体模型能力、区域和服务等级以 Model Selection 和模型页面为准。

## 2. GPT-6 Astra 的 prompting 特点

官方指出 GPT-6 Astra：
- 更擅长遵循长指令，但也更容易受到可访问文件（如 `AGENTS.md`、skills）中的指令影响；
- 可能在重要信息不足时主动询问，应用应定义何时可以做合理、可逆的假设；
- 默认倾向更详细、格式化的回答；若产品需要简洁段落，应显式说明；
- 在子 Agent 委派方面，可能比工作流期望的更少，需要定义何时并行委派；
- 对 coding 任务可能做较广泛测试；提示词应说明测试范围和完成条件。

## 3. 让模型完成长任务

在任务 prompt 中说明：
- 用户的目标是什么；
- 哪些工作已被授权；
- 哪些决定必须由用户做；
- 哪些动作是不可逆的；
- 什么才算真正完成。

可以加入如下指令（按产品权限调整）：

```text
当用户明确要求执行工作时，把请求视为需要交付结果的任务。
在授权范围内持续推进，不要只停留在计划或能力确认。
对可逆、只读和已授权的工作直接执行。
只有在缺少关键参数、范围发生实质变化、存在明确阻塞或需要执行不可逆动作时才暂停。
完成后核对每一项验收标准，并报告实际验证结果。
```

## 4. 指令冲突与技能文件

GPT-6 对上下文中的 instructions 更敏感。应用加载 `AGENTS.md`、skills、项目规则文件时：
- 审查这些文件是否存在过期或冲突的规则；
- 明确用户指令与项目指导之间的优先级；
- 工具描述、文件内容和引用材料不要混成同一个指令层级；
- 对不可信文件内容明确标注为数据，而非控制指令。

## 5. 写作风格

不要依赖模型默认的风格。定义：
- 是否用 Markdown；
- 段落还是列表；
- 专业术语密度；
- 是否先给结论；
- 是否需要面向外部读者补充背景；
- 文档、邮件、消息和代码注释的不同写法。

## 6. Subagent 委派

如果 harness 提供协作工具，可规定：
- 何时适合并行化；
- 每个 subagent 的任务和输入；
- 结果如何汇总；
- 主 Agent 如何验证；
- 不要对简单、互相依赖或共享写入状态的任务盲目并行。

GPT-6.1 Sol 有 Responses Multi-agent beta 支持，使用时检查 `reasoning.context` 等兼容性配置。

## 7. Reasoning Effort 差异

官方页面列出：
- GPT-6 Astra 和 GPT-6.1 Sol 不支持 `none` reasoning effort；
- GPT-6.1 Terra、GPT-6 Sol 和 GPT-6 Luna 支持 `none`。

不要假设同一个 effort 枚举在所有型号上都可用。

## 官方来源

- [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)
- [Model selection](https://developers.openai.com/api/docs/guides/model-selection)
- [Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
