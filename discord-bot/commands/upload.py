import discord
from discord.ext import commands
import subprocess

class Upload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rclone_upload_direct_url(self, ctx, remote, url):
        await ctx.send(f"**Downloading file from URL and uploading to {remote}...**")
        filename = url.split('/')[-1]
        temp_path = f"/tmp/{filename}"

        download_result = subprocess.run(['wget', '-O', temp_path, url], capture_output=True, text=True)
        if download_result.returncode == 0:
            upload_result = subprocess.run(['rclone', 'copy', temp_path, remote], capture_output=True, text=True)
            if upload_result.returncode == 0:
                await ctx.send(f"**File {filename} uploaded to {remote} successfully!**")
            else:
                await ctx.send(f"Error uploading file: {upload_result.stderr}")
                subprocess.run(['rm', temp_path])
        else:
            await ctx.send(f"Error downloading file: {download_result.stderr}")
            if os.path.exists(temp_path):
                subprocess.run(['rm', temp_path])

        if os.path.exists(temp_path):
            subprocess.run(['rm', temp_path])

    @commands.command()
    async def rclone_upload_temp_cloud_url(self, ctx, remote, url):
        await ctx.send(f"**Downloading file from temporary cloud link and uploading to {remote}...**")
        filename = url.split('/')[-1]
        temp_path = f"/tmp/{filename}"

        download_result = subprocess.run(['wget', '-O', temp_path, url], capture_output=True, text=True)
        if download_result.returncode == 0:
            upload_result = subprocess.run(['rclone', 'copy', temp_path, remote], capture_output=True, text=True)
            if upload_result.returncode == 0:
                await ctx.send(f"**File {filename} uploaded to {remote} successfully!**")
            else:
                await ctx.send(f"Error uploading file: {upload_result.stderr}")
                subprocess.run(['rm', temp_path])
        else:
            await ctx.send(f"Error downloading file: {download_result.stderr}")
            if os.path.exists(temp_path):
                subprocess.run(['rm', temp_path])

        if os.path.exists(temp_path):
            subprocess.run(['rm', temp_path])

    @commands.command()
    async def rclone_api_upload(self, ctx, remote, api_url, file_id):
        await ctx.send(f"**Fetching download link from API and uploading to {remote}...**")

        response = requests.post(api_url, json={'file_id': file_id})
        if response.status_code == 200:
            download_link = response.json().get('download_link')
            if download_link:
                filename = download_link.split('/')[-1]
                temp_path = f"/tmp/{filename}"

                download_result = subprocess.run(['wget', '-O', temp_path, download_link], capture_output=True, text=True)
                if download_result.returncode == 0:
                    upload_result = subprocess.run(['rclone', 'copy', temp_path, remote], capture_output=True, text=True)
                    if upload_result.returncode == 0:
                        await ctx.send(f"**File {filename} uploaded to {remote} successfully!**")
                    else:
                        await ctx.send(f"Error uploading file: {upload_result.stderr}")
                        subprocess.run(['rm', temp_path])
                else:
                    await ctx.send(f"Error downloading file: {download_result.stderr}")
                    if os.path.exists(temp_path):
                        subprocess.run(['rm', temp_path])

                if os.path.exists(temp_path):
                    subprocess.run(['rm', temp_path])
            else:
                await ctx.send("Failed to retrieve download link from API response.")
        else:
            await ctx.send(f"Error fetching download link from API: {response.status_code} {response.text}")
