# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install rclone, curl, bash, and unzip
RUN apt-get update && \
    apt-get install -y rclone curl bash unzip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run start.sh when the container launches
CMD ["sh", "start.sh"]
