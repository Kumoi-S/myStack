# 5.2 按 cursor-codex.md 生成 Codex 产物

收到人的执行指令后，先确认本目录的 `cursor-codex.md` 已由人审定，frontmatter 为 `status: done`。未审定时停止。

以 `../4_codex_openai_yaml/output/` 为底稿，按定稿逐项修改对应的 agent、skill、playbook 和脚本，将完整结果写入本阶段的 `output/`。核对受影响的调用点和文件引用，确保它们使用定稿中的名称、路径和处理方式。
