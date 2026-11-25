# pstack 通用版运行依赖

当前条目来自适配规格，发版时按实际产物核对并补全。

| 类别 | 环境、能力或工具 | 适用条件 |
| --- | --- | --- |
| 本机 | Git，支持 worktree、rebase 和 merge | open-a-pr 工作流。无远端时使用本地合并。 |
| 本机 | 已配置的 `gh` 或 `origin` CLI | 需要创建远端 PR 且会话未提供 PR 工具时，使用与仓库匹配的 CLI。 |
| Harness | 支持用户显式调用技能 | 用户调用 open-a-pr 时。 |
