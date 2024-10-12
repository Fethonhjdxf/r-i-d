import subprocess
import os

class StatusManager:
    @staticmethod
    def download_file(url, temp_path):
        return subprocess.run(['wget', '-O', temp_path, url], capture_output=True, text=True)

    @staticmethod
    def upload_file(temp_path, remote):
        return subprocess.run(['rclone', 'copy', temp_path, remote], capture_output=True, text=True)

    @staticmethod
    def cleanup_temp_file(temp_path):
        if os.path.exists(temp_path):
            subprocess.run(['rm', temp_path])
