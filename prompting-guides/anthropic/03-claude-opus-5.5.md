# Prompting Claude Opus 5.5

> API ID：`claude-opus-5-5`
>
> 定位：长时间 Agentic Coding、复杂知识工作、系统工程、视觉密集型工作流。

## 1. 模型行为与默认值

- Adaptive thinking 始终开启，不能通过 `thinking: {"type":"disabled"}` 关闭。
- 默认 effort：`medium`。
- Context window：1M tokens；最大输出：128K tokens。
- Opus 5.5 的 `medium` 在 Anthropic 的部分内部评测中可达到或超过旧 Opus 模型更高 effort 的表现；不要直接继承旧模型 effort 配置。
- Thinking token 计入 `max_tokens`，即使 API 不显示完整 thinking 内容。

## 2. Effort 校准

推荐：
1. 从 `medium` 开始；
2. 对真实任务集测试 low / medium / high；
3. 只有在确实提升质量时才使用 xhigh / max；
4. 如果成本或延迟偏高，优先降低 effort；
5. 为长 Agent turn 留出足够大的 `max_tokens`，避免 thinking 占用预算后截断最终回答。

Opus 5.5 不支持旧式 thinking disabled。若从关闭 thinking 的旧 prompt 迁移：
- 先试 low；
- 删除要求把内部推理写进最终答案的旧指令；
- 通过 API 的 summarized thinking 等方式获取可展示的摘要（如确有需要）；
- 不要依赖自然语言“不要思考”覆盖 API 行为。

## 3. 长时间无人值守 Agent

Opus 5.5 可能发出文本状态更新并以 `end_turn` 结束当前回合，但这不一定表示所有任务项已完成。

Harness 建议：
- 用 checklist / todo 工具记录任务项；
- 在 system prompt 中写明完成条件；
- 当任务清单仍有未完成项且没有阻塞时，发送简短续作消息；
- 对后台命令和 subagent 等待其结果返回后再判断完成；
- 自动续作应设置上限，避免无限循环；
- 保留对高风险、不可逆操作的人工确认。

示例续作消息：

```text
任务清单仍有两项未完成：迁移剩余两个 endpoint，并更新对应测试。
继续完成它们。如果存在阻塞，请指出具体原因；否则不要只汇报计划。
```

## 4. 进度更新与最终报告

长任务建议同时定义：
- 进度更新的频率和内容；
- 最终报告结构；
- 哪些状态属于“继续工作”，哪些状态属于“已完成”；
- 哪些情况必须等待用户。

最终报告应说明做了什么、发现了什么、验证了什么、还需要用户做什么。不要把中间推理缩写直接带入最终交付。

## 5. 视觉与复杂输入

Opus 5.5 在图表、流程图、截图、布局和 computer use 任务上有较强能力。提示词应明确：
- 要读取的对象/区域；
- 空间关系（箭头连接、图层顺序、位置变化）；
- 多张图或多个版本之间的比较方式；
- 是否需要标注不确定性；
- 是否允许使用视觉工具或计算工具。

不要把视觉任务简化为“总结图片”；明确要从图片中得到什么结论。

## 6. 推荐 Agent Prompt 骨架

```text
你是负责本任务的工程 Agent。

目标：
[可验证的交付结果]

范围：
[代码库/文件/系统/数据]

执行规则：
- 先检查现有实现与约定。
- 对已授权、可逆的工作主动推进。
- 对不可逆的外部动作遵循审批边界。
- 使用工具时验证工具结果。
- 维护任务清单；有未完成项时不要只给总结。

完成条件：
- [功能条件]
- [测试条件]
- [交付条件]

最终报告：
- 改动内容
- 验证方式和结果
- 未完成项 / 阻塞
- 风险与需用户决策事项
```

## 官方来源

- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
- [Claude Opus 5.5 model overview](https://platform.claude.com/docs/en/models/opus-5-5/overview)
- [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
