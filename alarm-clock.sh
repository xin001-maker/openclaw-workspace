#!/bin/bash
# 闹钟定时触发器
# 用法：./alarm-clock.sh "任务描述" "延迟分钟数"

TASK="$1"
DELAY_MINUTES="${2:-30}"

LOG_FILE="/root/沟通文件/alarm-clock.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] 设置闹钟：$DELAY_MINUTES 分钟后执行任务" >> "$LOG_FILE"
echo "任务：$TASK" >> "$LOG_FILE"

# 计算触发时间
TRIGGER_TIME=$(date -d "+$DELAY_MINUTES minutes" '+%Y-%m-%d %H:%M:%S')
echo "触发时间：$TRIGGER_TIME" >> "$LOG_FILE"

# 使用 at 命令设置定时任务（如果可用）
if command -v at &> /dev/null; then
    echo "cd /root/.openclaw/workspace && openclaw sessions_spawn --mode run --runtime subagent --label 'alarm-task' --cleanup keep --timeout-seconds 1800 --task '$TASK'" | at now + $DELAY_MINUTES minutes
    echo "[$TIMESTAMP] 已使用 at 命令设置定时任务" >> "$LOG_FILE"
else
    # 使用 sleep 后台运行
    (
        sleep $((DELAY_MINUTES * 60))
        cd /root/.openclaw/workspace
        openclaw sessions_spawn \
            --mode run \
            --runtime subagent \
            --label "alarm-task" \
            --cleanup keep \
            --timeout-seconds 1800 \
            --task "$TASK"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 闹钟触发 - 子代理已启动" >> "$LOG_FILE"
    ) &
    echo "[$TIMESTAMP] 已使用后台 sleep 设置定时任务 (PID: $!)" >> "$LOG_FILE"
fi

echo "✅ 闹钟已设置：$DELAY_MINUTES 分钟后执行"
