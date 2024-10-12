# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the rclone-index directory
COPY rclone-index /app/rclone-index

# Copy the discord-bot directory
COPY discord-bot /app/discord-bot

# Copy the start_combined.sh script
COPY start_combined.sh /app/start_combined.sh

# Install rclone, curl, bash, and unzip
RUN apt-get update && \
    apt-get install -y rclone curl bash unzip && \
    pip install --no-cache-dir -r /app/rclone-index/requirements.txt && \
    pip install --no-cache-dir -r /app/discord-bot/requirements.txt

# Make start_combined.sh and start.sh executable
RUN chmod +x /app/start_combined.sh /app/rclone-index/start.sh

# Start rclone-index and discord-bot
CMD ["sh", "/app/start_combined.sh"]
