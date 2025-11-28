#!/bin/bash

LOG_FILE=".claude/logs/bash-validation.log"
# 读取 Claude Code 传递的命令内容
COMMAND=$(cat | jq -r '.tool_input.command')


# 定义被阻止的目录模式（使用正则表达式）
## for python
BLOCKED="node_modules|\.env|__pycache__|\.git/|dist/|build/"

## for java 
## BLOCKED="node_modules|\.env|\.git/|target/|build/|\.gradle/"

## for rust
## BLOCKED="node_modules|\.env|\.git/|target/|Cargo.lock"

# 记录所有命令
echo "[$(date)] Checking: $COMMAND" >> "$LOG_FILE"

if echo "$COMMAND" | grep -qE "$BLOCKED"; then
  echo "[$(date)] BLOCKED: $COMMAND" >> "$LOG_FILE"
  echo "ERROR: Blocked directory pattern" >&2
  exit 2
else
  echo "[$(date)] ALLOWED: $COMMAND" >> "$LOG_FILE"
fi


