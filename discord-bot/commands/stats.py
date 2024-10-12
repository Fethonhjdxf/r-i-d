import discord
from discord.ext import commands
import subprocess

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rclone_stats(self, ctx):
        result = subprocess.run(['rclone', 'about'], capture_output=True, text=True)
        if result.returncode == 0:
            await ctx.send(f"**Rclone Usage Statistics:**\n{result.stdout}")
        else:
            await ctx.send(f"Error getting statistics: {result.stderr}")
