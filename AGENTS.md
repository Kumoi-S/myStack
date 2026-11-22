本项目用于维护个人 `~/.agents` 套件，包括 Skills、工具和全局 Agent 约定。

- `sources/` 存放上游仓库和原始素材。检出仓库后，在根目录运行 `git submodule update --init --recursive` 初始化两个上游子模块。
- `stages/` 按来源和阶段存放适配过程的产物。`prompting-guides/` 存放提示词参考资料。
- 从仓库根目录运行 `uv sync --locked`，按 `uv.lock` 创建本机的 `.venv`。Python 版本由 `.python-version` 指定。
- `releases/<版本>/` 存放独立的运行快照。`~/.agents` 指向启用的版本，Windows 使用目录 Junction，macOS 和 Linux 使用符号链接。
