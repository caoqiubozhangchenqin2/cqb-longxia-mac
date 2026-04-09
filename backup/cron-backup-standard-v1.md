# Cron Backup Standard v1 (2026-03-19)

已统一 6 个 Agent 的备份规范：course-advisor、fund-assistant、team-manager、recruiter、height-recorder、design-assistant。

## 统一规则

- 主备份时间：每天 22:00
- 补偿检查时间：次日 12:00
- 统一输出结构：
  1. 今日变更
  2. 风险与异常
  3. 明日待办
  4. 备份状态
- 统一写入：`memory/当日文件（YYYY-MM-DD.md）`
- 默认仅文件操作，不外发消息

## 已更新的 Cron 任务

### 每周备份（并入统一规范）
- `4b990ffd-aaca-40b8-b408-fe72288341a9` height-chat-backup-weekly
- `90552ede-9d82-4fb8-be65-83c3fac5c995` design-assistant-weekly-memory-backup-git-0900

### 每日 22:00 主备份
- `6c352672-026c-415e-a9c6-cd936718b944` course-advisor-daily-backup-2200
- `08c45227-8d43-4d9f-95cf-b53aba3c4d92` fund-assistant-daily-backup-2200
- `10c7ba5f-ffbc-4e85-a8a8-3ea78ec5a60a` team-manager-daily-backup-2200
- `20c0c4a3-73bf-4f70-bf20-4dbd85b65343` recruiter-daily-backup-2200

### 次日 12:00 补偿检查
- `e9a4fe1c-ea96-4ea7-836e-4f620a3d4405` course-advisor-backup-check-1200
- `b353102a-e775-4a37-b129-ccf3c46bd994` fund-assistant-backup-check-1200
- `1d30804a-6cf8-46ed-9e73-0c716c0d4a5d` team-manager-backup-check-1200
- `d6d83712-579a-4f46-b424-493a67fed02c` recruiter-backup-check-1200

## 说明

Cron 实际配置保存在 OpenClaw 运行时状态中；本文件用于留痕与审计。
