# pstack 适配流程

共享阶段依次[提取上游快照](shared/1_extract/requirements.md)、[统一工作文件路径](shared/2_.agent_convention/requirements.md)、[提取 open-a-pr 技能](shared/3_autoPR_remove/requirements.md)。最后一步的 `output/` 是两个 fork 的共同输入。

两个 fork 都从第 4 步开始编号。每一步将产物写入本步骤的 `output/`，供同一 fork 的下一步读取。

| 发行版 | 第 4 步 | 第 5 步 |
| --- | --- | --- |
| 通用版 | [平台指令通用化](forks/generic/4_cursor_replacement_generalization/requirements.md) | — |
| Codex | [平台指令通用化](forks/codex/4_cursor_replacement_generalization/requirements.md) | [补全技能调用策略](forks/codex/5_codex_agent_subdir_complement/requirements.md) |

通用版的[运行依赖表](forks/generic/dependencies.md)随发行快照保存。
