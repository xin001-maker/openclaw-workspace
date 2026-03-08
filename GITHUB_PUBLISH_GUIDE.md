# 📦 GitHub 项目发布指南

## 项目：Python 效率工具箱

一个实用的 Python 自动化脚本集合，帮你节省日常工作时间。

---

## 🚀 创建仓库步骤

### 1. 在 GitHub 创建新仓库

1. 访问 https://github.com/new
2. 仓库名：`python-efficiency-tools`
3. 描述：`🛠️ 实用的 Python 自动化脚本集合 - 文件重命名/Excel 合并/图片压缩`
4. 设为 **Public**（公开）
5. **不要** 勾选 "Add a README file"
6. 点击 "Create repository"

### 2. 推送代码到 GitHub

在服务器终端执行以下命令（替换 `YOUR_USERNAME` 为你的 GitHub 用户名）：

```bash
cd /root/.openclaw/workspace/python-tools

# 初始化 git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Python 效率工具箱"

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/python-efficiency-tools.git

# 推送
git push -u origin main
```

如果推送失败（分支名问题），尝试：

```bash
git branch -M main
git push -u origin main
```

### 3. 设置 GitHub Sponsors（可选）

如果你想接受赞助：

1. 访问 https://github.com/sponsors
2. 点击 "Join the waitlist" 或 "Sign up"
3. 设置赞助层级（建议：$5/月）
4. 在 README 中添加赞助链接

---

## 📝 项目内容

```
python-tools/
├── README.md              # 项目说明文档
├── LICENSE                # MIT 许可证
├── .gitignore            # Git 忽略文件
├── rename_files.py       # 文件批量重命名脚本
├── merge_excel.py        # Excel 数据合并脚本
├── compress_images.py    # 图片批量压缩脚本
└── scripts_collection.md # 脚本合集说明
```

---

## 🎯 功能介绍

### 1. 文件批量重命名 (`rename_files.py`)
- 一键整理混乱的文件
- 自定义前缀
- 使用场景：整理照片、文档、下载文件

### 2. Excel 数据合并 (`merge_excel.py`)
- 自动合并多个 Excel 文件
- 支持多个 sheet
- 使用场景：报表汇总、数据整合

### 3. 图片批量压缩 (`compress_images.py`)
- 压缩图片不失真
- 可调节压缩质量
- 使用场景：网站图片优化、节省存储空间

---

## 📢 发布后推广

### 技术文章引流

在以下平台发布介绍文章：

1. **知乎** - "我用 Python 自动化了日常工作，每天节省 2 小时"
2. **掘金** - "5 个超实用的 Python 脚本，拿来就能用"
3. **V2EX** - 分享创造板块
4. **Reddit** - r/Python, r/automation

### 文章末尾添加

```markdown
---
🔗 项目地址：https://github.com/YOUR_USERNAME/python-efficiency-tools
⭐ 如果对你有帮助，欢迎 Star 支持！
💰 赞助：https://github.com/sponsors/YOUR_USERNAME
```

---

## 💡 后续优化建议

1. 添加单元测试
2. 制作成 Python 包（pip install）
3. 添加 GUI 界面（Tkinter/PyQt）
4. 添加更多实用脚本
5. 支持配置文件

---

*准备好后告诉我，我帮你执行推送命令！*
