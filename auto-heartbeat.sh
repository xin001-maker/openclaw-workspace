#!/bin/bash
# 自动心跳触发脚本
# 用途：每 30 分钟启动子代理自主工作
# 安装：crontab -e 然后添加：*/30 * * * * /root/.openclaw/workspace/auto-heartbeat.sh

LOG_FILE="/root/沟通文件/heartbeat-trigger.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] 心跳触发 - 启动子代理" >> "$LOG_FILE"

# 启动子代理
cd /root/.openclaw/workspace
openclaw sessions_spawn \
  --mode run \
  --runtime subagent \
  --label "heartbeat-worker" \
  --cleanup keep \
  --timeout-seconds 1800 \
  --task "
根据 HEARTBEAT.md 执行任务：
1. 检查投标进展，继续投标
2. 技术文章发布
3. GitHub 优化
4. 其他变现相关工作

完成后向主会话汇报进展。
" >> "$LOG_FILE" 2>&1

echo "[$TIMESTAMP] 子代理已启动" >> "$LOG_FILE"
