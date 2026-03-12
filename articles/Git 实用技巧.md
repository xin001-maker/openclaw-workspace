# Git 实用技巧：从入门到精通的 20 个技巧

> 用了 5 年 Git，总结的最实用技巧！每个技巧都能节省你的时间，建议收藏！

---

## 前言

你是不是也这样：
- Git 命令记不住，每次都要 Google
- 分支管理混乱，经常冲突
- 提交历史乱七八糟，不敢看
- 团队协作时，Git 成为瓶颈

**别慌！** 今天分享我用了 5 年 Git 总结的 20 个实用技巧。

**从基础到进阶，每个技巧都能立即提升你的效率！**

---

## 基础篇（新手必看）

### 技巧 1：配置用户信息

```bash
# 全局配置（所有项目）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

# 查看配置
git config --list

# 查看某个配置
git config user.name
```

**为什么重要：** 每次提交都会记录作者信息，配置错了会很尴尬。

### 技巧 2：初始化仓库

```bash
# 新建项目
mkdir my-project
cd my-project
git init

# 克隆现有项目
git clone https://github.com/username/repo.git

# 克隆特定分支
git clone -b dev https://github.com/username/repo.git
```

### 技巧 3：查看状态

```bash
# 查看仓库状态（最常用！）
git status

# 简洁模式
git status -s
```

**输出示例：**
```
 M README.md      # 修改但未暂存
A  new-file.txt   # 新文件已暂存
D  old-file.txt   # 已删除
```

### 技巧 4：添加文件

```bash
# 添加单个文件
git add README.md

# 添加所有文件
git add .

# 添加所有修改的文件（不包括新文件）
git add -u

# 交互式添加（可以选择性地添加）
git add -p
```

**技巧：** `git add -p` 可以逐块添加，适合只提交部分修改。

### 技巧 5：提交更改

```bash
# 提交并写消息
git commit -m "feat: 添加用户登录功能"

# 提交所有修改的文件
git commit -am "fix: 修复登录 bug"

# 修改上次提交
git commit --amend -m "feat: 添加用户登录功能（更新描述）"
```

**提交消息规范：**
```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 格式调整
refactor: 重构
test: 测试
chore: 构建/工具
```

---

## 分支篇（团队协作必备）

### 技巧 6：分支操作

```bash
# 查看分支
git branch

# 查看包括远程分支
git branch -a

# 创建新分支
git branch feature-login

# 创建并切换分支
git checkout -b feature-login

# 新版命令（Git 2.23+）
git switch -c feature-login

# 切换分支
git checkout feature-login
git switch feature-login

# 删除分支
git branch -d feature-login      # 安全删除（已合并）
git branch -D feature-login      # 强制删除（未合并）
```

### 技巧 7：合并分支

```bash
# 切换到主分支
git checkout main

# 合并功能分支
git merge feature-login

# 合并时不自动提交
git merge --no-commit feature-login

# 压缩合并（保持历史简洁）
git merge --squash feature-login
```

### 技巧 8：解决冲突

**冲突示例：**
```
<<<<<<< HEAD
这是主分支的内容
=======
这是功能分支的内容
>>>>>>> feature-login
```

**解决步骤：**
```bash
# 1. 编辑文件，解决冲突
# 2. 添加解决后的文件
git add conflicted-file.txt

# 3. 完成合并
git commit -m "merge: 解决登录模块冲突"

# 4. 如果搞砸了，取消合并
git merge --abort
```

### 技巧 9：分支策略

**推荐的工作流：**

```
main (生产环境)
  └── dev (开发环境)
       ├── feature/login (功能分支)
       ├── feature/payment
       └── bugfix/login-error
```

**操作示例：**
```bash
# 从 dev 创建功能分支
git checkout dev
git checkout -b feature/login

# 开发完成后合并回 dev
git checkout dev
git merge feature/login

# 删除功能分支
git branch -d feature/login
```

---

## 远程篇（GitHub/GitLab）

### 技巧 10：远程仓库操作

```bash
# 添加远程仓库
git remote add origin https://github.com/username/repo.git

# 查看远程仓库
git remote -v

# 重命名远程仓库
git remote rename origin upstream

# 删除远程仓库
git remote remove origin
```

### 技巧 11：推送和拉取

```bash
# 推送当前分支
git push

# 推送指定分支
git push origin feature-login

# 设置上游分支（之后可以直接 git push）
git push -u origin feature-login

# 强制推送（谨慎使用！）
git push -f origin feature-login

# 拉取远程更新
git pull

# 只拉取不合并
git fetch
```

**⚠️ 警告：** `git push -f` 会覆盖远程历史，不要在公共分支使用！

### 技巧 12：同步远程分支

```bash
# 获取所有远程分支
git fetch --all

# 删除本地已不存在的远程分支
git fetch --prune

# 基于远程分支创建本地分支
git checkout -b feature-login origin/feature-login
```

---

## 历史篇（时间机器）

### 技巧 13：查看提交历史

```bash
# 查看提交历史
git log

# 简洁模式（一行一个提交）
git log --oneline

# 图形化显示
git log --graph --oneline

# 查看某个文件的修改历史
git log --follow filename.txt

# 查看最近 5 次提交
git log -5

# 按作者筛选
git log --author="你的名字"

# 按时间筛选
git log --since="2 weeks ago"
git log --until="2024-01-01"
```

**实用组合：**
```bash
# 最美的日志显示
git log --graph --oneline --all --decorate
```

### 技巧 14：查看差异

```bash
# 查看工作区与暂存区的差异
git diff

# 查看暂存区与最新提交的差异
git diff --staged

# 查看两个提交的差异
git diff commit1 commit2

# 查看某个文件的差异
git diff filename.txt

# 统计差异（不显示具体内容）
git diff --stat
```

### 技巧 15：回退操作

```bash
# 撤销工作区的修改（危险！）
git checkout -- filename.txt
git restore filename.txt  # 新版命令

# 撤销暂存
git reset HEAD filename.txt
git restore --staged filename.txt  # 新版命令

# 回退到某个提交
git reset --hard commit_id      # 完全回退（会丢失修改）
git reset --soft commit_id      # 保留修改
git reset --mixed commit_id     # 默认，保留工作区修改

# 回退远程仓库（谨慎！）
git push -f origin HEAD~1
```

### 技巧 16：撤销提交

```bash
# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1

# 撤销提交并删除修改
git reset --hard HEAD~1

# 撤销任意次提交
git reset --soft HEAD~3

# 使用 revert（安全，创建新提交）
git revert commit_id
```

**区别：**
- `reset`：删除提交，会改写历史
- `revert`：创建新提交抵消修改，不改写历史

**建议：** 公共分支用 `revert`，私人分支用 `reset`。

---

## 进阶篇（效率提升）

### 技巧 17：Git Stash（临时保存）

```bash
# 保存当前修改
git stash

# 保存并写消息
git stash save "正在开发登录功能"

# 查看保存列表
git stash list

# 恢复最近的保存
git stash pop

# 恢复指定保存
git stash pop stash@{2}

# 应用但不删除
git stash apply

# 删除所有保存
git stash clear
```

**使用场景：** 正在开发功能 A，突然要修紧急 bug B。

```bash
# 1. 保存当前工作
git stash

# 2. 修 bug
git checkout -b bugfix
# ... 修复 bug ...
git commit -am "fix: 紧急 bug"
git checkout main
git merge bugfix

# 3. 恢复之前的工作
git checkout feature-login
git stash pop
```

### 技巧 18：Git Cherry-pick（挑选提交）

```bash
# 复制某个提交到当前分支
git cherry-pick commit_id

# 复制多个提交
git cherry-pick commit1 commit2 commit3

# 复制连续提交
git cherry-pick commit1^..commit3

# 复制时不自动提交
git cherry-pick -n commit_id
```

**使用场景：** bugfix 分支的修复需要应用到多个版本。

### 技巧 19：Git Rebase（变基）

```bash
# 变基到主分支
git checkout feature-login
git rebase main

# 交互式变基（可以编辑提交历史）
git rebase -i HEAD~3

# 继续变基（解决冲突后）
git rebase --continue

# 中止变基
git rebase --abort
```

**交互式变基选项：**
```
p, pick = 使用提交
r, reword = 使用提交，编辑提交消息
e, edit = 使用提交，暂停修改
s, squash = 使用提交，合并到前一个提交
f, fixup = 类似 squash，丢弃提交消息
d, drop = 删除提交
```

**⚠️ 警告：** 不要在公共分支使用 rebase！

### 技巧 20：Git Bisect（二分查找 bug）

```bash
# 开始二分查找
git bisect start

# 标记当前版本有问题
git bisect bad

# 标记某个提交没问题
git bisect good commit_id

# Git 会自动切换到中间版本，重复测试

# 找到 bug 后结束
git bisect reset
```

**使用场景：** 100 个提交前的代码是好的，现在有问题，快速定位哪个提交引入的 bug。

---

## 效率工具篇

### 技巧 21：Git 别名

```bash
# 添加别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.last "log -1 HEAD"

# 使用别名
git st      # 代替 git status
git co -b   # 代替 git checkout -b
```

**我的常用别名：**
```bash
git config --global alias.lg "log --graph --oneline --all --decorate"
git config --global alias.unstage "reset HEAD --"
git config --global alias.who "shortlog -sn --"
```

### 技巧 22：Git Hooks（自动化）

**.git/hooks/pre-commit 示例：**
```bash
#!/bin/bash
# 提交前自动检查

# 运行测试
npm test

# 检查代码格式
npm run lint

# 如果有错误，阻止提交
if [ $? -ne 0 ]; then
    echo "测试失败，请修复后再提交"
    exit 1
fi
```

**使用场景：**
- 提交前自动格式化代码
- 提交前运行测试
- 提交消息格式检查

### 技巧 23：.gitignore 最佳实践

```gitignore
# 操作系统
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo

# 依赖
node_modules/
vendor/
__pycache__/

# 构建输出
dist/
build/
*.min.js

# 日志
*.log
logs/

# 环境变量
.env
.env.local
.env.*.local

# 敏感信息
*.pem
*.key
secrets/
```

**推荐：** 使用 [gitignore.io](https://www.gitignore.io) 生成对应项目的 .gitignore。

---

## 团队协作篇

### 技巧 24：Pull Request 最佳实践

**1. 小的 PR**
- ✅ 一个 PR 只做一件事
- ✅ 控制在 200 行以内
- ✅ 容易审查

**2. 清晰的描述**
```markdown
## 变更内容
- 添加用户登录功能
- 修复登录 bug

## 测试
- [x] 单元测试通过
- [x] 手动测试登录流程

## 截图
（如果有 UI 变更）
```

**3. 及时审查**
- 24 小时内回复
- 建设性意见
- 批准或请求变更

### 技巧 25：提交消息规范

**推荐格式：**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**示例：**
```
feat(auth): 添加用户登录功能

- 实现用户名密码登录
- 添加登录表单验证
- 集成 JWT token

Closes #123
```

**类型说明：**
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档
- `style`: 格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 其他

---

## 常见问题

### Q1：提交错了分支怎么办？

```bash
# 1. 保存提交
git stash

# 2. 切换到正确分支
git checkout correct-branch

# 3. 恢复提交
git stash pop

# 4. 提交
git commit -m "..."
```

### Q2：如何删除已推送的敏感信息？

```bash
# 1. 删除文件（从历史中）
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch secrets.txt' \
  --prune-empty HEAD

# 2. 强制推送
git push -f origin main

# 3. 通知团队成员重置
git reset --hard origin/main
```

**⚠️ 警告：** 这会改写历史，需要团队配合！

### Q3：如何保持提交历史整洁？

```bash
# 1. 使用交互式变基
git rebase -i HEAD~5

# 2. 合并相关提交（squash）
# 3. 编辑提交消息（reword）
# 4. 删除无用提交（drop）
```

### Q4：大文件怎么处理？

```bash
# 使用 Git LFS
git lfs install
git lfs track "*.psd"
git lfs track "*.zip"

# 提交
git add .gitattributes
git add large-file.psd
git commit -m "add large file"
```

---

## 学习路线

### 第 1 周：基础
- ✅ 安装配置
- ✅ 基本命令（add/commit/push）
- ✅ 分支操作

### 第 2 周：进阶
- ✅ 合并与冲突
- ✅ 远程协作
- ✅ 提交历史

### 第 3 周：高级
- ✅ Rebase
- ✅ Cherry-pick
- ✅ Bisect

### 第 4 周：精通
- ✅ Hooks
- ✅ 工作流优化
- ✅ 团队协作规范

---

## 资源推荐

### 学习资源
- [Git 官方文档](https://git-scm.com/doc)
- [Pro Git 电子书](https://git-scm.com/book/zh/v2)
- [Git 图解](https://learngitbranching.js.org/)

### 工具推荐
- **Sourcetree** - 图形化 Git 客户端
- **GitKraken** - 跨平台 Git GUI
- **VS Code Git 插件** - 编辑器集成

### 练习平台
- **GitHub** - 实战练习
- **GitLab** - 团队协作
- **Gitee** - 国内加速

---

## 结语

**Git 是程序员的必备技能，但精通需要时间！**

**我的建议：**

1. **每天用** - Git 是肌肉记忆，越用越熟
2. **记笔记** - 遇到坑就记录下来
3. **看历史** - 经常 git log，理解项目演进
4. **敢尝试** - 私人仓库随便玩，搞砸了重来

**3 个月后，你会成为团队的 Git 专家！**

---

**如果这篇文章对你有帮助，欢迎：**

- ⭐ 点赞支持
- 💬 评论区分享你的 Git 技巧
- 📢 分享给需要的朋友

**代码已开源：** [GitHub - git-tips](https://github.com/你的用户名/git-tips)

---

*作者：AI 助手 | 公众号：XXX | 微信：XXX*

*专注分享 Python 自动化、效率工具、副业变现*
