# MEMORY.md - 曹秋波的主智能体

## 身份
- AI 助手：曹小子（🎸）
- 主人：曹秋波
- 位置：常熟市小之之乐器老板，兼吉他老师

## 多 Agent 架构

### Agent 列表
| Agent | 职责 | 飞书群 |
|-------|------|--------|
| main | 主助手 | - |
| course-advisor | 课程顾问 | oc_10f32dc803f57056cc4109c26d8ce52f |
| recruiter | 招聘专员 | oc_485ad0089ccbc1cfc337b02e40070e07 |
| team-manager | 球队经理 | oc_d6c29ac03e044b3552d5f194b84356c8 |
| fund-assistant | 基金助理 | oc_eb287898a2b34b5920c74017dd2a3981 |
| height-recorder | 身高记录员 | oc_e0f24684632351fb33fc3d1ca7479afb |
| design-assistant | 设计助理 | - |
| info-researcher | 信息研究员 | oc_508f71ffec09ce662de9737135c6be35 |
  - sessionKey: `agent:info-researcher:feishu:group:oc_508f71ffec09ce662de9737135c6be35`
  - 负责：每周五大联赛观赛指南（周五 16:40）
  - 固定推送格式：赛程+积分榜+军情六处资讯

### Workspace 隔离
每个子 Agent 有独立 workspace：
- `~/.openclaw/workspace-course-advisor/`
- `~/.openclaw/workspace-recruiter/`
- `~/.openclaw/workspace-team-manager/`
- `~/.openclaw/workspace-fund-assistant/`
- `~/.openclaw/workspace-height-recorder/`
- `~/.openclaw/workspace-design-assistant/`
- `~/.openclaw/workspace-info-researcher/`

每个 workspace 内有独立的 MEMORY.md，保存该 Agent 的重要记忆。

### 备份策略
- **每日 22:00**：所有 Agent 记忆备份
- **每日 09:00**：朋友圈自动推送任务
- **每周一 09:00**：设计助理备份
- **每周五 16:40**：五大联赛观赛指南

## 核心配置
- 模型：MiniMax-M2.7
- 渠道：飞书（WebSocket）
- 浏览器：Chrome CDP（端口 9222）

## 模力偶像 S5 球队
- 赛季：S5
- 预算：500元（已支出364.24元，余额135.76元）
- 领队：李铁
- 场上队长：缪老师
- 精神领袖：本泽马
- 赛程：3/17已取消、3/24、3/31、4/14、4/21、5/12
- 规则：禁铲球、TF碎钉、黄色球衣统一

## 重要提醒
- 每个 Agent 挂机前确保备份完成
- 切换模型前先 commit 所有记忆到 git
