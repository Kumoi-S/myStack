# 5.1 编写 cursor-codex.md

开始前确认 `../4_codex_openai_yaml/output/` 已包含上一阶段产出的 `agents/` 和 `skills/`。缺少产物就停在这里。

1. 首次编写时，把上游的 [pstack in Claude Code](../../../sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md) 复制到本目录，命名为 `cursor-codex.md`。
2. 对照[上游 pstack 源码](../../../sources/cursor-plugins/pstack/)核查适配器的遗漏，包括 skill 调用的 playbook 和脚本。把遗漏项按原文的表格或短段落风格追加到文末。
3. 逐项对照 Stage 4 的实际产物，删去前几个阶段已处理或提取后已用不到的替换项。例如，路径若已在 Stage 2 统一，就删去对应的路径映射。
4. 将标题改为 `# pstack in Codex`，保留 Cursor 列，把 Claude Code 列改为 Codex。直接填入对应的 Codex 工具名、字段或命令，同步改写表外说明。缺少对应能力时，写明该步骤具体怎么处理。

在文档 frontmatter 中写入 `status: ready-for-human`，然后停止，等人直接编辑并改为 `status: done`。重跑时保留已有人工修改。用 Git 核对自上次审定以来的上游源码和 Stage 4 产物，映射未变就沿用原稿和状态。有变化只更新受影响的条目，交人复审。
