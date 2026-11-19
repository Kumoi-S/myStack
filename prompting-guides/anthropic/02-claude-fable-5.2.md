# Prompting Claude Fable 5.2

> API ID：`claude-fable-5-2`
>
> 定位：高难度研究、多日任务、长周期 Agent 工作。

## 1. 模型行为与参数

- Adaptive thinking 始终开启，不能关闭。
- 默认 effort：`high`。
- 支持 effort：`low`、`medium`、`high`、`xhigh`、`max`。
- Context window：1M tokens；最大输出：128K tokens。
- `thinking: {"type":"disabled"}` 或旧式 `thinking: {"type":"enabled","budget_tokens":...}` 不适用于该模型。
- `temperature`、`top_p`、`top_k` 等旧采样参数应按模型迁移文档处理，不要直接沿用。
- `tool_choice` 支持范围有限；模型迁移文档指出 `auto` / `none` 可用，强制 `any` 或指定 `tool` 会返回 400。

## 2. 校准 effort

从 `high` 开始，但不要认为 `xhigh` 或 `max` 一定更好：
- 普通任务：比较 low / medium / high 的质量、延迟和成本；
- 高难度长周期任务：只有评测证明有收益时再升到 xhigh；
- max 用于测量能力上限或极少数时间/成本不重要的任务；
- 不同模型的同名 effort 档位不代表相同推理量。

## 3. 完成整个任务，避免早停

Fable 5.2 可能在任务中途给出状态或报告。Agent harness 不应把每条文本消息都当作最终完成。

建议在 prompt 中明确：
- 任务包含哪些子项；
- 哪些子项已完成才算 done；
- 如果还有未完成项，继续推进；
- 只有遇到真正阻塞、超出授权范围或需要用户决策时才停；
- 最终报告必须包含已完成项、验证结果和剩余阻塞。

建议维护外部 checklist / task file，不能只依赖模型在上下文中的临时记忆。

## 4. 明确代码所有权

Fable 5.2 对“谁拥有代码”很敏感。若希望它改进现有代码结构，而不是简单复制/堆叠新代码，应明确说明这是需要它负责维护的代码库，并允许在保持行为兼容的前提下合并重复实现。

示例：

```text
这是我们负责维护的代码库。你拥有本次改动范围内代码的维护责任。
优先理解现有抽象和调用方依赖；如果发现重复逻辑，可以在保持行为兼容的前提下整理。
不要为了重构而重构；每项结构调整都必须服务于当前任务。
```

## 5. 长任务进度更新

- 对用户可见的长任务，要求定期报告当前阶段、已完成项和下一步。
- API 可按需要使用 `thinking.display` 的 updates/summarized 等选项。
- 不要让状态更新替代实际工作；更新后继续执行下一步。
- 最终报告应独立、完整，不能依赖用户阅读中间进度消息。

## 6. Subagents

在系统提示中规定：
- 哪些工作适合并行委派；
- 何时不值得启动子 Agent；
- 子 Agent 的任务边界、输入和交付格式；
- 根 Agent 必须审阅合并结果并验证。

避免让简单任务启动过多 subagents，也不要让多个 Agent 无边界地修改同一资源。

## 7. 避免“谨慎规则”累积

如果模型过度请求确认，检查 prompt 是否堆叠了大量笼统的“谨慎”“确认后再做”指令。应按风险类型写清楚：
- 只读、可逆、已授权工作：可以继续；
- 外部发送、发布、删除、付款等不可逆动作：按应用授权和审批流程处理；
- 缺少关键参数：询问；
- 不影响主任务的可逆假设：明确假设后继续。

## 8. 旧 prompt / harness 迁移

从 Fable 5.1 或 Opus 5.5 迁移时，重点检查：
- 删除要求模型输出完整私有思维链的提示；
- 移除 thinking disabled / 旧 token budget 配置；
- 不要预填 assistant 回复；
- 不要在已存会话中任意修改早期 system、tools 或历史消息；Fable 5.2 的 prefix check 失败会返回 400；
- 中途需要改变指令时，按当前文档追加新 turn / system message，而不是编辑旧前缀；
- 检查工具选择、结构化输出和 CMEK 组织配置限制。

## 9. 最终报告模板

```text
## 已完成
- [交付项与文件]

## 验证
- [测试/检查命令及结果]

## 未完成或阻塞
- [明确说明；没有则写“无”]

## 风险与后续
- [需要人工决策的事项]
```

## 官方来源

- [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2)
- [Claude Fable 5.2 model overview](https://platform.claude.com/docs/en/models/fable-5-2/overview)
- [What's new in Claude Fable 5.2](https://platform.claude.com/docs/en/models/fable-5-2/whats-new-fable-5-2)
- [Fable 5.2 migration guide](https://platform.claude.com/docs/en/models/fable-5-2/migration-guide)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
