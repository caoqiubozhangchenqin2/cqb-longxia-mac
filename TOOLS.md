# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## Sports APIs

API keys 存在 `memory/api-keys.md`，调用时用这两个数据源：

- **football-data.org** — 查英超积分、赛程、球队数据
  - Base: `https://api.football-data.org/v4`
  - 示例：`GET /competitions/PL/standings`（英超积分榜）

- **TheSportsDB.com** — 查球队标志、联赛信息等
  - Base: `https://www.thesportsdb.com/api/v1/json/{API_KEY}`

---

Add whatever helps you do your job. This is your cheat sheet.
