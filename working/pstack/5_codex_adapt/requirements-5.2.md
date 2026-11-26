# 5.2 检查 cursor-codex.md

由新的子代理独立检查本目录的 `cursor-codex.md`。以 [5.1 的编写要求](requirements-5.1.md)、[上游适配器](../../../sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md) 和 [Stage 4 底稿](../4_codex_openai_yaml/output/) 为依据。

1. **先看两列能否逐行对照。** 每行只回答一个替换问题。左列写 Stage 4 实际使用的 Cursor 名称、字段、路径或操作，右列在同一层次给出 Codex 对应项。例如，工具名一行可写成 `Task` → `spawn_agent`。若原调用还涉及并行派发或收集结果，分别写出两边对应的操作。仅在 Codex 端才有的限制或回退紧跟对应行加注。逐行检查右列的每个动作能否在左列找到来由，也检查左列的每个条件是否都有去向。
2. **核对来源和覆盖范围。** 从每条映射找到 Stage 4 的调用点，再从实际使用的 agent、skill、playbook 和脚本反查遗漏。标出已由前序阶段处理的条目、重复项，以及与底稿行为冲突的说明。
3. **核对 Codex 侧能否照做。** 按实际调用场景核实工具名、字段、命令、路径和默认行为。缺少对应能力时，检查回退办法能否达到原步骤的目的。仍有缺口时，写清哪一步无法完成。

检查后更新 `cursor-codex.md` 的 frontmatter，正文由 5.1 负责修改。

- **通过**时写入 `status: ready-for-human`，向主代理交付映射稿并停止，等人审定。
- **未通过**时，在本轮共享的临时目录中新建一份审阅文件。按表格顺序列出问题，每项指出要修改的映射行、修改要求以及对应原文或调用点。漏项定位到 Stage 4 的具体文件和行。写完文件后标记 `status: Unqualified`，把文件的绝对路径交给主代理，请 5.1 返修。
