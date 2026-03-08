# OpenClaw 使用手册 🦞

> _"EXFOLIATE! EXFOLIATE!"_ — A space lobster, probably

**版本**: 2026.2.26  
**最后更新**: 2026-03-08

---

## 目录

1. [简介](#第 1 章简介)
2. [快速开始](#第 2 章快速开始)
3. [核心概念](#第 3 章核心概念)
4. [CLI 命令详解](#第 4 章 cli 命令详解)
5. [技能系统](#第 5 章技能系统)
6. [工具系统](#第 6 章工具系统)
7. [通道配置](#第 7 章通道配置)
8. [高级功能](#第 8 章高级功能)
9. [配置详解](#第 9 章配置详解)
10. [最佳实践](#第 10 章最佳实践)
11. [附录](#附录)

---

# 第 1 章 简介

## 1.1 OpenClaw 是什么

OpenClaw 是一个**自托管的多通道网关**，用于连接你喜爱的聊天应用（WhatsApp、Telegram、Discord、飞书、QQ、钉钉、企业微信等）与 AI 编码助手。它运行在你自己的机器（或服务器）上，成为消息应用与随时可用的 AI 助手之间的桥梁。

**核心理念**: 从口袋里发消息，获得 AI 代理响应。

## 1.2 核心功能和特点

### 主要特性

- **自托管**: 运行在你的硬件上，遵循你的规则
- **多通道**: 一个网关同时服务 WhatsApp、Telegram、Discord、飞书等多个平台
- **Agent 原生**: 专为编码助手设计，支持工具使用、会话管理、记忆系统和多代理路由
- **开源**: MIT 许可，社区驱动
- **插件扩展**: 支持通过插件添加更多通道和功能

### 技术架构

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  聊天应用 + 插件  │ ──→ │   Gateway    │ ──→ │  AI 代理    │
│ WhatsApp/Telegram│     │  (WebSocket) │     │  (Pi 运行时) │
│ Discord/飞书等    │     │              │     │             │
└─────────────────┘     └──────────────┘     └─────────────┘
                               │
                    ┌──────────┼──────────┐
                    ↓          ↓          ↓
               CLI 工具    Web 控制台    移动节点
```

### 关键能力

| 能力 | 描述 |
|------|------|
| 多通道网关 | WhatsApp、Telegram、Discord、飞书等，单一网关进程 |
| 插件通道 | 支持 Mattermost 等扩展插件 |
| 多代理路由 | 每个代理独立会话，支持工作空间隔离 |
| 媒体支持 | 发送和接收图片、音频、文档 |
| Web 控制台 | 浏览器仪表盘，用于聊天、配置、会话管理 |
| 移动节点 | 支持 iOS 和 Android 节点配对，Canvas 支持 |
| 浏览器自动化 | 专用浏览器控制，支持点击、输入、截图 |
| 定时任务 | 内置 Cron 调度器，支持周期性任务 |

## 1.3 适用场景

### 个人开发者
- 个人 AI 助手，随时通过聊天应用访问
- 代码审查、调试、文档查询
- 自动化日常任务（日历检查、邮件摘要等）

### 小团队
- 团队知识库问答
- 自动化报告生成
- 多渠道客户支持

### 高级用户
- 自定义工作流自动化
- 多代理协作系统
- 远程服务器管理

## 1.4 与其他 AI 工具的区别

| 特性 | OpenClaw | 传统 Chatbot | 云端 AI 服务 |
|------|----------|-------------|-------------|
| 部署方式 | 自托管 | SaaS | SaaS |
| 数据控制 | 完全本地 | 云端存储 | 云端存储 |
| 多通道 | 原生支持 | 通常单一 | 通常单一 |
| 定制化 | 高度可定制 | 有限 | 有限 |
| 成本 | 仅硬件成本 | 订阅费 | 订阅费 + API 费 |
| 隐私 | 数据不出本地 | 依赖服务商 | 依赖服务商 |

---

# 第 2 章 快速开始

## 2.1 系统要求

### 硬件要求
- **CPU**: 任意现代 x64 或 ARM 处理器
- **内存**: 最低 2GB，推荐 4GB+
- **存储**: 至少 1GB 可用空间
- **网络**: 稳定的互联网连接（用于 API 调用）

### 软件要求
- **Node.js**: 22 或更高版本
- **操作系统**: macOS、Linux 或 Windows（推荐 WSL2）
- **包管理器**: npm 或 pnpm

<Note>
在 Windows 上，强烈建议在 [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) 下运行 OpenClaw。
</Note>

## 2.2 安装步骤

### 方法一：安装脚本（推荐）

安装脚本会自动处理 Node.js 检测、安装和入门向导。

**macOS / Linux / WSL2**:
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows (PowerShell)**:
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

如果只想安装二进制文件，跳过入门向导：
```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

### 方法二：npm/pnpm 安装

如果你已有 Node 22+ 并希望自行管理安装：

**使用 npm**:
```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

**使用 pnpm**:
```bash
pnpm add -g openclaw@latest
pnpm approve-builds -g        # 批准 openclaw, node-llama-cpp, sharp 等
openclaw onboard --install-daemon
```

<Note>
pnpm 需要明确批准带有构建脚本的包。首次安装显示 "Ignored build scripts" 警告后，运行 `pnpm approve-builds -g` 并选择列出的包。
</Note>

### 方法三：从源码安装

适合贡献者或需要本地 checkout 的用户：

```bash
# 克隆仓库
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 安装依赖并构建
pnpm install
pnpm ui:build
pnpm build

# 全局链接 CLI
pnpm link --global

# 运行入门向导
openclaw onboard --install-daemon
```

### 验证安装

```bash
# 检查版本
openclaw --version

# 健康检查
openclaw doctor

# 查看状态
openclaw status

# 打开 Web 控制台
openclaw dashboard
```

## 2.3 首次配置

### 运行入门向导

```bash
openclaw onboard
```

向导会引导你完成：
1. API 密钥配置（推荐 Anthropic/Claude）
2. 通道设置（WhatsApp、Telegram 等）
3. 网关配置
4. 工作空间初始化

### 配置文件位置

配置文件位于 `~/.openclaw/openclaw.json`

### 工作空间文件

OpenClaw 在工作空间中使用以下文件：

| 文件 | 用途 |
|------|------|
| `AGENTS.md` | 操作指令 + "记忆" |
| `SOUL.md` | 人格、边界、语气 |
| `TOOLS.md` | 用户维护的工具笔记 |
| `BOOTSTRAP.md` | 一次性首次运行仪式（完成后删除） |
| `IDENTITY.md` | 代理名称/风格/emoji |
| `USER.md` | 用户档案 + 首选称呼 |

## 2.4 第一个任务

### 启动网关

```bash
# 前台运行
openclaw gateway

# 后台运行（安装为服务后）
openclaw gateway start
```

### 连接通道

以 WhatsApp 为例：

```bash
# 登录 WhatsApp
openclaw channels login --channel whatsapp

# 扫描二维码完成配对
# 在手机上打开 WhatsApp → 设置 → 已连接设备 → 连接设备
```

### 发送第一条消息

通过配对的 WhatsApp 号码发送消息给代理，例如：
```
你好！请介绍一下你自己。
```

### 使用 Web 控制台

```bash
openclaw dashboard
```

在浏览器中访问 `http://127.0.0.1:18789/` 查看：
- 聊天界面
- 会话列表
- 配置选项
- 日志输出

---

# 第 3 章 核心概念

## 3.1 会话（Session）

### 什么是会话

会话是 OpenClaw 中对话的基本单位。每个会话有独立的上下文和记忆。

### 会话类型

| 类型 | 会话键格式 | 说明 |
|------|-----------|------|
| 直接消息（默认） | `agent:<agentId>:<mainKey>` | 所有 DM 共享主会话 |
| 按发送者隔离 | `agent:<agentId>:dm:<peerId>` | 每个发送者独立会话 |
| 按通道 + 发送者 | `agent:<agentId>:<channel>:dm:<peerId>` | 推荐多用户收件箱 |
| 群聊 | `agent:<agentId>:<channel>:group:<id>` | 群组独立会话 |
| Cron 任务 | `cron:<jobId>` | 定时任务独立会话 |

### 会话配置

```json5
{
  session: {
    // DM 会话范围
    dmScope: "per-channel-peer",  // main | per-peer | per-channel-peer | per-account-channel-peer
    
    // 身份链接（同一人在不同通道的会话合并）
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"]
    },
    
    // 会话重置策略
    reset: {
      mode: "daily",      // daily | idle
      atHour: 4,          // 每日重置时间（本地时间）
      idleMinutes: 120    // 空闲重置（分钟）
    },
    
    // 存储路径
    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
    mainKey: "main"
  }
}
```

### 会话维护

```bash
# 列出所有会话
openclaw sessions

# 只显示最近 2 小时的活跃会话
openclaw sessions --active 120

# 运行会话维护（清理过期会话）
openclaw sessions cleanup --enforce

# 预览维护效果（不实际执行）
openclaw sessions cleanup --dry-run
```

### 会话管理命令

在聊天中发送以下命令：
- `/status` - 查看会话状态和上下文使用
- `/new` 或 `/reset` - 开始新会话
- `/compact` - 压缩旧上下文，释放空间
- `/stop` - 停止当前运行
- `/send on/off` - 控制消息发送

## 3.2 子代理（Subagent）

### 什么是子代理

子代理是从现有代理运行中派生的后台代理运行。它们在独立的会话中运行，完成后将结果**通告**回请求者聊天通道。

### 使用场景

- 并行化研究/长时间任务/慢速工具工作
- 不阻塞主运行的后台任务
- 多代理协作（编排者模式）

### 基本用法

**通过 slash 命令**:
```bash
# 列出子代理
/subagents list

# 生成子代理
/subagents spawn main "研究最新的前端框架趋势"

# 查看日志
/subagents log <id>

# 停止子代理
/subagents kill <id>
```

**通过工具调用**:
```json
{
  "tool": "sessions_spawn",
  "params": {
    "task": "整理 GitHub issues",
    "label": "issue-triage",
    "mode": "run",
    "cleanup": "keep"
  }
}
```

### 配置

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxConcurrent: 8,           // 最大并发数
        maxSpawnDepth: 2,           // 最大嵌套深度（1-5）
        maxChildrenPerAgent: 5,     // 每个代理的最大子代理数
        runTimeoutSeconds: 900,     // 默认超时（秒）
        archiveAfterMinutes: 60     // 自动归档时间
      }
    }
  }
}
```

### 嵌套子代理

当 `maxSpawnDepth >= 2` 时，支持编排者模式：

```
主代理 (深度 0)
  └─→ 编排者子代理 (深度 1)
       ├─→ 工作子代理 A (深度 2)
       ├─→ 工作子代理 B (深度 2)
       └─→ 工作子代理 C (深度 2)
```

## 3.3 技能（Skill）

### 什么是技能

技能是教导代理如何使用工具的指令文件夹。每个技能包含一个 `SKILL.md` 文件，其中有 YAML frontmatter 和详细说明。

### 技能位置

技能从三个位置加载（优先级从高到低）：

1. **工作空间技能**: `<workspace>/skills`（最高优先级）
2. **本地/管理技能**: `~/.openclaw/skills`
3. **捆绑技能**: 随安装附带（最低优先级）

### 技能格式

```markdown
---
name: nano-banana-pro
description: 通过 Gemini 3 Pro Image 生成或编辑图片
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"] },
      "primaryEnv": "GEMINI_API_KEY"
    }
  }
---

# 技能说明

这里是技能的详细使用说明...
```

### 技能门控

技能可以通过 `metadata` 在加载时过滤：

- `always: true` - 始终包含
- `requires.bins` - 需要的二进制文件
- `requires.env` - 需要的环境变量
- `requires.config` - 需要的配置项
- `os` - 支持的操作系统列表

### 配置技能

```json5
{
  skills: {
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: "YOUR_API_KEY",
        env: {
          GEMINI_API_KEY: "YOUR_KEY"
        },
        config: {
          endpoint: "https://example.com"
        }
      }
    }
  }
}
```

## 3.4 工具（Tool）

### 核心工具

| 工具 | 用途 | 示例 |
|------|------|------|
| `read` | 读取文件 | 读取配置文件、文档 |
| `write` | 写入文件 | 创建新文件 |
| `edit` | 编辑文件 | 精确文本替换 |
| `exec` | 执行命令 | 运行 shell 命令 |
| `process` | 管理进程 | 后台任务管理 |
| `web_search` | 网络搜索 | 搜索文档、事实 |
| `web_fetch` | 获取网页 | 提取网页内容 |
| `browser` | 浏览器控制 | 自动化网页操作 |
| `message` | 发送消息 | 通道消息发送 |

### 工具策略

```json5
{
  tools: {
    // 完全拒绝的工具
    deny: ["exec"],
    
    // 仅允许的工具（如果设置）
    allow: ["read", "write", "web_search"],
    
    // exec 特定配置
    exec: {
      host: "sandbox",        // sandbox | gateway | node
      security: "allowlist",  // deny | allowlist | full
      ask: "on-miss",         // off | on-miss | always
      pathPrepend: ["~/bin"]  // PATH 前缀
    }
  }
}
```

## 3.5 通道（Channel）

### 支持的通道

| 通道 | 状态 | 配置复杂度 |
|------|------|-----------|
| WhatsApp | ✅ 稳定 | 中等 |
| Telegram | ✅ 稳定 | 简单 |
| Discord | ✅ 稳定 | 简单 |
| 飞书 | ✅ 稳定 | 中等 |
| QQ | ✅ 稳定 | 中等 |
| 钉钉 | ✅ 稳定 | 中等 |
| 企业微信 | ✅ 稳定 | 中等 |
| Slack | ✅ 稳定 | 简单 |
| Signal | ✅ 稳定 | 复杂 |
| iMessage | ✅ 测试 | 复杂 |

### 通道配置示例

```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      allowFrom: ["+8613800138000"],  // 允许的号码
      groups: {
        "*": { requireMention: true }  // 群组需要@提及
      }
    },
    telegram: {
      enabled: true,
      botToken: "YOUR_BOT_TOKEN"
    },
    feishu: {
      enabled: true,
      appId: "cli_xxx",
      appSecret: "xxx"
    }
  }
}
```

## 3.6 网关（Gateway）

### 什么是网关

网关是 OpenClaw 的 WebSocket 服务器，负责：
- 通道连接和管理
- 会话路由
- 节点配对
- 钩子执行
- Cron 调度

### 运行模式

| 模式 | 绑定 | 用途 |
|------|------|------|
| `local` | 本地回环 | 默认，安全 |
| `lan` | 局域网 | 内网访问 |
| `tailnet` | Tailscale | 安全远程访问 |
| `auto` | 自动选择 | 根据配置 |

### 启动网关

```bash
# 基本启动
openclaw gateway

# 指定端口
openclaw gateway --port 18789

# 指定绑定模式
openclaw gateway --bind lan

# 使用 token 认证
openclaw gateway --token "your-token"

# 开发模式（自动创建配置）
openclaw gateway --dev
```

### 网关服务管理

```bash
# 安装为系统服务
openclaw gateway install

# 启动服务
openclaw gateway start

# 停止服务
openclaw gateway stop

# 重启服务
openclaw gateway restart

# 卸载服务
openclaw gateway uninstall

# 查看状态
openclaw gateway status
```

---

# 第 4 章 CLI 命令详解

## 4.1 openclaw 基础命令

### 全局选项

```bash
openclaw [选项] [命令]

选项:
  --dev                开发模式：隔离状态到 ~/.openclaw-dev
  -h, --help           显示帮助
  --log-level <level>  日志级别 (silent|fatal|error|warn|info|debug|trace)
  --no-color           禁用 ANSI 颜色
  --profile <name>     使用命名配置文件
  -V, --version        显示版本号
```

### 常用命令速查

```bash
openclaw --version              # 查看版本
openclaw doctor                 # 健康检查
openclaw status                 # 查看状态
openclaw dashboard              # 打开 Web 控制台
openclaw configure              # 交互式配置向导
openclaw help                   # 显示帮助
```

## 4.2 配置命令（config/configure）

### config 命令

非交互式配置助手：

```bash
# 获取配置值
openclaw config get browser.executablePath
openclaw config get agents.defaults.workspace

# 设置配置值
openclaw config set browser.executablePath "/usr/bin/google-chrome"
openclaw config set agents.defaults.heartbeat.every "2h"

# 取消设置
openclaw config unset tools.web.search.apiKey

# 使用 JSON5 解析
openclaw config set gateway.port 19001 --strict-json
openclaw config set channels.whatsapp.groups '["*"]' --strict-json
```

### 路径表示法

```bash
# 点表示法
openclaw config get agents.defaults.workspace

# 括号表示法（用于数组）
openclaw config get agents.list[0].id
openclaw config set agents.list[1].tools.exec.node "node-id"
```

### configure 命令

交互式配置向导：

```bash
openclaw configure
```

引导完成：
- 凭证配置
- 通道设置
- 网关配置
- 代理默认值

## 4.3 会话管理（agents/sessions）

### agents 命令

管理隔离的代理（工作空间 + 认证 + 路由）：

```bash
# 列出所有代理
openclaw agents list

# 添加新代理
openclaw agents add work --workspace ~/.openclaw/workspace-work

# 查看路由绑定
openclaw agents bindings

# 绑定通道到代理
openclaw agents bind --agent work --bind telegram:ops

# 解绑
openclaw agents unbind --agent work --bind telegram:ops

# 设置身份
openclaw agents set-identity --agent main --name "OpenClaw" --emoji "🦞"

# 从 IDENTITY.md 加载
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity

# 删除代理
openclaw agents delete work
```

### sessions 命令

查看和管理会话：

```bash
# 列出所有会话
openclaw sessions

# 只显示最近 2 小时的活跃会话
openclaw sessions --active 120

# 指定代理
openclaw sessions --agent work

# 聚合所有代理的会话
openclaw sessions --all-agents

# JSON 输出
openclaw sessions --json

# 运行会话维护
openclaw sessions cleanup --enforce
openclaw sessions cleanup --dry-run
```

## 4.4 技能管理（clawhub）

### clawhub 命令

ClawHub 是 OpenClaw 的技能注册中心：

```bash
# 搜索技能
openclaw clawhub search <query>

# 安装技能
openclaw clawhub install <skill-slug>

# 更新所有技能
openclaw clawhub update --all

# 同步（扫描 + 发布更新）
openclaw clawhub sync --all

# 列出自定义技能
openclaw clawhub list

# 备份技能
openclaw clawhub backup
```

### 示例

```bash
# 安装天气技能
openclaw clawhub install weather

# 安装浏览器自动化技能
openclaw clawhub install agent-browser

# 更新特定技能
openclaw clawhub update weather
```

## 4.5 浏览器控制（browser）

### browser 命令

管理浏览器控制服务器和执行浏览器操作：

```bash
# 查看状态
openclaw browser status

# 启动浏览器
openclaw browser start

# 停止浏览器
openclaw browser stop

# 列出台灯
openclaw browser tabs

# 打开网页
openclaw browser open https://example.com

# 聚焦标签
openclaw browser focus <targetId>

# 关闭标签
openclaw browser close <targetId>

# 截图
openclaw browser screenshot
openclaw browser screenshot --full-page

# 快照
openclaw browser snapshot
openclaw browser snapshot --interactive

# 导航
openclaw browser navigate https://example.com

# 点击（使用快照中的 ref）
openclaw browser click 12
openclaw browser click e12

# 输入
openclaw browser type 23 "hello"

# 等待
openclaw browser wait --text "Done"
openclaw browser wait --url "**/dash"

# Cookie 管理
openclaw browser cookies
openclaw browser cookies set session abc123 --url "https://example.com"
openclaw browser cookies clear
```

### 浏览器配置文件

```bash
# 列出配置文件
openclaw browser profiles

# 创建配置文件
openclaw browser create-profile --name work --color "#FF5A36"

# 使用特定配置文件
openclaw browser --browser-profile work tabs
openclaw browser --browser-profile chrome snapshot

# 删除配置文件
openclaw browser delete-profile --name work
```

### Chrome 扩展中继

```bash
# 安装扩展
openclaw browser extension install

# 查看扩展路径
openclaw browser extension path
```

## 4.6 定时任务（cron）

### cron 命令

管理网关调度器的 cron 任务：

```bash
# 列出任务
openclaw cron list

# 添加一次性任务
openclaw cron add \
  --name "提醒" \
  --at "2026-03-08T18:00:00Z" \
  --session main \
  --system-event "提醒：提交费用报告" \
  --wake now \
  --delete-after-run

# 添加周期性任务
openclaw cron add \
  --name "晨间简报" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "总结隔夜更新" \
  --announce \
  --channel whatsapp \
  --to "+8613800138000"

# 编辑任务
openclaw cron edit <job-id> \
  --message "更新后的提示" \
  --model "opus"

# 手动运行任务
openclaw cron run <job-id>
openclaw cron run <job-id> --due

# 查看运行历史
openclaw cron runs --id <job-id> --limit 50

# 删除任务
openclaw cron remove <job-id>
```

### Cron 表达式示例

| 表达式 | 含义 |
|--------|------|
| `0 7 * * *` | 每天早上 7 点 |
| `0 */2 * * *` | 每 2 小时 |
| `0 9 * * 1-5` | 工作日早上 9 点 |
| `0 0 1 * *` | 每月 1 号午夜 |
| `*/5 * * * *` | 每 5 分钟 |

## 4.7 通道管理（channels）

### channels 命令

管理聊天通道账户和运行时状态：

```bash
# 列出所有通道
openclaw channels list

# 查看状态
openclaw channels status

# 查看功能
openclaw channels capabilities

# 添加账户
openclaw channels add --channel telegram --token <bot-token>

# 移除账户
openclaw channels remove --channel telegram --delete

# 登录（交互式）
openclaw channels login --channel whatsapp

# 登出
openclaw channels logout --channel whatsapp

# 查看日志
openclaw channels logs --channel all

# 解析名称到 ID
openclaw channels resolve --channel slack "#general" "@jane"
```

### 通道能力探测

```bash
# 所有通道
openclaw channels capabilities

# 特定通道
openclaw channels capabilities --channel discord --target channel:123
```

---

# 第 5 章 技能系统

## 5.1 技能是什么

技能是教导代理如何使用工具的指令文件夹。每个技能包含：

- `SKILL.md` - 主要说明文件（含 YAML frontmatter）
- 可选的脚本、参考文档、资源文件

### 技能结构

```
skill-name/
├── SKILL.md          # 必需：技能说明
├── scripts/          # 可选：脚本文件
├── references/       # 可选：参考文档
└── assets/           # 可选：资源文件
```

### SKILL.md 格式

```markdown
---
name: skill-name
description: 简短描述
metadata:
  {
    "openclaw": {
      "emoji": "🔧",
      "requires": { "bins": ["node"], "env": ["API_KEY"] },
      "primaryEnv": "API_KEY",
      "install": [
        {
          "id": "npm",
          "kind": "node",
          "package": "package-name",
          "bins": ["cmd"]
        }
      ]
    }
  }
---

# 技能名称

## 用途

这里是技能的详细说明...

## 使用方法

### 示例 1

```bash
命令示例
```

### 示例 2

更多示例...
```

## 5.2 安装技能（clawhub install）

### 从 ClawHub 安装

```bash
# 搜索技能
openclaw clawhub search weather

# 安装技能
openclaw clawhub install weather

# 安装到特定位置
cd ~/.openclaw/workspace
openclaw clawhub install weather
```

### 安装后配置

```json5
{
  skills: {
    entries: {
      "weather": {
        enabled: true,
        apiKey: "YOUR_API_KEY"
      }
    }
  }
}
```

## 5.3 更新技能

### 更新单个技能

```bash
openclaw clawhub update weather
```

### 更新所有技能

```bash
openclaw clawhub update --all
```

### 同步技能

```bash
# 扫描并发布更新
openclaw clawhub sync --all
```

## 5.4 开发技能

### 创建技能结构

```bash
mkdir -p ~/.openclaw/workspace/skills/my-skill
cd ~/.openclaw/workspace/skills/my-skill

# 创建 SKILL.md
cat > SKILL.md << 'EOF'
---
name: my-skill
description: 我的自定义技能
---

# 我的技能

这里是说明...
EOF
```

### 技能开发最佳实践

1. **清晰的 frontmatter**: 提供准确的名称和描述
2. **详细的说明**: 包含使用示例和边界情况
3. **适当的门控**: 使用 metadata 指定依赖
4. **错误处理**: 说明可能的错误和解决方案
5. **测试**: 在实际使用中验证技能

### 技能调试

```bash
# 查看加载的技能
openclaw config get skills.entries

# 重新加载技能（重启网关或等待 watcher）
openclaw gateway restart
```

## 5.5 发布技能

### 发布到 ClawHub

```bash
# 登录 ClawHub
openclaw clawhub login

# 发布技能
openclaw clawhub publish my-skill

# 更新已发布的技能
openclaw clawhub publish my-skill --update
```

### 发布要求

1. 有效的 `SKILL.md` 格式
2. 清晰的描述和使用说明
3. 适当的元数据（依赖、环境等）
4. 无恶意代码

## 5.6 常用技能介绍

### 核心技能

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| `weather` | 天气预报 | `clawhub install weather` |
| `brave-search` | 网络搜索 | `clawhub install brave-search` |
| `agent-browser` | 浏览器自动化 | `clawhub install agent-browser` |
| `github` | GitHub 操作 | `clawhub install github` |
| `memory-manager` | 记忆管理 | `clawhub install memory-manager` |

### 主动代理技能

| 技能 | 用途 |
|------|------|
| `proactive-agent` | 主动工作架构 |
| `proactive-tasks` | 任务管理 |
| `self-improving-agent` | 自我改进 |

### 平台特定技能

| 技能 | 用途 |
|------|------|
| `feishu-doc` | 飞书文档操作 |
| `feishu-drive` | 飞书云存储 |
| `qqbot-media` | QQ 媒体发送 |

---

# 第 6 章 工具系统

## 6.1 文件操作

### read - 读取文件

读取文本文件或图片内容。

**参数**:
- `path` - 文件路径（必需）
- `offset` - 起始行号（可选）
- `limit` - 最大行数（可选）

**示例**:
```json
{
  "tool": "read",
  "params": {
    "path": "~/.openclaw/openclaw.json"
  }
}
```

```json
{
  "tool": "read",
  "params": {
    "path": "large-file.txt",
    "offset": 100,
    "limit": 50
  }
}
```

### write - 写入文件

创建或覆盖文件。

**参数**:
- `path` - 文件路径（必需）
- `content` - 文件内容（必需）

**示例**:
```json
{
  "tool": "write",
  "params": {
    "path": "notes.md",
    "content": "# 笔记\n\n这里是内容..."
  }
}
```

### edit - 编辑文件

精确文本替换编辑。

**参数**:
- `path` - 文件路径（必需）
- `oldText` - 要替换的原文（必需）
- `newText` - 新文本（必需）

**示例**:
```json
{
  "tool": "edit",
  "params": {
    "path": "config.json",
    "oldText": "\"port\": 8080",
    "newText": "\"port\": 9090"
  }
}
```

### exec - 执行命令

运行 shell 命令。

**参数**:
- `command` - 命令（必需）
- `workdir` - 工作目录（可选）
- `env` - 环境变量（可选）
- `yieldMs` - 后台延迟（可选）
- `timeout` - 超时秒数（可选）
- `pty` - 伪终端（可选）
- `host` - 执行主机（sandbox|gateway|node）（可选）
- `security` - 安全模式（可选）

**示例**:
```json
{
  "tool": "exec",
  "params": {
    "command": "ls -la"
  }
}
```

```json
{
  "tool": "exec",
  "params": {
    "command": "npm run build",
    "yieldMs": 1000,
    "timeout": 300
  }
}
```

### process - 管理进程

管理后台 exec 会话。

**动作**:
- `list` - 列出会话
- `poll` - 轮询状态
- `log` - 获取日志
- `write` - 写入数据
- `send-keys` - 发送按键
- `submit` - 提交输入
- `paste` - 粘贴文本
- `kill` - 终止进程

**示例**:
```json
{
  "tool": "process",
  "params": {
    "action": "poll",
    "sessionId": "<session-id>",
    "timeout": 5000
  }
}
```

```json
{
  "tool": "process",
  "params": {
    "action": "send-keys",
    "sessionId": "<session-id>",
    "keys": ["Enter"]
  }
}
```

## 6.2 网络工具

### web_search - 网络搜索

使用 Brave Search API 搜索网络。

**参数**:
- `query` - 搜索词（必需）
- `count` - 结果数量（1-10）（可选）
- `country` - 国家代码（可选）
- `search_lang` - 搜索语言（可选）
- `ui_lang` - UI 语言（可选）
- `freshness` - 时间过滤（可选）

**示例**:
```json
{
  "tool": "web_search",
  "params": {
    "query": "OpenClaw documentation",
    "count": 5
  }
}
```

```json
{
  "tool": "web_search",
  "params": {
    "query": "最新 AI 新闻",
    "country": "CN",
    "search_lang": "zh",
    "freshness": "pw"
  }
}
```

### web_fetch - 获取网页

从 URL 提取可读内容。

**参数**:
- `url` - URL（必需）
- `extractMode` - 提取模式（markdown|text）（可选）
- `maxChars` - 最大字符数（可选）

**示例**:
```json
{
  "tool": "web_fetch",
  "params": {
    "url": "https://docs.openclaw.ai",
    "extractMode": "markdown"
  }
}
```

### browser - 浏览器控制

控制浏览器执行自动化操作。

**动作**:
- `status` - 查看状态
- `start` - 启动浏览器
- `stop` - 停止浏览器
- `tabs` - 列出台灯
- `open` - 打开 URL
- `focus` - 聚焦标签
- `close` - 关闭标签
- `snapshot` - 获取快照
- `screenshot` - 截图
- `navigate` - 导航
- `act` - 执行操作（点击、输入等）

**示例**:
```json
{
  "tool": "browser",
  "params": {
    "action": "open",
    "targetUrl": "https://example.com"
  }
}
```

```json
{
  "tool": "browser",
  "params": {
    "action": "snapshot",
    "refs": "aria"
  }
}
```

```json
{
  "tool": "browser",
  "params": {
    "action": "act",
    "request": {
      "kind": "click",
      "ref": "e12"
    }
  }
}
```

## 6.3 消息工具

### message - 发送消息

通过通道插件发送和管理消息。

**动作**:
- `send` - 发送消息
- `broadcast` - 广播消息

**参数**:
- `action` - 动作（必需）
- `target` - 目标通道/用户（可选）
- `message` - 消息内容（可选）
- `channel` - 通道（可选）
- `threadId` - 线程 ID（可选）
- `replyTo` - 回复消息 ID（可选）
- `media` - 媒体 URL（可选）
- `buffer` - 附件 base64（可选）

**示例**:
```json
{
  "tool": "message",
  "params": {
    "action": "send",
    "target": "telegram:123456789",
    "message": "你好！这是一条测试消息。"
  }
}
```

```json
{
  "tool": "message",
  "params": {
    "action": "send",
    "channel": "discord",
    "message": "团队通知：会议推迟到下午 3 点",
    "threadId": "thread-123"
  }
}
```

## 6.4 会话工具

### sessions_list - 列出会话

列出存储的会话。

**示例**:
```json
{
  "tool": "sessions_list",
  "params": {
    "agentId": "main",
    "activeMinutes": 120
  }
}
```

### sessions_history - 获取历史

获取会话历史记录。

**示例**:
```json
{
  "tool": "sessions_history",
  "params": {
    "sessionKey": "agent:main:main"
  }
}
```

### sessions_spawn - 生成子代理

生成子代理运行。

**参数**:
- `task` - 任务描述（必需）
- `label` - 标签（可选）
- `agentId` - 代理 ID（可选）
- `model` - 模型（可选）
- `thinking` - 思考级别（可选）
- `mode` - 模式（run|session）（可选）
- `cleanup` - 清理策略（delete|keep）（可选）
- `thread` - 线程绑定（可选）

**示例**:
```json
{
  "tool": "sessions_spawn",
  "params": {
    "task": "研究最新的前端框架",
    "label": "research",
    "mode": "run",
    "cleanup": "keep"
  }
}
```

## 6.5 Feishu 工具

### feishu_doc - 飞书文档

操作飞书文档。

**动作**:
- `read` - 读取文档
- `write` - 写入文档
- `append` - 追加内容
- `create` - 创建文档
- `list_blocks` - 列出块
- `get_block` - 获取块
- `update_block` - 更新块
- `delete_block` - 删除块

**示例**:
```json
{
  "tool": "feishu_doc",
  "params": {
    "action": "read",
    "doc_token": "docxxx"
  }
}
```

### feishu_drive - 飞书云存储

操作飞书云存储。

**动作**:
- `list` - 列出文件
- `info` - 获取信息
- `create_folder` - 创建文件夹
- `move` - 移动文件
- `delete` - 删除文件

**示例**:
```json
{
  "tool": "feishu_drive",
  "params": {
    "action": "list",
    "folder_token": "folderxxx"
  }
}
```

### feishu_wiki - 飞书知识库

操作飞书知识库。

**动作**:
- `spaces` - 列出空间
- `nodes` - 列出节点
- `get` - 获取节点
- `search` - 搜索
- `create` - 创建节点
- `move` - 移动节点
- `rename` - 重命名

**示例**:
```json
{
  "tool": "feishu_wiki",
  "params": {
    "action": "search",
    "query": "项目文档"
  }
}
```

### feishu_bitable - 飞书多维表格

操作飞书多维表格。

**相关工具**:
- `feishu_bitable_get_meta` - 获取元数据
- `feishu_bitable_list_fields` - 列出字段
- `feishu_bitable_list_records` - 列出记录
- `feishu_bitable_get_record` - 获取记录
- `feishu_bitable_create_record` - 创建记录
- `feishu_bitable_update_record` - 更新记录
- `feishu_bitable_create_app` - 创建应用
- `feishu_bitable_create_field` - 创建字段

**示例**:
```json
{
  "tool": "feishu_bitable_get_meta",
  "params": {
    "url": "https://xxx.feishu.cn/base/xxx?table=xxx"
  }
}
```

## 6.6 其他工具

### tts - 文本转语音

将文本转换为语音。

**参数**:
- `text` - 文本内容（必需）
- `channel` - 通道 ID（可选）

**示例**:
```json
{
  "tool": "tts",
  "params": {
    "text": "你好，这是语音消息。"
  }
}
```

### nodes - 节点管理

管理配对的节点。

**动作**:
- `status` - 查看状态
- `describe` - 描述节点
- `notify` - 发送通知
- `camera_snap` - 相机快照
- `screen_record` - 屏幕录制
- `location_get` - 获取位置
- `run` - 运行命令
- `invoke` - 调用

**示例**:
```json
{
  "tool": "nodes",
  "params": {
    "action": "status"
  }
}
```

### subagents - 子代理管理

管理生成的子代理。

**动作**:
- `list` - 列出子代理
- `kill` - 终止子代理
- `steer` - 指导子代理

**示例**:
```json
{
  "tool": "subagents",
  "params": {
    "action": "list"
  }
}
```

---

# 第 7 章 通道配置

## 7.1 Feishu（飞书）配置

### 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret

### 配置步骤

```json5
{
  channels: {
    feishu: {
      enabled: true,
      appId: "cli_xxx",
      appSecret: "xxx",
      domain: "feishu",  // 或 feishu.cn
      groupPolicy: "open"  // open | mention
    }
  }
}
```

### 权限配置

在飞书开放平台配置以下权限：
- 消息发送权限
- 用户信息读取权限
- 群组信息读取权限

### 验证配置

```bash
openclaw channels list --channel feishu
openclaw channels status
```

## 7.2 Telegram 配置

### 创建 Telegram Bot

1. 与 [@BotFather](https://t.me/BotFather) 对话
2. 发送 `/newbot` 创建新 bot
3. 获取 bot token

### 配置步骤

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "YOUR_BOT_TOKEN",
      allowFrom: ["123456789"],  // 允许的用户 ID
      groups: {
        "*": { requireMention: true }
      }
    }
  }
}
```

### 获取用户/群组 ID

```bash
# 解析名称到 ID
openclaw channels resolve --channel telegram "@username"

# 查看通道能力
openclaw channels capabilities --channel telegram
```

## 7.3 Discord 配置

### 创建 Discord 应用

1. 访问 [Discord Developer Portal](https://discord.com/developers/applications)
2. 创建新应用
3. 创建 Bot 并获取 token
4. 邀请 Bot 到服务器

### 配置步骤

```json5
{
  channels: {
    discord: {
      enabled: true,
      botToken: "YOUR_BOT_TOKEN",
      guilds: ["guild-id"],  // 允许的服务器 ID
      threadBindings: {
        enabled: true,
        ttlHours: 24
      }
    }
  }
}
```

### 权限配置

Bot 需要以下权限：
- 发送消息
- 读取消息历史
- 管理线程（如果使用线程绑定）

## 7.4 WhatsApp 配置

### 配置步骤

WhatsApp 通过二维码配对：

```bash
# 登录 WhatsApp
openclaw channels login --channel whatsapp

# 在手机上打开 WhatsApp
# 设置 → 已连接设备 → 连接设备
# 扫描显示的二维码
```

### 配置选项

```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      allowFrom: ["+8613800138000"],  // 允许的号码
      groups: {
        "*": { requireMention: true }  // 群组需要@提及
      },
      sessionTimeout: 86400  // 会话超时（秒）
    }
  }
}
```

### 多账号支持

```json5
{
  channels: {
    whatsapp: {
      accounts: {
        default: {
          allowFrom: ["+8613800138000"]
        },
        work: {
          allowFrom: ["+8613900139000"]
        }
      }
    }
  }
}
```

## 7.5 QQ 配置

### 配置步骤

QQ 通过插件支持：

```bash
# 安装 QQ 插件
npm install -g @sliverp/qqbot

# 配置 QQ 通道
openclaw config set channels.qqbot.enabled true
```

### 配置选项

```json5
{
  channels: {
    qqbot: {
      enabled: true,
      // 具体配置参考插件文档
    }
  }
}
```

## 7.6 其他通道

### 钉钉 (DingTalk)

```json5
{
  channels: {
    ddingtalk: {
      enabled: true,
      // 配置参考钉钉开放平台
    }
  }
}
```

### 企业微信 (WeCom)

```json5
{
  channels: {
    wecom: {
      enabled: true,
      // 配置参考企业微信开放平台
    }
  }
}
```

### Slack

```json5
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-xxx",
      signingSecret: "xxx"
    }
  }
}
```

### Signal

Signal 需要运行 signal-cli：

```json5
{
  channels: {
    signal: {
      enabled: true,
      signalCliPath: "/usr/bin/signal-cli",
      account: "+1234567890"
    }
  }
}
```

---

# 第 8 章 高级功能

## 8.1 子代理系统

### 架构概述

子代理系统允许主代理派生后台代理运行，实现：
- 并行任务执行
- 任务隔离
- 结果自动通告

### 深度级别

| 深度 | 会话键格式 | 角色 | 可生成子代理 |
|------|-----------|------|-------------|
| 0 | `agent:<id>:main` | 主代理 | 总是 |
| 1 | `agent:<id>:subagent:<uuid>` | 子代理 | 仅当 `maxSpawnDepth >= 2` |
| 2 | `agent:<id>:subagent:<uuid>:subagent:<uuid>` | 子子代理 | 从不 |

### 编排者模式

启用嵌套子代理：

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxSpawnDepth: 2,
        maxChildrenPerAgent: 5
      }
    }
  }
}
```

### 通告链

```
深度 2 工作代理完成
  ↓ 通告给深度 1 编排者
深度 1 编排者合成结果
  ↓ 通告给主代理
主代理交付给用户
```

### 工具策略

**深度 1（编排者）**:
- 允许：`sessions_spawn`, `subagents`, `sessions_list`, `sessions_history`
- 拒绝：其他会话/系统工具

**深度 2（工作代理）**:
- 拒绝：所有会话工具

### 级联停止

```bash
# 停止主会话会级联停止所有子代理
/stop

# 停止特定子代理会级联停止其子代理
/subagents kill <id>

# 停止所有子代理
/subagents kill all
```

## 8.2 Cron 定时任务

### 任务类型

**一次性任务**:
```bash
openclaw cron add \
  --name "会议提醒" \
  --at "2026-03-08T15:00:00+08:00" \
  --session main \
  --system-event "提醒：下午 3 点有会议" \
  --wake now
```

**周期性任务**:
```bash
openclaw cron add \
  --name "每日简报" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "总结昨天的工作" \
  --announce \
  --channel feishu \
  --to "chat_id"
```

### 执行模式

**主会话模式**:
- 在下一个心跳时运行
- 共享主会话上下文
- 适合轻量任务

**隔离模式**:
- 独立会话运行
- 不污染主会话
- 适合嘈杂或频繁任务

### 交付模式

| 模式 | 说明 |
|------|------|
| `announce` | 发送到指定通道 |
| `webhook` | POST 到 HTTP 端点 |
| `none` | 仅内部执行 |

### 配置示例

```json5
{
  cron: {
    enabled: true,
    store: "~/.openclaw/cron/jobs.json",
    maxConcurrentRuns: 1,
    sessionRetention: "24h",
    runLog: {
      maxBytes: "2mb",
      keepLines: 2000
    }
  }
}
```

### 维护

```bash
# 查看运行历史
openclaw cron runs --id <job-id>

# 编辑任务
openclaw cron edit <job-id> --message "新提示"

# 删除任务
openclaw cron remove <job-id>
```

## 8.3 浏览器自动化

### 浏览器配置文件

**openclaw 配置文件**:
- 专用隔离浏览器
- 不影响个人浏览数据
- 自动管理

**chrome 配置文件**:
- 使用现有 Chrome
- 需要扩展中继
- 共享浏览数据

### 配置

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "openclaw",
    headless: false,
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" }
    },
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: true
    }
  }
}
```

### 自动化工作流

```bash
# 1. 启动浏览器
openclaw browser --browser-profile openclaw start

# 2. 打开网页
openclaw browser --browser-profile openclaw open https://example.com

# 3. 获取快照
openclaw browser --browser-profile openclaw snapshot --interactive

# 4. 点击元素
openclaw browser --browser-profile openclaw click e12

# 5. 输入文本
openclaw browser --browser-profile openclaw type e23 "搜索内容"

# 6. 截图
openclaw browser --browser-profile openclaw screenshot --full-page
```

### 等待条件

```bash
# 等待文本
openclaw browser wait --text "加载完成"

# 等待 URL
openclaw browser wait --url "**/dashboard"

# 等待加载状态
openclaw browser wait --load networkidle

# 等待 JS 条件
openclaw browser wait --fn "window.ready===true"

# 组合等待
openclaw browser wait "#main" \
  --url "**/dash" \
  --load networkidle \
  --timeout-ms 15000
```

### 调试

```bash
# 查看错误
openclaw browser errors

# 查看请求
openclaw browser requests --filter api

# 清除错误
openclaw browser errors --clear

# 记录追踪
openclaw browser trace start
# ... 重现问题 ...
openclaw browser trace stop
```

## 8.4 远程节点

### 什么是节点

节点是运行在远程机器上的 OpenClaw 组件，允许：
- 远程命令执行
- 浏览器代理
- 屏幕录制
- 相机控制

### 配对节点

```bash
# 生成配对令牌
openclaw pairing create

# 在远程设备上输入令牌完成配对
```

### 节点命令

```bash
# 列出节点
openclaw nodes status

# 描述节点
openclaw nodes describe --node <node-id>

# 发送通知
openclaw nodes notify --node <node-id> --title "标题" --body "内容"

# 运行命令
openclaw nodes run --node <node-id> --command "ls -la"

# 屏幕录制
openclaw nodes screen_record --node <node-id> --duration 30

# 获取位置
openclaw nodes location_get --node <node-id>
```

### 远程浏览器代理

当节点连接时，浏览器工具可自动路由到节点：

```json5
{
  gateway: {
    nodes: {
      browser: {
        mode: "auto",  // auto | off | pin
        node: "node-id"  // 当 mode=pin 时使用
      }
    }
  }
}
```

## 8.5 记忆系统

### 记忆文件结构

```
workspace/
├── MEMORY.md              # 长期记忆（精选）
└── memory/
    ├── 2026-03-07.md      # 每日记忆
    ├── 2026-03-08.md
    └── projects.md        # 主题记忆
```

### 记忆工具

**memory_search** - 语义搜索:
```json
{
  "tool": "memory_search",
  "params": {
    "query": "项目配置",
    "limit": 5
  }
}
```

**memory_get** - 获取特定记忆:
```json
{
  "tool": "memory_get",
  "params": {
    "path": "memory/projects.md"
  }
}
```

### 配置记忆搜索

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        enabled: true,
        provider: "openai",  // openai | gemini | voyage | mistral | local
        model: "text-embedding-3-small",
        query: {
          hybrid: {
            enabled: true,
            vectorWeight: 0.7,
            textWeight: 0.3,
            mmr: {
              enabled: true,
              lambda: 0.7
            },
            temporalDecay: {
              enabled: true,
              halfLifeDays: 30
            }
          }
        },
        cache: {
          enabled: true,
          maxEntries: 50000
        }
      }
    }
  }
}
```

### 自动记忆刷新

当会话接近自动压缩时，OpenClaw 会触发静默记忆刷新：

```json5
{
  agents: {
    defaults: {
      compaction: {
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000,
          systemPrompt: "会话接近压缩。现在存储持久记忆。",
          prompt: "将持久笔记写入 memory/YYYY-MM-DD.md；如果没有要存储的，回复 NO_REPLY。"
        }
      }
    }
  }
}
```

### QMD 后端（实验性）

```json5
{
  memory: {
    backend: "qmd",
    citations: "auto",
    qmd: {
      includeDefaultMemory: true,
      update: { interval: "5m", debounceMs: 15000 },
      limits: { maxResults: 6, timeoutMs: 4000 },
      paths: [
        { name: "docs", path: "~/notes", pattern: "**/*.md" }
      ]
    }
  }
}
```

---

# 第 9 章 配置详解

## 9.1 配置文件位置

### 默认位置

```
~/.openclaw/openclaw.json
```

### 环境变量覆盖

| 变量 | 用途 |
|------|------|
| `OPENCLAW_HOME` | 主目录基础路径 |
| `OPENCLAW_STATE_DIR` | 可变状态位置 |
| `OPENCLAW_CONFIG_PATH` | 配置文件位置 |
| `OPENCLAW_GATEWAY_TOKEN` | 网关令牌 |
| `OPENCLAW_GATEWAY_PORT` | 网关端口 |

### 配置文件

```bash
# 使用命名配置文件
openclaw --profile work

# 开发模式
openclaw --dev

# 指定配置路径
OPENCLAW_CONFIG_PATH=/path/to/config.json openclaw gateway
```

## 9.2 openclaw.json 结构

### 完整配置示例

```json5
{
  // 元数据
  "meta": {
    "lastTouchedVersion": "2026.2.26",
    "lastTouchedAt": "2026-03-07T02:51:49.238Z"
  },

  // 向导配置
  "wizard": {
    "lastRunAt": "2026-02-27T08:04:00.750Z",
    "lastRunVersion": "2026.2.26",
    "lastRunCommand": "onboard",
    "lastRunMode": "local"
  },

  // 代理配置
  "agents": {
    "defaults": {
      "workspace": "/root/.openclaw/workspace",
      "compaction": {
        "mode": "safeguard"
      },
      "maxConcurrent": 4,
      "subagents": {
        "maxConcurrent": 8,
        "maxSpawnDepth": 2,
        "maxChildrenPerAgent": 5,
        "runTimeoutSeconds": 900
      },
      "model": {
        "primary": "qwencode/qwen3.5-plus"
      },
      "memorySearch": {
        "enabled": true,
        "provider": "openai",
        "model": "text-embedding-3-small"
      }
    },
    "list": [
      {
        "id": "main",
        "identity": {
          "name": "OpenClaw",
          "theme": "space lobster",
          "emoji": "🦞",
          "avatar": "avatars/openclaw.png"
        }
      }
    ]
  },

  // 消息配置
  "messages": {
    "ackReactionScope": "group-mentions"
  },

  // 命令配置
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true,
    "ownerDisplay": "raw"
  },

  // 会话配置
  "session": {
    "dmScope": "per-channel-peer",
    "reset": {
      "mode": "daily",
      "atHour": 4,
      "idleMinutes": 120
    },
    "maintenance": {
      "mode": "enforce",
      "pruneAfter": "30d",
      "maxEntries": 500
    }
  },

  // 网关配置
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "your-token"
    },
    "tailscale": {
      "mode": "off"
    },
    "nodes": {
      "browser": {
        "mode": "auto"
      }
    }
  },

  // 技能配置
  "skills": {
    "install": {
      "nodeManager": "npm"
    },
    "entries": {
      "weather": {
        "enabled": true,
        "apiKey": "YOUR_API_KEY"
      }
    }
  },

  // 插件配置
  "plugins": {
    "entries": {
      "feishu": { "enabled": true },
      "qqbot": { "enabled": true },
      "ddingtalk": { "enabled": true },
      "wecom": { "enabled": true }
    }
  },

  // 模型配置
  "models": {
    "providers": {
      "qwencode": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "sk-xxx",
        "api": "openai-completions",
        "models": [
          { "id": "qwen3.5-plus", "name": "Qwen3.5 Plus" },
          { "id": "qwen3-max-2026-01-23", "name": "Qwen3 Max" }
        ]
      }
    },
    "mode": "merge"
  },

  // 通道配置
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "domain": "feishu",
      "groupPolicy": "open"
    },
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+8613800138000"],
      "groups": {
        "*": { "requireMention": true }
      }
    }
  },

  // 工具配置
  "tools": {
    "exec": {
      "host": "sandbox",
      "security": "allowlist",
      "ask": "on-miss",
      "pathPrepend": ["~/bin"]
    }
  },

  // 浏览器配置
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "headless": false,
    "ssrfPolicy": {
      "dangerouslyAllowPrivateNetwork": true
    }
  },

  // Cron 配置
  "cron": {
    "enabled": true,
    "sessionRetention": "24h",
    "runLog": {
      "maxBytes": "2mb",
      "keepLines": 2000
    }
  }
}
```

## 9.3 环境变量

### 核心环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPENCLAW_HOME` | `~/.openclaw` | 主目录 |
| `OPENCLAW_STATE_DIR` | `~/.openclaw` | 状态目录 |
| `OPENCLAW_CONFIG_PATH` | `~/.openclaw/openclaw.json` | 配置文件 |
| `OPENCLAW_GATEWAY_PORT` | `18789` | 网关端口 |
| `OPENCLAW_GATEWAY_TOKEN` | - | 网关令牌 |
| `OPENCLAW_SKIP_CRON` | - | 跳过 Cron（设为 1） |

### API 密钥环境变量

| 变量 | 用途 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API |
| `OPENAI_API_KEY` | OpenAI API |
| `GEMINI_API_KEY` | Google Gemini API |
| `VOYAGE_API_KEY` | Voyage AI API |
| `MISTRAL_API_KEY` | Mistral AI API |

## 9.4 安全设置

### 网关安全

```json5
{
  gateway: {
    // 绑定模式
    bind: "loopback",  // loopback | lan | tailnet | auto
    
    // 认证模式
    auth: {
      mode: "token",  // none | token | password | trusted-proxy
      token: "your-secure-token"
    },
    
    // Tailscale 暴露
    tailscale: {
      mode: "off",  // off | serve | funnel
      resetOnExit: false
    },
    
    // 控制 UI
    controlUi: {
      allowedOrigins: ["http://localhost:18789"],
      allowInsecureAuth: false,
      dangerouslyDisableDeviceAuth: false
    }
  }
}
```

### 工具安全

```json5
{
  tools: {
    // 完全拒绝的工具
    deny: ["exec"],
    
    // exec 特定安全
    exec: {
      host: "sandbox",  // sandbox | gateway | node
      security: "allowlist",  // deny | allowlist | full
      ask: "on-miss",  // off | on-miss | always
      
      // 安全二进制文件（仅 stdin）
      safeBins: ["cat", "grep", "jq"],
      
      // 信任目录
      safeBinTrustedDirs: ["/usr/local/bin"],
      
      // PATH 前缀
      pathPrepend: ["~/bin"]
    }
  }
}
```

### 会话安全

```json5
{
  session: {
    // DM 会话范围（多用户时推荐 per-channel-peer）
    dmScope: "per-channel-peer",
    
    // 身份链接
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321"]
    },
    
    // 发送策略
    sendPolicy: {
      rules: [
        { action: "deny", match: { channel: "discord", chatType: "group" } }
      ],
      default: "allow"
    }
  }
}
```

### 浏览器安全

```json5
{
  browser: {
    // SSRF 策略
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: false,  // 严格模式
      hostnameAllowlist: ["*.example.com", "example.com"],
      allowedHostnames: ["localhost"]
    },
    
    // 禁用 JS 执行（可选）
    evaluateEnabled: false
  }
}
```

### 技能安全

```json5
{
  skills: {
    // 只允许特定捆绑技能
    allowBundled: ["weather", "brave-search"],
    
    // 技能条目配置
    entries: {
      "my-skill": {
        enabled: true,
        apiKey: {
          source: "env",
          provider: "default",
          id: "MY_API_KEY"
        }
      }
    }
  }
}
```

---

# 第 10 章 最佳实践

## 10.1 使用技巧

### 会话管理

1. **定期清理会话**:
```bash
# 每周运行会话维护
openclaw sessions cleanup --enforce
```

2. **使用适当的 dmScope**:
- 单用户：`main`（默认）
- 多用户：`per-channel-peer`
- 多账号：`per-account-channel-peer`

3. **会话重置策略**:
```json5
{
  session: {
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 120
    }
  }
}
```

### 记忆管理

1. **定期整理 MEMORY.md**:
- 每周回顾 daily notes
- 提取重要信息到 MEMORY.md
- 删除过期信息

2. **使用记忆搜索**:
```json
{
  "tool": "memory_search",
  "params": {
    "query": "项目配置",
    "limit": 5
  }
}
```

3. **配置混合搜索**:
```json5
{
  memorySearch: {
    query: {
      hybrid: {
        enabled: true,
        vectorWeight: 0.7,
        textWeight: 0.3,
        mmr: { enabled: true, lambda: 0.7 },
        temporalDecay: { enabled: true, halfLifeDays: 30 }
      }
    }
  }
}
```

### 子代理使用

1. **适当使用子代理**:
- 长时间任务（>5 分钟）
- 独立研究任务
- 并行可执行任务

2. **配置超时**:
```json5
{
  agents: {
    defaults: {
      subagents: {
        runTimeoutSeconds: 900  // 15 分钟
      }
    }
  }
}
```

3. **监控子代理**:
```bash
/subagents list
/subagents log <id>
```

### Cron 任务

1. **避免整点任务**:
使用 stagger 分散负载：
```bash
openclaw cron add \
  --name "检查" \
  --cron "0 * * * *" \
  --stagger 30s
```

2. **使用隔离模式处理嘈杂任务**:
```bash
openclaw cron add \
  --name "每分钟检查" \
  --cron "* * * * *" \
  --session isolated \
  --delivery.mode none
```

3. **定期清理运行历史**:
```json5
{
  cron: {
    runLog: {
      maxBytes: "2mb",
      keepLines: 2000
    }
  }
}
```

## 10.2 性能优化

### 减少上下文大小

1. **配置上下文令牌限制**:
```json5
{
  agents: {
    defaults: {
      contextTokens: 80000  // 限制上下文窗口
    }
  }
}
```

2. **启用自动压缩**:
```json5
{
  agents: {
    defaults: {
      compaction: {
        mode: "safeguard",
        reserveTokensFloor: 20000
      }
    }
  }
}
```

3. **使用记忆刷新**:
```json5
{
  agents: {
    defaults: {
      compaction: {
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000
        }
      }
    }
  }
}
```

### 优化技能加载

1. **禁用不需要的技能**:
```json5
{
  skills: {
    entries: {
      "unused-skill": { enabled: false }
    }
  }
}
```

2. **使用技能门控**:
```markdown
---
name: my-skill
metadata:
  {
    "openclaw": {
      "requires": { "env": ["API_KEY"] }
    }
  }
---
```

### 浏览器优化

1. **使用 headless 模式**（服务器）:
```json5
{
  browser: {
    headless: true
  }
}
```

2. **配置 SSRF 策略**:
```json5
{
  browser: {
    ssrfPolicy: {
      dangerouslyAllowPrivateNetwork: false
    }
  }
}
```

3. **使用高效快照**:
```json5
{
  browser: {
    snapshotDefaults: {
      mode: "efficient"
    }
  }
}
```

## 10.3 常见问题

### Q: `openclaw` 命令找不到

**A**: 检查 PATH 配置
```bash
# 诊断
npm prefix -g
echo $PATH

# 修复（添加到 ~/.zshrc 或 ~/.bashrc）
export PATH="$(npm prefix -g)/bin:$PATH"
```

### Q: WhatsApp 无法连接

**A**: 
1. 检查网络连通性
2. 重新登录：`openclaw channels logout --channel whatsapp`
3. 清除会话数据后重新配对

### Q: 网关无法启动

**A**:
1. 检查端口占用：`lsof -i :18789`
2. 检查配置：`openclaw doctor`
3. 查看详细日志：`openclaw gateway --verbose`

### Q: 技能不加载

**A**:
1. 检查技能格式：`SKILL.md` frontmatter
2. 检查依赖：二进制文件、环境变量
3. 查看网关日志
4. 重启网关：`openclaw gateway restart`

### Q: 记忆搜索不工作

**A**:
1. 检查 embedding provider 配置
2. 验证 API 密钥
3. 检查记忆文件是否存在
4. 查看 `memory_search` 工具返回

### Q: 子代理无法生成

**A**:
1. 检查 `maxSpawnDepth` 配置
2. 检查并发限制
3. 查看网关日志
4. 验证工具策略

## 10.4 故障排除

### 诊断命令

```bash
# 全面健康检查
openclaw doctor

# 深度状态检查
openclaw status --deep

# 网关探测
openclaw gateway probe

# 通道状态
openclaw channels status

# 查看日志
openclaw logs

# 安全审计
openclaw security audit
```

### 日志级别

```bash
# 详细日志
openclaw gateway --verbose

# 调试级别
openclaw --log-level debug gateway

# 仅 CLI 日志
openclaw gateway --claude-cli-logs
```

### 常见问题解决

**网关启动失败**:
```bash
# 检查配置
openclaw config get gateway.mode

# 强制启动（开发模式）
openclaw gateway --dev --allow-unconfigured

# 杀死占用端口的进程
lsof -ti:18789 | xargs kill -9
```

**通道连接问题**:
```bash
# 重新登录
openclaw channels logout --channel <channel>
openclaw channels login --channel <channel>

# 查看通道日志
openclaw channels logs --channel <channel>
```

**会话问题**:
```bash
# 清理会话
openclaw sessions cleanup --enforce

# 重置特定会话
# 在聊天中发送：/reset
```

**技能问题**:
```bash
# 重新安装技能
openclaw clawhub install <skill> --force

# 检查技能配置
openclaw config get skills.entries
```

### 恢复模式

如果配置损坏：

```bash
# 备份当前配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup

# 重新运行向导
openclaw configure

# 或完全重置（开发模式）
openclaw gateway --dev --reset
```

---

# 附录

## 附录 A: 命令速查表

### 基础命令

| 命令 | 说明 |
|------|------|
| `openclaw --version` | 查看版本 |
| `openclaw --help` | 显示帮助 |
| `openclaw doctor` | 健康检查 |
| `openclaw status` | 查看状态 |
| `openclaw dashboard` | 打开 Web 控制台 |
| `openclaw configure` | 配置向导 |

### 网关命令

| 命令 | 说明 |
|------|------|
| `openclaw gateway` | 启动网关 |
| `openclaw gateway start` | 启动服务 |
| `openclaw gateway stop` | 停止服务 |
| `openclaw gateway restart` | 重启服务 |
| `openclaw gateway install` | 安装服务 |
| `openclaw gateway uninstall` | 卸载服务 |
| `openclaw gateway probe` | 探测网关 |
| `openclaw gateway discover` | 发现网关 |

### 通道命令

| 命令 | 说明 |
|------|------|
| `openclaw channels list` | 列出通道 |
| `openclaw channels status` | 查看状态 |
| `openclaw channels login` | 登录通道 |
| `openclaw channels logout` | 登出通道 |
| `openclaw channels add` | 添加账户 |
| `openclaw channels remove` | 移除账户 |
| `openclaw channels logs` | 查看日志 |

### 代理命令

| 命令 | 说明 |
|------|------|
| `openclaw agents list` | 列出代理 |
| `openclaw agents add` | 添加代理 |
| `openclaw agents delete` | 删除代理 |
| `openclaw agents bind` | 绑定通道 |
| `openclaw agents unbind` | 解绑通道 |
| `openclaw agents set-identity` | 设置身份 |

### 会话命令

| 命令 | 说明 |
|------|------|
| `openclaw sessions` | 列出会话 |
| `openclaw sessions --active 120` | 活跃会话 |
| `openclaw sessions cleanup` | 清理会话 |

### 技能命令

| 命令 | 说明 |
|------|------|
| `openclaw clawhub search` | 搜索技能 |
| `openclaw clawhub install` | 安装技能 |
| `openclaw clawhub update` | 更新技能 |
| `openclaw clawhub sync` | 同步技能 |
| `openclaw clawhub list` | 列出技能 |

### 浏览器命令

| 命令 | 说明 |
|------|------|
| `openclaw browser status` | 查看状态 |
| `openclaw browser start` | 启动浏览器 |
| `openclaw browser stop` | 停止浏览器 |
| `openclaw browser tabs` | 列出台灯 |
| `openclaw browser open` | 打开 URL |
| `openclaw browser snapshot` | 获取快照 |
| `openclaw browser screenshot` | 截图 |
| `openclaw browser click` | 点击元素 |
| `openclaw browser type` | 输入文本 |

### Cron 命令

| 命令 | 说明 |
|------|------|
| `openclaw cron list` | 列出任务 |
| `openclaw cron add` | 添加任务 |
| `openclaw cron edit` | 编辑任务 |
| `openclaw cron run` | 运行任务 |
| `openclaw cron runs` | 运行历史 |
| `openclaw cron remove` | 删除任务 |

### 配置命令

| 命令 | 说明 |
|------|------|
| `openclaw config get` | 获取配置 |
| `openclaw config set` | 设置配置 |
| `openclaw config unset` | 取消配置 |

## 附录 B: 工具参数参考

### read 工具

```json
{
  "tool": "read",
  "params": {
    "path": "string (required)",
    "offset": "number (optional)",
    "limit": "number (optional)"
  }
}
```

### write 工具

```json
{
  "tool": "write",
  "params": {
    "path": "string (required)",
    "content": "string (required)"
  }
}
```

### edit 工具

```json
{
  "tool": "edit",
  "params": {
    "path": "string (required)",
    "oldText": "string (required)",
    "newText": "string (required)"
  }
}
```

### exec 工具

```json
{
  "tool": "exec",
  "params": {
    "command": "string (required)",
    "workdir": "string (optional)",
    "env": "object (optional)",
    "yieldMs": "number (optional)",
    "background": "boolean (optional)",
    "timeout": "number (optional)",
    "pty": "boolean (optional)",
    "host": "string (optional)",
    "security": "string (optional)",
    "ask": "string (optional)",
    "node": "string (optional)",
    "elevated": "boolean (optional)"
  }
}
```

### web_search 工具

```json
{
  "tool": "web_search",
  "params": {
    "query": "string (required)",
    "count": "number (optional, 1-10)",
    "country": "string (optional)",
    "search_lang": "string (optional)",
    "ui_lang": "string (optional)",
    "freshness": "string (optional)"
  }
}
```

### browser 工具

```json
{
  "tool": "browser",
  "params": {
    "action": "string (required)",
    "profile": "string (optional)",
    "target": "string (optional)",
    "targetId": "string (optional)",
    "targetUrl": "string (optional)",
    "request": "object (optional)",
    "refs": "string (optional)",
    "selector": "string (optional)",
    "fullPage": "boolean (optional)",
    "timeoutMs": "number (optional)"
  }
}
```

## 附录 C: 资源链接

### 官方资源

- **官方网站**: https://openclaw.ai
- **官方文档**: https://docs.openclaw.ai
- **GitHub**: https://github.com/openclaw/openclaw
- **ClawHub**: https://clawhub.com

### 社区资源

- **Discord 社区**: (查看官方文档获取链接)
- **技能市场**: https://clawhub.com
- **问题追踪**: https://github.com/openclaw/openclaw/issues

### 学习资源

- **入门指南**: https://docs.openclaw.ai/start/getting-started
- **配置参考**: https://docs.openclaw.ai/gateway/configuration
- **通道文档**: https://docs.openclaw.ai/channels
- **工具文档**: https://docs.openclaw.ai/tools

## 附录 D: 社区支持

### 获取帮助

1. **查看文档**: https://docs.openclaw.ai
2. **搜索问题**: https://github.com/openclaw/openclaw/issues
3. **提交问题**: https://github.com/openclaw/openclaw/issues/new
4. **社区讨论**: (查看官方文档获取 Discord 链接)

### 贡献代码

1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

### 贡献技能

1. 创建技能文件夹
2. 编写 SKILL.md
3. 通过 ClawHub 发布

### 报告 Bug

报告 Bug 时请包含：
- OpenClaw 版本
- 操作系统和版本
- 重现步骤
- 错误日志
- 配置文件（脱敏后）

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2026.2.26 | 2026-02-27 | 当前版本 |
| 2026.2.25 | 2026-02-20 | 上一版本 |

## 许可证

OpenClaw 使用 MIT 许可证。详见 [LICENSE](https://github.com/openclaw/openclaw/blob/main/LICENSE)。

---

**🦞 Happy Clawning!**
