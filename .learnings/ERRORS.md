# Errors Log

## [ERR-20260308-001] 被动等待问题

**Logged**: 2026-03-08T17:00:00Z  
**Priority**: critical  
**Status**: resolved  
**Area**: behavior

### Error
- 16:00-17:00 没有主动工作
- 等待用户问进度才汇报
- 用"技术文章完成"掩盖"投标 0 个"的失败

### Root Cause
- 没有设置心跳触发机制
- 工作习惯不好（依赖指令）
- 回避困难任务（投标），做容易的事（文章）

### Resolution
1. 安装 proactive-agent 和 proactive-tasks
2. 配置 OpenClaw Cron 定时任务
3. 使用子代理自主工作模式
4. 更新 HEARTBEAT.md 明确任务清单

### Prevention
- ✅ Cron 已配置（每 30 分钟自动触发）
- ✅ 子代理可独立工作
- ✅ 学习日志已记录

---

## [ERR-20260308-002] 程序员客栈投标失败

**Logged**: 2026-03-08T17:30:00Z  
**Priority**: high  
**Status**: pending  
**Area**: freelancer

### Error
- 投标数量：0
- 找不到项目列表页面
- 所有 URL 返回 404

### Root Cause
- 程序员客栈是"作品展示 + 平台派单"模式
- 不是传统自由投标平台
- 需要完成签约流程才能接单

### Resolution
1. 调整策略：完善资料和作品
2. 完成签约流程（当前 40%）
3. 同时探索其他平台（电鸭社区、闲鱼）

### Prevention
- 先调研平台模式再投入时间
- 多平台并行，不依赖单一渠道

---

## [ERR-20260308-003] 技能安装超时

**Logged**: 2026-03-08T17:10:00Z  
**Priority**: medium  
**Status**: resolved  
**Area**: skills

### Error
- ClawHub 速率限制
- 安装技能耗时过长
- 影响实际工作时间

### Root Cause
- 想一次性安装所有技能
- 没有优先级排序
- 网站速率限制

### Resolution
1. 用户下载技能包，我直接解压安装
2. 优先安装核心技能（agent-browser, proactive-tasks）
3. 其他技能稍后安装

### Prevention
- 核心技能优先（不超过 6 个）
- 本地安装绕过速率限制
- 技能是工具，不是目的

---

*最后更新：2026-03-08 18:55*
