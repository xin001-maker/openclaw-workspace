# 🦞 OpenClaw 完全使用指南

> 让你的 AI 助手真正干活！从入门到精通的完整指南

**版本**: 2026.2.26  
**最后更新**: 2026-03-09  
**基于**: openclaw101.dev + 官方文档

---

## 📖 目录

### 第一部分：入门（第 1-3 天）
1. [什么是 OpenClaw](#1-什么是-openclaw)
2. [快速开始](#2-快速开始)
3. [核心概念](#3-核心概念)

### 第二部分：进阶（第 4-6 天）
4. [CLI 命令详解](#4-cli 命令详解)
5. [技能系统](#5-技能系统)
6. [工具系统](#6-工具系统)

### 第三部分：精通（第 7 天+）
7. [通道配置](#7-通道配置)
8. [高级功能](#8-高级功能)
9. [配置详解](#9-配置详解)
10. [最佳实践](#10-最佳实践)
11. [故障排除](#11-故障排除)
12. [资源汇总](#12-资源汇总)

---

# 1. 什么是 OpenClaw

## 🎯 一句话解释

**OpenClaw = 你的 24/7 个人 AI 助理**

它是一个开源平台，让你拥有完全可控的 AI 助手，通过你喜欢的聊天工具（微信、飞书、Telegram 等）随时访问。

## ✨ 核心特点

| 特点 | 说明 | 好处 |
|------|------|------|
| 🏠 **自托管** | 运行在你的服务器上 | 数据完全可控，隐私安全 |
| 💬 **多平台** | 支持飞书/微信/Telegram/Discord 等 | 随时随地访问 |
| 🔧 **可扩展** | 5494+ 社区技能 | 按需扩展功能 |
| 🔒 **隐私安全** | 数据不出你的服务器 | 企业级安全 |
| 💰 **零订阅** | 一次部署，免费使用 | 只需支付 API 费用 |

## 🎯 它能帮你做什么

### 工作场景
- 📧 自动回复邮件和消息
- 📅 管理日程和会议提醒
- 📊 数据分析和报告生成
- 💻 代码审查和调试
- 📝 文档编写和整理

### 学习场景
- 🔍 资料搜索和整理
- 📚 知识点总结
- 🎯 学习计划制定
- ✍️ 论文写作辅助

### 生活场景
- ⏰ 定时提醒
- 🌤️ 天气查询
- 📰 新闻摘要
- 🛒 购物清单管理

## 🆚 与其他 AI 工具的区别

| 特性 | OpenClaw | ChatGPT | 文心一言 |
|------|----------|---------|----------|
| 部署方式 | 自托管 | 云端 | 云端 |
| 数据控制 | 完全本地 | OpenAI 存储 | 百度存储 |
| 多平台 | 原生支持 | 单一应用 | 单一应用 |
| 定制化 | 高度可定制 | 有限 | 有限 |
| 成本 | 仅 API 费 | $20/月 | 免费/付费 |
| 隐私 | 数据不出本地 | 云端处理 | 云端处理 |
| 主动性 | 可主动工作 | 被动回复 | 被动回复 |

---

# 2. 快速开始

## ⏱️ 10 分钟上手指南

### 第一步：确认环境（1 分钟）

```bash
# 检查 Node.js 版本（需要 22+）
node --version

# 检查 OpenClaw 是否已安装
openclaw --version
```

### 第二步：启动网关（1 分钟）

```bash
# 启动网关服务
openclaw gateway start

# 检查状态
openclaw status
```

### 第三步：连接飞书（5 分钟）

你已经配置好了飞书通道，可以直接使用！

### 第四步：第一次对话（1 分钟）

在飞书中发送：
```
你好，请介绍一下你自己
```

### 第五步：尝试第一个任务（2 分钟）

发送：
```
帮我搜索最新的 AI 变现方式
```

---

## 📋 系统要求

### 硬件要求
| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| CPU | 任意现代 x64/ARM | 4 核+ |
| 内存 | 2GB | 4GB+ |
| 存储 | 1GB | 10GB+ |
| 网络 | 稳定连接 | 宽带 |

### 软件要求
- **Node.js**: 22 或更高版本
- **操作系统**: macOS、Linux、Windows（WSL2）
- **包管理器**: npm 或 pnpm

---

# 2.5 完整部署指南（小白专用）

## 🎯 部署方式选择

| 部署方式 | 适合人群 | 成本 | 难度 | 优点 |
|----------|----------|------|------|------|
| **本地部署** | 学习体验 | 免费 | ⭐⭐ | 零成本，快速上手 |
| **云服务器** | 7×24 运行 | ¥50-200/月 | ⭐⭐⭐ | 稳定，不用自己的电脑 |
| **阿里云一键** | 新手推荐 | ¥60-300/月 | ⭐ | 最简单，可视化配置 |
| **腾讯云一键** | 性价比 | ¥24-100/月 | ⭐ | 便宜，中文支持好 |

---

## 🖥️ 方式一：本地部署（适合学习）

### 适用场景
- ✅ 想先体验 OpenClaw 功能
- ✅ 有闲置电脑/笔记本
- ✅ 不需要 7×24 小时运行
- ✅ 预算有限（零成本）

### 部署步骤（15 分钟）

#### 步骤 1：安装 Node.js（5 分钟）

**Windows 用户**:
1. 访问 https://nodejs.org/
2. 下载 LTS 版本（22.x）
3. 双击安装，一路下一步

**macOS 用户**:
```bash
# 使用 Homebrew 安装
brew install node@22
```

**Linux 用户**:
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# CentOS/RHEL
curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -
sudo yum install -y nodejs
```

**验证安装**:
```bash
node --version  # 应该显示 v22.x.x
npm --version   # 应该显示 10.x.x
```

#### 步骤 2：安装 OpenClaw（3 分钟）

```bash
# 使用 npm 安装（推荐）
npm install -g openclaw@latest

# 或使用 pnpm
pnpm add -g openclaw@latest
```

**验证安装**:
```bash
openclaw --version
```

#### 步骤 3：运行入门向导（5 分钟）

```bash
openclaw onboard
```

向导会引导你完成：
1. ✅ 选择模型提供商（推荐：通义千问/MiniMax）
2. ✅ 输入 API Key（需要先去官网申请）
3. ✅ 选择是否安装技能（新手选 No）
4. ✅ 启用记忆功能（选 Yes）

#### 步骤 4：配置飞书通道（5 分钟）

**4.1 创建飞书应用**:
1. 访问 https://open.feishu.cn/app
2. 登录飞书账号
3. 点击"创建企业自建应用"
4. 填写应用名称（如"OpenClaw 助手"）
5. 点击"创建"

**4.2 添加机器人**:
1. 在应用管理页，点击"添加应用能力"
2. 选择"机器人"，点击"添加"
3. 打开机器人配置开关
4. 消息接收模式选择"Stream 模式"
5. 点击"发布"

**4.3 获取凭证**:
1. 在左侧菜单找到"凭据与基础信息"
2. 复制 App ID 和 App Secret

**4.4 配置通道**:
```bash
# 添加飞书通道
openclaw channels add

# 选择 Yes → 飞书
# 输入 App ID 和 App Secret
```

**4.5 配置权限**:
在飞书开发者平台"权限管理"中，批量导入以下权限：
```json
{
  "scopes": {
    "tenant": [
      "contact:user.base:readonly",
      "im:chat",
      "im:chat:read",
      "im:chat:update",
      "im:message",
      "im:message.p2p_msg:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ]
  }
}
```

**4.6 发布应用**:
1. 点击"版本管理与发布"
2. 创建新版本
3. 填写版本号和描述
4. 点击"保存并发布"

#### 步骤 5：启动网关（1 分钟）

```bash
# 启动网关
openclaw gateway start

# 查看状态
openclaw status

# 查看 Web 控制台
openclaw dashboard
```

#### 步骤 6：测试（1 分钟）

在飞书中找到你的应用，发送：
```
你好！
```

如果收到回复，说明部署成功！🎉

---

## ☁️ 方式二：阿里云一键部署（最简单）

### 适用场景
- ✅ 新手首选
- ✅ 需要 7×24 小时运行
- ✅ 预算充足（¥60-300/月）
- ✅ 想要最简单的方式

### 部署步骤（20 分钟）

#### 步骤 1：购买服务器（5 分钟）

1. 访问阿里云轻量应用服务器购买页：
   https://swasnext.console.aliyun.com/buy?regionId=us-east-1&planId=swas.s.c2m2s40b1.linux&imageId=9cea544bb4ce4046a164fe84ace83025

2. 配置选择：
   - **实例**: 内存必须 2GiB 及以上
   - **地域**: 默认美国（弗吉尼亚）
   - **购买时长**: 12 个月（可调整）

3. 点击"立即购买"，完成支付

#### 步骤 2：配置 OpenClaw（5 分钟）

1. 登录阿里云控制台：
   https://swasnext.console.aliyun.com/servers

2. 点击服务器卡片，进入详情页

3. 在"应用详情页签"中：
   - **端口放通**: 点击"执行命令"开放端口
   - **配置 API Key**: 点击"执行命令"配置百炼 API Key
   - **访问 Web UI**: 点击"执行命令"获取访问地址

#### 步骤 3：配置百炼 API Key（5 分钟）

1. 访问阿里云百炼平台：
   https://bailian.console.aliyun.com/

2. 创建 API Key：
   - 推荐购买 Coding Plan 套餐（固定月费，成本可控）
   - 支持模型：qwen3.5-plus、kimi-k2.5、MiniMax-M2.5、glm-5 等

3. 在 OpenClaw 控制台输入 API Key

#### 步骤 4：集成钉钉（可选，5 分钟）

**4.1 创建钉钉应用**:
1. 访问钉钉开放平台：
   https://open-dev.dingtalk.com/

2. 创建应用：
   - 选择或创建组织
   - 点击"创建应用"
   - 填写应用名称和描述

**4.2 配置机器人**:
1. 添加应用能力 → 选择"机器人"
2. 打开机器人配置开关
3. 消息接收模式选择"Stream 模式"
4. 点击"发布"

**4.3 配置凭证**:
1. 复制 Client ID 和 Client Secret
2. 在阿里云控制台填入

**4.4 测试**:
在钉钉群中添加机器人，@机器人进行测试

#### 费用说明

| 项目 | 费用 | 说明 |
|------|------|------|
| 服务器 | ¥60-300/月 | 根据配置不同 |
| 模型调用 | ¥0-100/月 | 推荐 Coding Plan 套餐 |
| **总计** | **¥60-400/月** | 新手建议 ¥100/月配置 |

---

## ☁️ 方式三：腾讯云一键部署（性价比）

### 适用场景
- ✅ 追求性价比
- ✅ 需要 7×24 小时运行
- ✅ 预算有限（¥24-100/月）
- ✅ 中文支持好

### 部署步骤（25 分钟）

#### 步骤 1：购买服务器（5 分钟）

**方式 A：新购实例**
1. 访问腾讯云 Lighthouse 购买页
2. 配置选择：
   - **应用创建方式**: 应用模板 > AI 智能体 > OpenClaw
   - **地域**: 优先选择海外（硅谷、弗吉尼亚、新加坡）
   - **套餐类型**: 锐驰型（推荐）
   - **套餐配置**: 2C2GB 或以上

**方式 B：重装旧实例**
1. 在 Lighthouse 控制台找到闲置实例
2. 点击"重装系统"
3. 选择应用模板 > AI 智能体 > OpenClaw
4. 确认重装

#### 步骤 2：登录服务器（3 分钟）

1. 在 Lighthouse 控制台点击"登录"
2. 选择"免密连接"
3. 点击"登录"进入 OrcaTerm

#### 步骤 3：运行配置向导（10 分钟）

```bash
# 运行配置命令
clawdbot onboard
```

**配置流程**:
1. **同意免责声明**: 选择 Yes
2. **配置模式**: 选择 QuickStart（快速入门）
3. **模型配置**:
   - 推荐选择国内厂商（MiniMax、Qwen、Moonshot AI、Z.AI/GLM）
   - 需要去对应官网申请 API Key
   - Kimi: https://platform.moonshot.ai/
   - MiniMax: https://platform.minimax.io/
   - GLM: https://z.ai/manage-apikey/apikey-list
4. **技能包**: 新手选择 No（后续可添加）
5. **Hooks**: 选择 Memory（启用记忆功能）

等待 30 秒 -1 分钟，部署完成

#### 步骤 4：配置飞书通道（7 分钟）

**4.1 创建飞书应用**:
1. 访问 https://open.feishu.cn/app
2. 创建企业自建应用
3. 添加机器人能力

**4.2 获取凭证**:
1. 在"凭据与基础信息"中复制 App ID 和 App Secret

**4.3 添加通道**:
```bash
# 返回终端运行
clawdbot channels add

# 选择 Yes → 飞书
# 输入 App ID 和 App Secret
```

**4.4 配置权限**:
在飞书开发者平台批量导入权限（参考本地部署部分）

**4.5 启动网关**:
```bash
clawdbot gateway --port 18789 --verbose
```

**4.6 测试**:
在飞书中找到应用，发送消息测试

#### 费用说明

| 项目 | 费用 | 说明 |
|------|------|------|
| 服务器 | ¥24-100/月 | 根据配置不同 |
| 模型调用 | ¥0-50/月 | 按使用量计费 |
| **总计** | **¥24-150/月** | 新手建议 ¥50/月配置 |

---

## 🆚 部署方式对比

| 特性 | 本地部署 | 阿里云 | 腾讯云 |
|------|----------|--------|--------|
| **成本** | 免费 | ¥60-400/月 | ¥24-150/月 |
| **难度** | ⭐⭐ | ⭐ | ⭐⭐ |
| **稳定性** | 依赖自家网络 | 企业级 | 企业级 |
| **7×24 运行** | ❌ 不推荐 | ✅ 支持 | ✅ 支持 |
| **适合人群** | 学习体验 | 企业用户 | 个人/小团队 |
| **配置时间** | 15 分钟 | 20 分钟 | 25 分钟 |

---

## 💡 新手建议

### 预算有限（学生党）
1. **先用本地部署**学习体验
2. 熟悉后再考虑云服务器
3. 推荐腾讯云（最便宜）

### 企业用户
1. **直接阿里云一键部署**
2. 配置 Coding Plan 套餐（成本可控）
3. 集成钉钉/飞书企业版

### 个人开发者
1. **腾讯云性价比最高**
2. 选择 2C2GB 配置（¥24/月）
3. 按需购买 API 额度

---

## ⚠️ 常见问题

### Q1: 本地部署后电脑能关机吗？
**不能**。本地部署需要电脑保持开机和网络连接。如果需要 7×24 运行，请选择云服务器。

### Q2: 云服务器需要备案吗？
**不需要**。OpenClaw 是个人使用工具，不涉及网站运营，无需备案。

### Q3: API Key 在哪里申请？
不同模型提供商有不同的官网：
- **通义千问**: https://bailian.console.aliyun.com/
- **Kimi**: https://platform.moonshot.ai/
- **MiniMax**: https://platform.minimax.io/
- **GLM**: https://z.ai/manage-apikey/apikey-list

### Q4: 一个月大概需要多少钱？
| 使用场景 | 月费用 |
|----------|--------|
| 轻度使用（每天几次） | ¥30-50 |
| 中度使用（工作辅助） | ¥50-100 |
| 重度使用（自动化业务） | ¥100-300 |

### Q5: 部署失败怎么办？
1. 检查 Node.js 版本（需要 22+）
2. 检查网络连接
3. 查看错误日志：`openclaw gateway logs`
4. 重启网关：`openclaw gateway restart`

### Q6: 可以多人使用吗？
**可以**。每个用户有独立的会话和记忆，支持多用户同时使用。

---

## 🔒 安全建议

### 基础安全
1. **修改默认 Token**
```bash
openclaw config set gateway.auth.token "新 Token"
```

2. **绑定本地回环**（仅本地访问）
```json5
{
  gateway: {
    bind: "loopback"
  }
}
```

3. **定期更新**
```bash
npm update -g openclaw
```

### 云服务器安全
1. **配置防火墙**：只开放必要端口
2. **使用 SSH 密钥**：不用密码登录
3. **定期备份**：备份配置文件和数据
4. **监控资源**：设置 CPU/内存告警

---

## 📚 相关资源

### 官方文档

| 资源 | 链接 | 说明 |
|------|------|------|
| 官方文档 | https://docs.openclaw.ai | 完整 API 参考 |
| GitHub | https://github.com/openclaw/openclaw | 源代码 |
| ClawHub | https://clawhub.com | 技能市场 |
| Discord | https://discord.gg/clawd | 社区 |

### 中文教程

| 教程 | 链接 | 类型 |
|------|------|------|
| 阿里云部署教程 | https://help.aliyun.com/zh/simple-application-server/use-cases/quickly-deploy-and-use-openclaw | 官方文档 |
| 腾讯云飞书对接 | https://cloud.tencent.com/developer/article/2625073 | 社区文章 |
| 飞书官方指南 | https://www.feishu.cn/content/article/7602519239445974205 | 官方文档 |
| 知乎深度解析 | https://zhuanlan.zhihu.com/p/2000850539936765122 | 技术文章 |

### 视频教程（强烈推荐⭐）

| 教程 | 平台 | 时长 | 链接 |
|------|------|------|------|
| **10 分钟保姆级教程** | B 站 | 10 分钟 | https://www.bilibili.com/video/BV1MfFAz6EnR/ |
| **超详细最强 AI 部署** | B 站 | 25 分钟 | https://www.bilibili.com/video/BV1fMfZBuEMj/ |
| **OpenClaw 海量全玩法** | B 站 | 45 分钟 | https://www.bilibili.com/video/BV1kH6nBFEPq/ |
| **本地部署接入微信/飞书/钉钉/QQ** | B 站 | 10 分钟 | https://www.bilibili.com/video/BV1MfFAz6EnR/ |
| **多 Agent 高级玩法** | B 站 | 30 分钟 | https://www.bilibili.com/video/BV1dqffBMEcg/ |
| **Kimi Claw 飞书自动化** | B 站 | 15 分钟 | https://www.bilibili.com/video/BV119ZtBAEe3/ |
| **硬件/软件成本实测** | B 站 | 20 分钟 | https://www.bilibili.com/video/BV1fJZjBdEov/ |
| **Full Setup Tutorial** | YouTube | 15 分钟 | https://www.youtube.com/watch?v=fcZMmP5dsl4 |
| **Secure Setup Guide** | YouTube | 20 分钟 | https://www.youtube.com/watch?v=YCD2FSvj35I |
| **Multi-Agent Setup** | YouTube | 25 分钟 | https://www.youtube.com/watch?v=LKjkYbT2M0Y |

### 安全资源

| 资源 | 链接 | 说明 |
|------|------|------|
| OpenClaw Security 101 | https://adversa.ai/blog/openclaw-security-101-vulnerabilities-hardening-2026/ | 安全入门 |
| SecureClaw | https://github.com/AdversaAI/SecureClaw | 安全加固插件 |
| 恶意技能分析 | https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html | 安全警告 |

### 社区项目

| 项目 | 链接 | 说明 |
|------|------|------|
| Awesome OpenClaw Skills | https://github.com/VoltAgent/awesome-openclaw-skills | 社区精选技能 |
| OpenClaw Mega Cheatsheet | https://moltfounders.com/openclaw-mega-cheatsheet | 150+ 命令速查 |
| 25+ Real Use Cases | https://www.forwardfuture.ai/p/what-people-are-actually-doing-with-openclaw-25-use-cases | 真实案例 |
| OpenClaw Newsletter | https://buttondown.com/openclaw-newsletter | 官方周刊 |

---

## 🎬 视频教程推荐（新手必看）

### 入门系列（按顺序观看）

#### 1️⃣ 快速上手（10 分钟）
**视频**: [本地部署接入微信/飞书/钉钉/QQ](https://www.bilibili.com/video/BV1MfFAz6EnR/)  
**内容**: 从零开始，10 分钟完成部署  
**适合**: 完全新手

#### 2️⃣ 完整部署（25 分钟）
**视频**: [超详细的最强 AI 部署教程](https://www.bilibili.com/video/BV1fMfZBuEMj/)  
**内容**: 详细讲解所有配置步骤  
**适合**: 想深入了解的用户

#### 3️⃣ 功能详解（45 分钟）
**视频**: [OpenClaw 海量全玩法攻略](https://www.bilibili.com/video/BV1kH6nBFEPq/)  
**内容**: 所有功能和玩法演示  
**适合**: 想全面掌握的用户

### 进阶系列

#### 4️⃣ 多 Agent 协作（30 分钟）
**视频**: [OpenClaw 多 Agent 高级玩法](https://www.bilibili.com/video/BV1dqffBMEcg/)  
**内容**: 多 Agent 架构和任务分配  
**适合**: 有基础用户

#### 5️⃣ 成本实测（20 分钟）
**视频**: [上手 OpenClaw 的硬件/软件成本有多高](https://www.bilibili.com/video/BV1fJZjBdEov/)  
**内容**: 三种设备方案成本对比  
**适合**: 考虑部署方案的用户

### 英文版（可选）

#### 6️⃣ Complete Setup Tutorial（15 分钟）
**视频**: [Full OpenClaw Setup Tutorial](https://www.youtube.com/watch?v=fcZMmP5dsl4)  
**内容**: 完整安装和配置流程  
**语言**: 英文

#### 7️⃣ Secure Setup（20 分钟）
**视频**: [SECURE OpenClaw Setup Guide](https://www.youtube.com/watch?v=YCD2FSvj35I)  
**内容**: 安全部署指南  
**语言**: 英文

---

## 💡 学习建议

### 新手学习路径

1. **第 1 天**: 观看视频 1（10 分钟）→ 本地部署体验
2. **第 2 天**: 观看视频 2（25 分钟）→ 深入理解配置
3. **第 3 天**: 观看视频 3（45 分钟）→ 了解所有功能
4. **第 4-7 天**: 实践本手册内容 → 完成 7 天学习路径

### 企业部署路径

1. **第 1 天**: 观看视频 1+2 → 理解部署流程
2. **第 2 天**: 选择云服务商 → 阿里云/腾讯云一键部署
3. **第 3 天**: 集成企业 IM（飞书/钉钉）
4. **第 4-7 天**: 定制业务场景 → 客服/数据/自动化

### 开发者路径

1. **第 1-2 天**: 完成基础部署
2. **第 3-4 天**: 学习技能开发（参考官方文档）
3. **第 5-7 天**: 开发自定义技能
4. **第 2 周**: 发布到 ClawHub

---

## 📖 配套文档

| 文档 | 用途 | 位置 |
|------|------|------|
| 本手册 | 完整使用指南 | 当前文档 |
| 官方文档 | API 和技术细节 | https://docs.openclaw.ai |
| GitHub Wiki | 社区贡献内容 | https://github.com/openclaw/openclaw/wiki |
| 技能开发文档 | 开发自定义技能 | https://docs.openclaw.ai/tools/clawhub |

---

# 3. 核心概念

## 3.1 会话（Session）

### 什么是会话

会话是对话的基本单位，每个会话有独立的上下文和记忆。

### 会话类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| 直接消息 | 你和 AI 的私聊 | 日常工作 |
| 群聊 | 群组对话 | 团队协作 |
| 定时任务 | Cron 触发的会话 | 自动任务 |
| 子代理 | 后台运行的会话 | 长时间任务 |

### 会话管理

```bash
# 查看所有会话
openclaw sessions

# 查看活跃会话（最近 2 小时）
openclaw sessions --active 120

# 清理过期会话
openclaw sessions cleanup
```

### 聊天中的会话命令

在飞书中发送：
- `/status` - 查看会话状态
- `/new` - 开始新会话
- `/compact` - 压缩上下文
- `/stop` - 停止当前运行

## 3.2 子代理（Subagent）

### 什么是子代理

子代理是后台运行的 AI，可以独立完成任务后汇报结果。

### 使用场景

- 🔍 长时间研究任务
- 📊 数据分析
- 📝 批量处理
- 🤖 多代理协作

### 基本用法

**在聊天中**:
```
/subagents spawn "研究 Python 自动化变现项目"
```

**查看子代理**:
```
/subagents list
```

**查看日志**:
```
/subagents log <id>
```

### 配置示例

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxConcurrent: 8,        // 最大并发数
        runTimeoutSeconds: 900   // 默认超时 15 分钟
      }
    }
  }
}
```

## 3.3 技能（Skill）

### 什么是技能

技能是 AI 的能力扩展包，每个技能教会 AI 做一件事。

### 技能分类（31 个类别）

| 类别 | 数量 | 代表技能 |
|------|------|----------|
| 🧠 AI & LLMs | 159 | 模型调用、提示词优化 |
| 🔍 Search & Research | 148 | 网络搜索、文献查找 |
| ☁️ DevOps & Cloud | 144 | 部署、监控、CI/CD |
| 📈 Marketing & Sales | 94 | 邮件营销、SEO |
| 💬 Communication | 58 | 消息发送、邮件 |
| 🤖 Coding Agents | 55 | 代码生成、审查 |
| 🏠 Smart Home & IoT | 50 | 智能家居控制 |
| 🌐 Web & Frontend | 46 | 网页操作、测试 |
| 🗣️ Speech & Audio | 44 | 语音合成、识别 |
| 📝 Notes & PKM | 61 | 笔记管理、知识库 |
| 🏋️ Health & Fitness | 35 | 健康追踪 |
| 🎮 Gaming | 7 | 游戏自动化 |

**总计**: 5494+ 技能

### 安装技能

```bash
# 安装单个技能
npx clawhub@latest install <技能名>

# 示例：安装天气技能
npx clawhub@latest install weather

# 查看已安装技能
npx clawhub@latest list
```

### ⚠️ 安全警告

**重要**: ClawHub 曾发现恶意技能窃取用户数据！

**安全原则**:
1. ✅ 只安装可信技能
2. ✅ 检查源代码
3. ✅ 查看作者信息
4. ✅ 不要安装要求过多权限的技能

**推荐技能**（已验证安全）:
- weather - 天气查询
- brave-search - 网络搜索
- github - GitHub 操作
- notion - Notion 管理
- summarize - 内容摘要

## 3.4 工具（Tool）

### 核心工具

| 工具 | 用途 | 示例 |
|------|------|------|
| `read` | 读取文件 | 读取配置文件 |
| `write` | 写入文件 | 创建新文件 |
| `edit` | 编辑文件 | 精确文本替换 |
| `exec` | 执行命令 | 运行 shell 命令 |
| `process` | 管理进程 | 后台任务管理 |
| `web_search` | 网络搜索 | 搜索信息 |
| `web_fetch` | 获取网页 | 提取网页内容 |
| `browser` | 浏览器控制 | 自动化操作 |
| `message` | 发送消息 | 飞书消息 |
| `sessions_spawn` | 创建子代理 | 后台任务 |

### 工具使用示例

**读取文件**:
```
帮我读取 /root/可交付文件/README.md 的内容
```

**执行命令**:
```
运行命令：ls -la /root/可交付文件/
```

**网络搜索**:
```
搜索 2026 年最新的 AI 变现方式
```

---

# 4. CLI 命令详解

## 基础命令

### openclaw --help
查看所有可用命令

### openclaw --version
查看版本号

### openclaw status
查看系统运行状态

```bash
$ openclaw status

OpenClaw 2026.2.26
Gateway: running (pid 124766)
Channel: feishu (connected)
Sessions: 8 active
Memory: 0 files
```

### openclaw doctor
健康检查，诊断常见问题

## 网关管理

### openclaw gateway
启动网关（前台运行）

### openclaw gateway start
启动网关（后台服务）

### openclaw gateway stop
停止网关

### openclaw gateway restart
重启网关

### openclaw gateway watch
开发模式，自动重载

## 会话管理

### openclaw sessions
列出所有会话

```bash
# 显示最近 2 小时的活跃会话
openclaw sessions --active 120

# 限制显示数量
openclaw sessions --limit 10
```

### openclaw sessions cleanup
清理过期会话

```bash
# 预览（不实际执行）
openclaw sessions cleanup --dry-run

# 强制执行
openclaw sessions cleanup --enforce
```

## 通道管理

### openclaw channels
管理聊天通道

```bash
# 列出已连接通道
openclaw channels list

# 登录新通道
openclaw channels login --channel telegram

# 登出
openclaw channels logout --channel telegram
```

## 技能管理

### openclaw skills
管理工作空间技能

```bash
# 列出技能
openclaw skills list

# 启用技能
openclaw skills enable weather

# 禁用技能
openclaw skills disable weather
```

## 配置管理

### openclaw config
配置管理

```bash
# 查看所有配置
openclaw config get

# 查看特定配置
openclaw config get gateway.port

# 设置配置
openclaw config set gateway.port 19001

# 重置配置
openclaw config unset gateway.port
```

### openclaw configure
交互式配置向导

## 浏览器控制

### openclaw browser
管理浏览器

```bash
# 查看状态
openclaw browser status

# 启动浏览器
openclaw browser start

# 停止浏览器
openclaw browser stop

# 截图
openclaw browser screenshot
```

## 定时任务

### openclaw cron
管理定时任务

```bash
# 列出任务
openclaw cron list

# 添加任务
openclaw cron add --name "daily-report" --cron "0 9 * * *" --message "生成日报"

# 删除任务
openclaw cron rm <id>

# 运行任务
openclaw cron run <id>

# 查看运行记录
openclaw cron runs
```

## 其他命令

### openclaw dashboard
打开 Web 控制台

### openclaw agents
管理 Agent

```bash
# 列出 Agent
openclaw agents list

# 添加 Agent
openclaw agents add my-agent

# 删除 Agent
openclaw agents remove my-agent
```

### openclaw memory
管理记忆系统

```bash
# 查看记忆
openclaw memory search "关键词"

# 清理记忆
openclaw memory cleanup
```

---

# 5. 技能系统

## 5.1 技能结构

每个技能是一个文件夹，包含：

```
skill-name/
├── SKILL.md          # 主要说明文件
├── assets/           # 资源文件
├── scripts/          # 脚本文件
└── _meta.json        # 元数据
```

### SKILL.md 格式

```markdown
---
name: 技能名称
version: 1.0.0
description: 技能描述
author: 作者名
---

# 技能说明

这里是详细的使用说明...

## 使用方法

1. 第一步...
2. 第二步...

## 示例

示例代码或用法...
```

## 5.2 技能加载顺序

技能从三个位置加载（优先级从高到低）：

1. **工作空间技能**: `/root/.openclaw/workspace/skills/` ⭐⭐⭐
2. **本地技能**: `~/.openclaw/skills/` ⭐⭐
3. **捆绑技能**: 安装自带 ⭐

## 5.3 技能门控

技能可以通过条件控制是否加载：

```json5
{
  metadata: {
    openclaw: {
      requires: {
        bins: ["python3", "git"],     // 需要的二进制
        env: ["API_KEY"],             // 需要的环境变量
        config: ["gateway.port"]      // 需要的配置项
      },
      os: ["linux", "macos"]          // 支持的操作系统
    }
  }
}
```

## 5.4 配置技能

在 `openclaw.json` 中配置：

```json5
{
  skills: {
    entries: {
      "weather": {
        enabled: true,
        apiKey: "YOUR_API_KEY"
      },
      "brave-search": {
        enabled: true,
        apiKey: "YOUR_API_KEY"
      }
    }
  }
}
```

## 5.5 开发技能

### 创建技能

```bash
# 创建技能文件夹
mkdir -p /root/.openclaw/workspace/skills/my-skill

# 创建 SKILL.md
cat > /root/.openclaw/workspace/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
version: 1.0.0
description: 我的自定义技能
---

# 技能说明

这里写详细说明...
EOF
```

### 测试技能

```bash
# 重新加载技能
openclaw skills reload

# 测试技能
openclaw skills test my-skill
```

### 发布技能

```bash
# 发布到 ClawHub
npx clawhub@latest publish /root/.openclaw/workspace/skills/my-skill
```

---

## 5.6 必装技能推荐（109 个精选）

> 从 5490+ 技能中精选的高价值技能，按优先级分类推荐

### ⭐⭐⭐ 优先级 S：新手必装（10 个）

这些技能是 OpenClaw 的核心功能，安装后即可使用基础能力。

| # | 技能 | 用途 | 安装命令 | 使用场景 |
|---|------|------|----------|----------|
| 1 | **brave-search** | 网络搜索 | `npx clawhub@latest install brave-search` | 搜索资讯、查找文档、验证事实 |
| 2 | **weather** | 天气查询 | `npx clawhub@latest install weather` | 每日出行、活动安排 |
| 3 | **github** | GitHub 操作 | `npx clawhub@latest install github` | 管理仓库、Issues、PRs |
| 4 | **summarize** | 内容摘要 | `npx clawhub@latest install summarize` | 总结文章、视频、会议记录 |
| 5 | **agent-browser** | 浏览器自动化 | `npx clawhub@latest install agent-browser` | 网页抓取、自动化测试、截图 |
| 6 | **notion** | Notion 管理 | `npx clawhub@latest install notion` | 创建笔记、管理任务、知识库 |
| 7 | **google-calendar** | 日历管理 | `npx clawhub@latest install google-calendar` | 创建会议、查看日程、提醒 |
| 8 | **gmail** | 邮件发送 | `npx clawhub@latest install gmail` | 发送邮件、查看收件箱 |
| 9 | **file-manager** | 文件管理 | `npx clawhub@latest install file-manager` | 文件整理、批量重命名 |
| 10 | **system-monitor** | 系统监控 | `npx clawhub@latest install system-monitor` | CPU/内存监控、性能优化 |

**新手包一键安装**:
```bash
for skill in brave-search weather github summarize agent-browser notion google-calendar gmail file-manager system-monitor; do
  npx clawhub@latest install $skill
done
```

---

### ⭐⭐ 优先级 A：强烈推荐（30 个）

#### 🔍 搜索与研究（5 个）

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| academic-research | 学术论文搜索 | `npx clawhub@latest install academic-research` |
| arxiv-search | arXiv 论文 | `npx clawhub@latest install arxiv-search` |
| google-scholar | 谷歌学术 | `npx clawhub@latest install google-scholar` |
| wikipedia | 维基百科 | `npx clawhub@latest install wikipedia` |
| news-search | 新闻搜索 | `npx clawhub@latest install news-search` |

#### 🤖 编程与开发（10 个）

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| python-executor | Python 执行 | `npx clawhub@latest install python-executor` |
| code-review | 代码审查 | `npx clawhub@latest install code-review` |
| sql-query | SQL 查询 | `npx clawhub@latest install sql-query` |
| api-tester | API 测试 | `npx clawhub@latest install api-tester` |
| docker-manager | Docker 管理 | `npx clawhub@latest install docker-manager` |
| git-automation | Git 自动化 | `npx clawhub@latest install git-automation` |
| vscode-integration | VSCode 集成 | `npx clawhub@latest install vscode-integration` |
| npm-manager | NPM 包管理 | `npx clawhub@latest install npm-manager` |
| regex-helper | 正则助手 | `npx clawhub@latest install regex-helper` |
| documentation-generator | 文档生成 | `npx clawhub@latest install documentation-generator` |

#### 🌐 Web 与前端（5 个）

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| web-scraper | 网页爬虫 | `npx clawhub@latest install web-scraper` |
| seo-analyzer | SEO 分析 | `npx clawhub@latest install seo-analyzer` |
| website-monitor | 网站监控 | `npx clawhub@latest install website-monitor` |
| screenshot-tool | 截图工具 | `npx clawhub@latest install screenshot-tool` |
| link-checker | 链接检查 | `npx clawhub@latest install link-checker` |

#### ☁️ DevOps 与云（5 个）

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| aws-cli | AWS 管理 | `npx clawhub@latest install aws-cli` |
| aliyun-cli | 阿里云 CLI | `npx clawhub@latest install aliyun-cli` |
| tencent-cloud | 腾讯云 CLI | `npx clawhub@latest install tencent-cloud` |
| k8s-manager | K8s 管理 | `npx clawhub@latest install k8s-manager` |
| ci-cd-automation | CI/CD 自动化 | `npx clawhub@latest install ci-cd-automation` |

#### 🧠 AI 与 LLM（5 个）

| 技能 | 用途 | 安装命令 |
|------|------|----------|
| openai-api | OpenAI API | `npx clawhub@latest install openai-api` |
| claude-api | Claude API | `npx clawhub@latest install claude-api` |
| stable-diffusion | 图像生成 | `npx clawhub@latest install stable-diffusion` |
| tts-skill | 语音合成 | `npx clawhub@latest install tts-skill` |
| speech-to-text | 语音识别 | `npx clawhub@latest install speech-to-text` |

---

### ⭐ 优先级 B：按需安装（69 个）

#### 📝 笔记与知识管理（5 个）
- **obsidian** - Obsidian 笔记：`npx clawhub@latest install obsidian`
- **evernote** - 印象笔记：`npx clawhub@latest install evernote`
- **roam-research** - Roam Research：`npx clawhub@latest install roam-research`
- **logseq** - Logseq：`npx clawhub@latest install logseq`
- **zettelkasten** - 卡片盒笔记：`npx clawhub@latest install zettelkasten`

#### 🏠 智能家居与 IoT（3 个）
- **home-assistant** - Home Assistant：`npx clawhub@latest install home-assistant`
- **xiaomi-home** - 小米智能家居：`npx clawhub@latest install xiaomi-home`
- **philips-hue** - 飞利浦 Hue：`npx clawhub@latest install philips-hue`

#### 🗣️ 语音与音频（4 个）
- **elevenlabs** - ElevenLabs TTS：`npx clawhub@latest install elevenlabs`
- **whisper** - Whisper 语音识别：`npx clawhub@latest install whisper`
- **spotify-control** - Spotify 控制：`npx clawhub@latest install spotify-control`
- **podcast-manager** - 播客管理：`npx clawhub@latest install podcast-manager`

#### 📊 数据分析（3 个）
- **excel-automation** - Excel 自动化：`npx clawhub@latest install excel-automation`
- **data-visualization** - 数据可视化：`npx clawhub@latest install data-visualization`
- **google-analytics** - Google Analytics：`npx clawhub@latest install google-analytics`

#### 🛡️ 安全与密码（5 个）
- **password-manager** - 密码管理器：`npx clawhub@latest install password-manager`
- **vpn-manager** - VPN 管理：`npx clawhub@latest install vpn-manager`
- **security-scan** - 安全扫描：`npx clawhub@latest install security-scan`
- **two-factor-auth** - 双因素认证：`npx clawhub@latest install two-factor-auth`
- **encryption-tool** - 加密工具：`npx clawhub@latest install encryption-tool`

---

### 🎯 按场景推荐技能包

#### 场景 1：个人效率提升
```bash
npx clawhub@latest install brave-search weather google-calendar notion file-manager summarize
```

#### 场景 2：开发者工具包
```bash
npx clawhub@latest install github python-executor code-review docker-manager git-automation vscode-integration
```

#### 场景 3：数字营销自动化
```bash
npx clawhub@latest install social-media-manager content-generator analytics-dashboard email-automation seo-analyzer
```

#### 场景 4：学术研究助手
```bash
npx clawhub@latest install academic-research arxiv-search google-scholar summarize documentation-generator
```

#### 场景 5：企业运维监控
```bash
npx clawhub@latest install system-monitor aws-cli k8s-manager ci-cd-automation website-monitor
```

---

### ⚠️ 技能安全提醒

**安装前检查清单**:
1. ✅ **查看源代码** - 访问 GitHub 仓库检查 SKILL.md
2. ✅ **检查作者** - 确认是可信开发者
3. ✅ **权限审查** - 检查是否过度授权
4. ✅ **VirusTotal 扫描** - 在 ClawHub 查看安全报告

**避免安装**:
- ❌ 要求系统 root 权限
- ❌ 访问敏感文件（密码、密钥）
- ❌ 网络请求到不明域名
- ❌ 加密/混淆代码
- ❌ 无源代码或描述过简

---

### 📊 技能使用统计

**最受欢迎技能 TOP 10**:

| 排名 | 技能 | 安装量 | 类别 |
|------|------|--------|------|
| 1 | brave-search | 50,000+ | 搜索 |
| 2 | github | 45,000+ | 开发 |
| 3 | weather | 40,000+ | 生活 |
| 4 | agent-browser | 35,000+ | 自动化 |
| 5 | summarize | 30,000+ | 效率 |
| 6 | notion | 28,000+ | 笔记 |
| 7 | openai-api | 25,000+ | AI |
| 8 | google-calendar | 22,000+ | 日历 |
| 9 | python-executor | 20,000+ | 开发 |
| 10 | web-scraper | 18,000+ | 爬虫 |

---

### 🔧 技能管理命令

```bash
# 查看已安装技能
npx clawhub@latest list

# 查看技能详情
npx clawhub@latest info <skill-name>

# 更新单个技能
npx clawhub@latest update <skill-name>

# 更新所有技能
npx clawhub@latest update-all

# 卸载技能
npx clawhub@latest uninstall <skill-name>

# 禁用/启用技能
openclaw skills disable <skill-name>
openclaw skills enable <skill-name>
```

---

# 6. 工具系统

## 6.1 文件操作工具

### read - 读取文件

```json
{
  "tool": "read",
  "params": {
    "path": "/path/to/file.txt",
    "offset": 1,      // 从第几行开始
    "limit": 100      // 最多读多少行
  }
}
```

### write - 写入文件

```json
{
  "tool": "write",
  "params": {
    "path": "/path/to/file.txt",
    "content": "文件内容"
  }
}
```

### edit - 编辑文件

```json
{
  "tool": "edit",
  "params": {
    "path": "/path/to/file.txt",
    "oldText": "要替换的原文",
    "newText": "替换后的内容"
  }
}
```

## 6.2 网络工具

### web_search - 网络搜索

```json
{
  "tool": "web_search",
  "params": {
    "query": "搜索关键词",
    "count": 10,           // 结果数量
    "freshness": "pd",     // 时间过滤：pd=今天，pw=本周，pm=本月
    "country": "CN"        // 国家
  }
}
```

### web_fetch - 获取网页

```json
{
  "tool": "web_fetch",
  "params": {
    "url": "https://example.com",
    "extractMode": "markdown",  // markdown 或 text
    "maxChars": 50000           // 最大字符数
  }
}
```

## 6.3 浏览器工具

### browser - 浏览器控制

```json
{
  "tool": "browser",
  "params": {
    "action": "open",
    "targetUrl": "https://example.com",
    "target": "sandbox"    // sandbox 或 host
  }
}
```

### 常用浏览器操作

| 操作 | action | 参数 |
|------|--------|------|
| 打开网页 | open | targetUrl |
| 截图 | screenshot | fullPage |
| 快照 | snapshot | refs |
| 点击 | act | request.kind="click" |
| 输入 | act | request.kind="type" |

## 6.4 消息工具

### message - 发送消息

```json
{
  "tool": "message",
  "params": {
    "action": "send",
    "channel": "feishu",
    "message": "消息内容",
    "target": "用户 ID"
  }
}
```

## 6.5 会话工具

### sessions_spawn - 创建子代理

```json
{
  "tool": "sessions_spawn",
  "params": {
    "task": "任务描述",
    "mode": "run",           // run 或 session
    "runtime": "subagent",   // subagent 或 acp
    "label": "任务标签",
    "timeoutSeconds": 3600
  }
}
```

### sessions_list - 列出会话

```json
{
  "tool": "sessions_list",
  "params": {
    "limit": 10,
    "activeMinutes": 120
  }
}
```

### sessions_history - 查看历史

```json
{
  "tool": "sessions_history",
  "params": {
    "sessionKey": "会话键",
    "limit": 50
  }
}
```

---

# 7. 通道配置

## 7.1 支持的通道

| 通道 | 状态 | 配置难度 |
|------|------|----------|
| 飞书 | ✅ 已配置 | 简单 |
| 钉钉 | ✅ 支持 | 简单 |
| 企业微信 | ✅ 支持 | 中等 |
| QQ | ✅ 支持 | 中等 |
| Telegram | ✅ 支持 | 简单 |
| Discord | ✅ 支持 | 简单 |
| WhatsApp | ✅ 支持 | 中等 |
| Slack | ✅ 支持 | 简单 |

## 7.2 飞书配置（已完成）

你的飞书已配置好，配置信息：

```json5
{
  channels: {
    feishu: {
      enabled: true,
      appId: "cli_a92150ac7db85bdb",
      appSecret: "IRsDHt9SFzGUwWmYPkym8bza7u8AHE5l",
      domain: "feishu",
      groupPolicy: "open"
    }
  }
}
```

## 7.3 添加新通道

### Telegram

```bash
# 通过 BotFather 创建机器人
# 获取 Token

# 配置
openclaw config set channels.telegram.enabled true
openclaw config set channels.telegram.token "YOUR_BOT_TOKEN"

# 重启网关
openclaw gateway restart
```

### Discord

```bash
# 在 Discord Developer Portal 创建应用
# 获取 Token

# 配置
openclaw config set channels.discord.enabled true
openclaw config set channels.discord.token "YOUR_BOT_TOKEN"

# 重启网关
openclaw gateway restart
```

---

# 8. 高级功能

## 8.1 多 Agent 系统

### 创建多个 Agent

```bash
# 创建工作 Agent
openclaw agents add work-agent

# 配置工作 Agent
openclaw configure --agent work-agent

# 切换 Agent
openclaw agents use work-agent
```

### Agent 隔离

每个 Agent 有独立的：
- 会话历史
- 记忆系统
- 工作空间
- 配置

## 8.2 定时任务（Cron）

### 创建定时任务

```bash
# 每天早上 9 点发送日报
openclaw cron add \
  --name "daily-report" \
  --cron "0 9 * * *" \
  --message "生成今日工作报告"
```

### Cron 表达式

| 字段 | 允许值 | 特殊字符 |
|------|--------|----------|
| 分钟 | 0-59 | , - * / |
| 小时 | 0-23 | , - * / |
| 日期 | 1-31 | , - * / |
| 月份 | 1-12 | , - * / |
| 星期 | 0-7 | , - * / |

**示例**:
- `0 9 * * *` - 每天早上 9 点
- `*/30 * * * *` - 每 30 分钟
- `0 0 * * 1` - 每周一凌晨
- `0 0 1 * *` - 每月 1 号凌晨

## 8.3 记忆系统

### 记忆类型

| 类型 | 文件 | 用途 |
|------|------|------|
| 长期记忆 | MEMORY.md | 重要信息永久保存 |
| 短期记忆 | memory/YYYY-MM-DD.md | 每日工作记录 |
| 工作记忆 | SESSION-STATE.md | 当前工作状态 |
| 缓冲记忆 | memory/working-buffer.md | 上下文缓冲 |

### 记忆操作

```bash
# 搜索记忆
openclaw memory search "关键词"

# 查看记忆
openclaw memory get MEMORY.md

# 清理记忆
openclaw memory cleanup
```

## 8.4 浏览器自动化

### 使用场景

- 网页数据抓取
- 自动化测试
- 批量操作
- 监控网页变化

### 基本用法

```json
{
  "tool": "browser",
  "params": {
    "action": "open",
    "targetUrl": "https://example.com"
  }
}
```

### 高级用法

```json
{
  "tool": "browser",
  "params": {
    "action": "snapshot",
    "refs": "aria"
  }
}
```

---

# 9. 配置详解

## 9.1 配置文件位置

```
~/.openclaw/openclaw.json  # 主配置文件
```

## 9.2 配置结构

```json5
{
  meta: {
    lastTouchedVersion: "2026.2.26",
    lastTouchedAt: "2026-03-08T02:51:49.238Z"
  },
  
  agents: {
    defaults: {
      workspace: "/root/.openclaw/workspace",
      model: {
        primary: "qwencode/qwen3.5-plus"
      },
      subagents: {
        maxConcurrent: 8
      }
    }
  },
  
  gateway: {
    port: 18789,
    mode: "local",
    bind: "loopback",
    auth: {
      mode: "token",
      token: "YOUR_TOKEN"
    }
  },
  
  channels: {
    feishu: {
      enabled: true,
      appId: "YOUR_APP_ID",
      appSecret: "YOUR_APP_SECRET"
    }
  },
  
  skills: {
    install: {
      nodeManager: "npm"
    },
    entries: {
      "weather": {
        enabled: true
      }
    }
  },
  
  models: {
    providers: {
      "qwencode": {
        baseUrl: "https://coding.dashscope.aliyuncs.com/v1",
        apiKey: "YOUR_API_KEY"
      }
    }
  }
}
```

## 9.3 环境变量

可以用环境变量覆盖配置：

```bash
export OPENCLAW_GATEWAY_PORT=19001
export OPENCLAW_MODEL_PRIMARY="anthropic/claude-3-5-sonnet"
export BRAVE_API_KEY="YOUR_KEY"
```

---

# 10. 最佳实践

## 10.1 安全配置

### 基础安全

1. **修改默认 Token**
```bash
openclaw config set gateway.auth.token "新 Token"
```

2. **绑定本地回环**
```json5
{
  gateway: {
    bind: "loopback"  // 只允许本地访问
  }
}
```

3. **定期更新**
```bash
npm update -g openclaw
```

### 技能安全

1. **只安装可信技能**
2. **检查源代码**
3. **限制权限**
4. **使用 VirusTotal 扫描**

## 10.2 性能优化

### 内存管理

```json5
{
  agents: {
    defaults: {
      compaction: {
        mode: "safeguard"  // 自动压缩上下文
      }
    }
  }
}
```

### 并发控制

```json5
{
  agents: {
    defaults: {
      maxConcurrent: 4,      // 最大并发 Agent 数
      subagents: {
        maxConcurrent: 8     // 最大并发子代理数
      }
    }
  }
}
```

## 10.3 备份策略

### 配置备份

```bash
# 备份配置
cp ~/.openclaw/openclaw.json ~/backup/openclaw.json.bak

# 备份工作空间
cp -r ~/.openclaw/workspace ~/backup/workspace.bak
```

### 记忆备份

```bash
# 备份记忆
cp -r ~/.openclaw/workspace/memory ~/backup/memory.bak
```

## 10.4 监控和日志

### 查看日志

```bash
# 查看网关日志
openclaw gateway logs

# 实时日志
tail -f ~/.openclaw/logs/gateway.log
```

### 性能监控

```bash
# 查看状态
openclaw status

# 查看会话
openclaw sessions --active 60
```

---

# 11. 故障排除

## 11.1 常见问题

### Q1: 网关无法启动

**症状**: `openclaw gateway start` 失败

**解决**:
```bash
# 检查端口占用
lsof -i :18789

# 更换端口
openclaw config set gateway.port 19001

# 重启
openclaw gateway restart
```

### Q2: 飞书消息不回复

**症状**: 飞书发消息，AI 不回复

**解决**:
```bash
# 检查通道状态
openclaw channels list

# 重新登录
openclaw channels logout --channel feishu
openclaw channels login --channel feishu

# 检查配置
openclaw config get channels.feishu
```

### Q3: 子代理不工作

**症状**: `/subagents spawn` 无响应

**解决**:
```bash
# 检查子代理状态
/subagents list

# 查看日志
/subagents log <id>

# 检查配置
openclaw config get agents.defaults.subagents
```

### Q4: 内存占用过高

**症状**: 系统变慢，内存不足

**解决**:
```bash
# 压缩上下文
/compact

# 清理会话
openclaw sessions cleanup --enforce

# 重启网关
openclaw gateway restart
```

## 11.2 诊断工具

### openclaw doctor

运行健康检查：
```bash
openclaw doctor
```

会检查：
- Node.js 版本
- 网关状态
- 通道连接
- 配置文件
- 权限问题

### openclaw status

查看系统状态：
```bash
openclaw status
```

显示：
- 网关状态
- 通道状态
- 会话数量
- 内存使用
- 模型配置

---

# 12. 资源汇总

## 12.1 官方资源

| 资源 | 链接 | 说明 |
|------|------|------|
| 官方文档 | https://docs.openclaw.ai | 完整 API 参考 |
| GitHub | https://github.com/openclaw/openclaw | 源代码 |
| ClawHub | https://clawhub.com | 技能市场 |
| Discord | https://discord.gg/clawd | 社区 |

## 12.2 中文教程

| 教程 | 来源 | 类型 |
|------|------|------|
| 阿里云部署教程 | 阿里云 | 云部署 |
| 腾讯云飞书对接 | 腾讯云 | 平台对接 |
| B 站视频教程 | Bilibili | 视频教学 |
| 知乎深度解析 | 知乎 | 技术文章 |
| 飞书官方指南 | 飞书 | 官方文档 |

## 12.3 视频教程

| 教程 | 平台 | 时长 |
|------|------|------|
| 10 分钟快速上手 | YouTube | 10 分钟 |
| 完整系统课程 | YouTube | 2 小时 |
| 多 Agent 实战 | B 站 | 30 分钟 |
| 安全部署指南 | YouTube | 20 分钟 |

## 12.4 安全资源

| 资源 | 说明 |
|------|------|
| OpenClaw Security 101 | 安全入门指南 |
| SecureClaw | 安全加固插件 |
| NanoClaw | 安全替代版本 |
| ClawHavoc 分析 | 恶意技能分析报告 |

## 12.5 社区项目

| 项目 | 说明 |
|------|------|
| Awesome OpenClaw Skills | 社区精选技能 |
| OpenClaw Mega Cheatsheet | 150+ 命令速查 |
| 25+ Real Use Cases | 真实案例集 |
| OpenClaw Newsletter | 官方周刊 |

---

## 📚 学习路径总结

### 第 1 天：入门
- ✅ 了解 OpenClaw 是什么
- ✅ 完成快速开始
- ✅ 发送第一条消息

### 第 2 天：基础
- ✅ 掌握 CLI 命令
- ✅ 理解会话概念
- ✅ 学会查看状态

### 第 3 天：技能
- ✅ 安装 3-5 个技能
- ✅ 理解技能系统
- ✅ 尝试使用技能

### 第 4 天：工具
- ✅ 掌握文件操作
- ✅ 学会网络搜索
- ✅ 尝试浏览器控制

### 第 5 天：进阶
- ✅ 配置定时任务
- ✅ 创建子代理
- ✅ 理解记忆系统

### 第 6 天：高级
- ✅ 多 Agent 配置
- ✅ 自定义技能
- ✅ 性能优化

### 第 7 天：精通
- ✅ 安全加固
- ✅ 故障排除
- ✅ 实战项目

---

**🎉 恭喜你完成 OpenClaw 系统学习！**

*本手册基于 openclaw101.dev 和官方文档整理*  
*最后更新：2026-03-09*  
*持续更新中...*
