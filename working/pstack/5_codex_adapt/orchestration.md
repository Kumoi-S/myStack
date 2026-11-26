# Stage 5 编排

主代理按稿件状态交接。三个子阶段分别遵循 [5.1 编写](requirements-5.1.md)、[5.2 检查](requirements-5.2.md) 和 [5.3 生成](requirements-5.3.md)。

```text
IF 首次启动或明确重跑 Stage 5
    DISPATCH 新的 5.1 子代理，传入 requirements-5.1.md、上游适配器路径和 Stage 4 底稿路径
    保留本轮 5.1 子代理 ID
    读回 cursor-codex.md，确认 status 为 wait-for-check

LOOP 从 cursor-codex.md 的 frontmatter 读回当前 status
    CASE wait-for-check
        送检当前稿

    CASE Unqualified
        IF 该稿的审阅文件已丢失
            送检当前稿
            CONTINUE

        读回审阅文件，对照 requirements-5.2.md 和每项意见引用的底稿调用点
        逐项核实改动是否必要、是否超出原 skill 的要求、改后两列是否仍在同一层次
        工具名与工具名对应，Codex 特有的限制或回退紧跟对应行加注
        IF 有意见不合理或依据尚未查明
            将该项意见和疑点交回出具意见的 5.2 子代理重审
            等待修订结论
            CONTINUE

        IF 本轮 5.1 子代理已不可恢复
            DISPATCH 新的 5.1 子代理，传入 requirements-5.1.md、同一稿件和已核实的审阅文件绝对路径
            保留接手者的 ID，供本轮后续返修使用
        ELSE
            将已核实的审阅文件绝对路径交回本轮 5.1 子代理
        返修期间保留临时文件
        等待返修，读回稿件，确认 status 为 wait-for-check

    CASE ready-for-human
        向用户交付可编辑的 cursor-codex.md，请其审定
        STOP

    CASE done
        IF 尚未收到用户的生成指令
            STOP 等待指令
        DISPATCH 新的 5.3 子代理，传入 requirements-5.3.md、人工定稿和 Stage 4 底稿路径
        按 requirements-5.3.md 核对 output/，交付核验通过的产物
        STOP

ON 送检当前稿
    选用本轮主代理、5.1 和 5.2 均可访问的临时目录
    DISPATCH 新的 5.2 子代理，传入 requirements-5.2.md、当前稿和临时目录的绝对路径
    等待检查结果，保留审阅文件路径（如有）
```
