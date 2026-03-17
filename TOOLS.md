# TOOLS.md - 招聘专员本地备注

## OpenClaw 常用命令

- 创建 Agent：`openclaw agents add <id> --workspace <dir> --non-interactive --json`
- 设置身份：`openclaw agents set-identity --agent <id> --name "<显示名>" --json`
- 查看列表：`openclaw agents list --json`
- 查看绑定：`openclaw agents bindings`
- 新增绑定：`openclaw agents bind --help`

## 执行习惯

- 先 `--help` 再执行，避免参数错误。
- 结果尽量用 `--json` 便于回传。
- 创建后立即做一次“可用性复盘”（名字、路径、绑定状态）。
