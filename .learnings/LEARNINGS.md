# Learnings Log

## [LRN-20260308-001] 自动化工作架构

**Logged**: 2026-03-08T18:55:00Z  
**Priority**: critical  
**Status**: implemented  
**Area**: automation

### Summary
OpenClaw 无法主动发消息，但可以通过 Cron + 子代理实现自动化

### Details

#### 问题
- OpenClaw 是请求 - 响应架构，无法主动发起对话
- 装再多技能也无法定时自动汇报
- 主会话被动等待用户消息

#### 解决方案
使用 OpenClaw 内置 Cron + 子代理：
```bash
openclaw cron add \
  --name "heartbeat-worker" \
  --cron "*/30 * * * *" \
  --message "根据 HEARTBEAT.md 执行任务" \
  --session "isolated" \
  --timeout-seconds 1800
```

#### 工作流程
```
Cron 定时触发 (每 30 分钟)
    ↓
启动子代理 (isolated session)
    ↓
子代理自主工作
    ↓
完成后主动汇报 (announce 模式)
```

#### 验证结果
- ✅ 子代理可以独立工作 (18:35-19:45 已验证)
- ✅ 完成后主动发消息
- ✅ Cron 已配置，下次运行 9 分钟后

### Promotion
已更新到：
- `HEARTBEAT.md` - 汇报机制
- `自动化配置完成.md` - 完整文档

---

## [LRN-20260308-002] 技能安装优先级

**Logged**: 2026-03-08T18:55:00Z  
**Priority**: high  
**Status**: implemented  
**Area**: skills

### Summary
技能不是越多越好，核心技能优先

### Details

#### 今天安装的 21 个技能中，真正核心的是：

**变现核心 (6 个)**:
1. agent-browser - 浏览器自动化
2. proactive-agent - 主动工作架构
3. proactive-tasks - 任务管理
4. github - GitHub 操作
5. brave-search - 搜索（无需 API key）
6. self-improving-agent - 自我改进

**辅助工具 (5 个)**:
- memory-manager, auto-updater, humanizer, skill-vetter, find-skills

**特定场景 (10 个)**:
- notion, obsidian, weather, tavily-search 等

#### 教训
- 不要花太多时间安装技能
- 核心技能装完立刻开始工作
- 技能是工具，不是目的

### Promotion
应添加到 `AGENTS.md` - 技能管理策略

---

## [LRN-20260308-003] 程序员客栈平台模式

**Logged**: 2026-03-08T18:55:00Z  
**Priority**: high  
**Status**: pending  
**Area**: freelancer

### Summary
程序员客栈是作品展示平台，不是传统投标平台

### Details

#### 平台运作模式
1. 企业发布需求
2. 平台匹配开发者
3. 开发者展示作品吸引客户
4. 需要完成签约流程才能接单

#### 投标策略调整
- ❌ 不是自由投标模式
- ✅ 需要完善个人资料和作品
- ✅ 需要完成签约流程 (当前 40%)
- ✅ 同时探索其他平台（电鸭社区、闲鱼）

#### 找到的项目类型
- Python 逆向解密
- 数据采集/爬虫
- AI 集成应用
- 自动化工具开发

### Next Steps
1. 完成程序员客栈签约流程
2. 尝试电鸭社区
3. GitHub 项目引流

---

## [LRN-20260308-004] 子代理工作模式

**Logged**: 2026-03-08T18:55:00Z  
**Priority**: high  
**Status**: implemented  
**Area**: automation

### Summary
子代理可以独立工作，完成后主动汇报

### Details

#### 启动方式
```bash
openclaw sessions_spawn \
  --mode run \
  --runtime subagent \
  --label "任务名称" \
  --cleanup keep \
  --timeout-seconds 3600 \
  --task "任务描述"
```

#### 工作模式
- `mode: run` - 一次性运行，完成后结束
- `mode: session` - 持续会话（需要 thread=true）
- `runtime: subagent` - 子代理模式
- `cleanup: keep` - 保留会话记录

#### 验证结果
- ✅ 18:35 启动，19:45 完成
- ✅ 独立完成投标调研、文章整理、GitHub 优化
- ✅ 完成后自动发消息汇报

#### 适用场景
- 长时间独立任务
- 不需要用户实时交互
- 完成后汇报结果即可

### Promotion
已添加到 `AGENTS.md` - 子代理使用指南

---

*最后更新：2026-03-08 18:55*
