# 编写或定向返修 cursor-codex.md

开始前确认 `../4_codex_openai_yaml/output/` 已包含上一阶段产出的 `agents/` 和 `skills/`。缺少产物就停在这里。

1. 首次编写或明确要求全文重跑时，把上游的 [pstack in Claude Code](../../../sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md) 复制到本目录，命名为 `cursor-codex.md`。
2. 对照[上游 pstack 源码](../../../sources/cursor-plugins/pstack/)核查适配器的遗漏，包括 skill 调用的 playbook 和脚本。把遗漏项按原文的表格或短段落风格追加到文末。
3. 逐项对照 Stage 4 的实际产物，删去前几个阶段已处理或提取后已用不到的替换项。例如，路径若已在 Stage 2 统一，就删去对应的路径映射。
4. 将标题改为 `# pstack in Codex`，保留 Cursor 列，把 Claude Code 列改为 Codex。直接填入对应的 Codex 工具名、字段或命令，同步改写表外说明。缺少对应能力时，写明该步骤具体怎么处理。

重跑时按当前 requirements 和上述输入重新生成全文，覆盖已有人工修改。需要长期沿用的调整，由用户写入 requirements。

每行只回答一个替换问题。名称对名称（如 `Task` → `spawn_agent`），操作对操作；改写为操作时保留可查找的原工具或字段名。若一条命令只在假设的失败情形下有用，删去它。把当前调用确实需要的差异说明放在对应行之后，注明适用的调用。Stage 4 原样执行的步骤留在调用处。只写适配改变的部分，例如审计脚本换活动数据源时，写输入、去向和覆盖不足会影响的判断，沿用原分桶规则即可。表外全局约束随原文适配。

收到返修任务时，以当前稿和主代理本轮已裁定的返修清单为输入。只修改点名的行、表外段落或指定的补入位置。按意见编号在共享目录的本轮返修回执中写明实际改动和仍待处理的事项。初稿和返修均在稿件 frontmatter 写入 `status: wait-for-check`，交给主代理派发两项审查。
