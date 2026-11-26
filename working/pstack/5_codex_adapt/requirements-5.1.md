# 5.1 编写 cursor-codex.md

开始前确认 `../4_codex_openai_yaml/output/` 已包含上一阶段产出的 `agents/` 和 `skills/`。缺少产物就停在这里。

1. 首次运行或重跑 5.1 时，把上游的 [pstack in Claude Code](../../../sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md) 复制到本目录，命名为 `cursor-codex.md`。
2. 对照[上游 pstack 源码](../../../sources/cursor-plugins/pstack/)核查适配器的遗漏，包括 skill 调用的 playbook 和脚本。把遗漏项按原文的表格或短段落风格追加到文末。
3. 逐项对照 Stage 4 的实际产物，删去前几个阶段已处理或提取后已用不到的替换项。例如，路径若已在 Stage 2 统一，就删去对应的路径映射。
4. 将标题改为 `# pstack in Codex`，保留 Cursor 列，把 Claude Code 列改为 Codex。直接填入对应的 Codex 工具名、字段或命令，同步改写表外说明。缺少对应能力时，写明该步骤具体怎么处理。

重跑时按当前 requirements 和上述输入重新生成全文，覆盖已有人工修改。需要长期沿用的调整，由用户写入 requirements。

每次交稿都在 `cursor-codex.md` 的 frontmatter 中写入 `status: wait-for-check`。返修时读取主代理交来的临时审阅文件，对照其中的问题和本阶段 requirements 修改本轮稿件，再交给 5.2 复查。
