import discord
from discord.ext import commands
import subprocess

class Rclone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rclone_copy(self, ctx, source, destination):
        result = subprocess.run(['rclone', 'copy', source, destination], capture_output=True, text=True)
        if result.returncode == 0:
            await ctx.send(f"**Copied from {source} to {destination} successfully!**")
        else:
            await ctx.send(f"Error copying: {result.stderr}")

    @commands.command()
    async def rclone_version(self, ctx):
        result = subprocess.run(['rclone', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            await ctx.send(f"**Rclone Version:**\n{result.stdout}")
        else:
            await ctx.send(f"Error retrieving version: {result.stderr}")
