#!/bin/sh

# Start rclone-index
/app/rclone-index/start.sh &

# Start discord-bot
python /app/discord-bot/bot.py
