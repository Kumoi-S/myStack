# 写法审查

逐行对照，左列照录 Stage 4 原文。先读完整左列，再决定这一行的去留。

1. **有平台写法，留行。** 工具名对工具名，技能调用只改标记。原句指定 Cursor 执行模式时，右列抄原句并删去模式，即使只差这几个字也留行。遇到具名角色字段，派发写作 Dispatch to，每个角色写作 `原名` subagent。保留原动作、对象和目的。
2. **只有通用动作，删整行。** worker、investigator 等普通称呼照样能用。确需逐行对照时才保留，右列逐字复制左列，含 Markdown、大小写和标点。
3. **每格只放一个主映射，禁用 `<br>`。** 删掉操作步骤和兜底。仅当共用的平台差异会改变实际调用时，在表外加短注。
4. **交 Markdown 意见。** 按原行号列左列、原右列和建议结果，格式问题指出违规处。末尾写已查范围和结论。复核沿用原编号，只查点名行及直接影响。稿件状态由主代理裁定。

## 人工训练样本

以下八项摘自人工批注。“原右列”是负样本，“人工结果”是正样本。格式批注只约束表格写法。样本保留人工批注原话；其中的「无需替换」在最终表中执行为删行，确要保留才原样复制左列。

### A01 · 原稿 L17

```text
左列：Open or update the todolist
原右列：`update_plan` when available, otherwise a checklist in chat.
人工结果：update_plan
```

### A05 · 原稿 L19

```text
左列：A workflow calls `/name` or “the **name** skill”
原右列：For a pstack skill, read and follow the sibling `<name>/SKILL.md` in the selected installation. Resolve project skills from the project and built-in skills from the skill catalog.
人工结果：calls $name or the **name** skill
```

### A06 · 原稿 L20

```text
左列：Search file contents
原右列：`rg -n -e <pattern> <directory>`
人工结果：无需替换
```

### A07 · 原稿 L21

```text
左列：Match file names
原右列：`rg --files --hidden -g '<glob>' <directory>`<br>When searching the selected skill root for installed skills, add `--follow` to include linked skill directories.
人工结果：无需替换
```

### A08 · 原稿 L27

```text
左列：`subagent_type: generalPurpose`
原右列：Default worker
人工结果：generalPurpose subagent
```

### A10 · 原稿 L30

```text
左列：Dispatch a `readonly: true` worker to investigate and report
原右列：Forbid writes in the brief and request a report. The brief alone cannot enforce read-only access. Compare the worktree state before and after the run.
人工结果：Dispatch a readonly subagent to investigate and report
```

### A12 · 原稿 L36

```text
左列：Resume a delegate with live state
原右列：Send the follow-up to the original worker ID using the exposed input tool, such as `send_input`.
人工结果：Send the follow-up to the original subagent
```

### A14 · 原稿 L80

```text
左列：Create a webhook routine with `update_state`
原右列：Use a configured webhook receiver and obtain its endpoint URL.<br>For make-bot-ui, configure the sender to POST to that URL with credentials scoped to the receiver. POST a harmless probe and confirm wake-up from the receiver's documented response. Without a receiver, leave the URL pending and mark wake-up unverified.
人工结果：禁止在md表格中使用<br>
```
