本项目用于维护个人 `~/.agents` 套件
- `sources/` 存放上游仓库和原始素材。检出仓库后，在根目录运行 `git submodule update --init --recursive` 初始化两个上游子模块
- `working/` 按来源和阶段存放适配过程的产物
- `prompting-guides/` 存放提示词参考资料
- 从仓库根目录运行 `uv sync --locked`，按 `uv.lock` 创建本机的 `.venv`。Python 版本由 `.python-version` 指定
- `releases/<版本>/` 存放独立的运行快照

## 约定
- 总是使用python脚本，通过`uv run`运行
- `working/*/<stage>/requirements.md` 是该stage的唯一事实，其余文档、工具都对该 requirements 负责，在任何时刻除非用户要求，否则 `requirements.md` 不得被修改