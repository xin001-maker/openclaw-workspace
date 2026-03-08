#!/bin/bash
# Heartbeat trigger script
# Add to crontab: */30 * * * * /root/.openclaw/workspace/send-heartbeat.sh

LOG_FILE="/root/.openclaw/workspace/memory/heartbeat-log.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Log heartbeat trigger
echo "## Heartbeat Triggered: $TIMESTAMP" >> "$LOG_FILE"

# Check if there's an active OpenClaw session to message
# This would need the OpenClaw CLI or API to send a message
# For now, just log the trigger

echo "[$TIMESTAMP] Heartbeat triggered - waiting for next user message to process" >> "$LOG_FILE"
