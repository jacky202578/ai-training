# AGENTS.md — AI交付管理能力培训（代码库手册）

> 代码工（Codex / Claude Code）进本仓库必读。角色通用职责在全局层（Codex→`~/.codex/AGENTS.md`、Claude Code→`~/.claude/CLAUDE.md`，已建好），这里只写本项目差异。**裸奔（缺本文件）即违规。**

## 项目是什么

AI 交付管理能力培训（需求单 REQ-2026-008），目标学员：工厂非技术管理人员；训练场地：8D 工作台 + 气泡图。

## 技术栈

- 前端：`src/index.html` 钉钉 H5 单文件 SPA
- 后端：`src/api.php` 服务端进度 API
- 内容：`content/` JSON 驱动课程内容（改内容改 JSON，不改代码）

## 目录结构

```
src/      前端 SPA + api.php
content/  JSON 课程内容
docs/     文档
deploy/   部署脚本
```

## 代码铁律

1. **只读不写**：vault 是唯一真相源，本仓库不复制文档
2. **内容与代码分离**：课程内容一律走 `content/*.json`，不硬编码进前端
3. **不碰生产**：开发生产物理隔离，改生产走 DP-006 变更单
4. **commit=push**：提交后立即推送，禁 commit 不 push
